#Very special thanks to Dan Elmore for the original wizard code 

###CREDIT TO LEE @ Community builds for writing the force close function



import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re, glob
import time
import downloader
import zipfile
import extract
import GoDev
import zipfile
import ntpath

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ADDON=xbmcaddon.Addon(id='plugin.program.firetvupdater')
AddonID = 'plugin.program.firetvupdater'
MainPath=xbmc.translatePath(os.path.join('special://home','addons',AddonID));
Images=xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources','images/')); 
FanArt = xbmc.translatePath(os.path.join(MainPath,'FanArt.png'));
HOME =  xbmc.translatePath('special://home/')
ADDONS =  xbmc.translatePath(os.path.join('special://home','addons',''))
Dialog =  xbmcgui.Dialog()
DialogProcess =  xbmcgui.DialogProgress()
USERDATA =  xbmc.translatePath(os.path.join('special://home/userdata',''))
GUISETTINGS =  os.path.join(USERDATA,'guisettings.xml')
THUMBNAILS =  xbmc.translatePath(os.path.join(USERDATA,'Thumbnails'))
zip =  ADDON.getSetting('zip')
USB =  xbmc.translatePath(os.path.join(zip))
skin =  xbmc.getSkinDir()
VERSION = "1.1"
PATH = "Fire TV Updater"

def MainMenu():
	Maintenance  =  ADDON.getSetting('Maintenance')
	FireTVBuildMenu  =  ADDON.getSetting('FireTVBuildMenu')
	if FireTVBuildMenu == 'true':
		addFolder('folder','Fire TV Updates','none', 'FireTVBuildMenu', 'firetvbuilds.png','','','')
	if Maintenance == 'true':
		addFolder('folder','Maintenance and Tools','fanart', 'Tools', 'maintenance.png','','','')	
	setView('movies', 'MAIN')
def FireTVBuildMenu():
    link = OPEN_URL('http://johnsrepairs.com/firetv/builds/wizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,FanArt,description in match:
        addXMLMenu(name,url,1,iconimage,FanArt,description)
    setView('movies', 'MAIN')	
def GeneralMaint():
    addFolder('','Clear Cache', 'none', 'Clear_Cache', 'clearcache.png','','','')
    addFolder('','Clear Crash Logs', 'none', 'Remove_Crash_Logs', 'crashlogs.png','','','')
    addFolder('','Clear Textures','none','Remove_Textures','cleartextures.png','','','')
    addFolder('','Clear Thumbnails','none','Remove_Thumbs','thumbnails.png','','','')
    addFolder('','Clear Packages','none','Remove_Packages','packages.png','','','')
    setView('movies', 'MAIN')	
def Tools():
    addFolder('folder','General Maintenance & Fixes', 'none', 'GeneralMaint', 'Generalmaintenance.png','','','')
    addFolder('folder','Backup/Restore','none','BackupMenu','backuprestore.png','','','')
    addFolder('','Fresh Start', 'none', 'Wipe_Kodi', 'freshstart.png','','','')
    setView('movies', 'MAIN')	
def BackupMenu():
    addFolder('folder','Backup','none','backup_option','Backup.png','','','')
    addFolder('folder','Restore','none','restore_option','Restore.png','','','')	
    setView('movies', 'MAIN')
	
def Backup_Option():
    addFolder('','Full Backup','url','backupzip','Backup.png','','','')
    setView('movies', 'MAIN')
def Restore_Option():
    addFolder('','Full restore','url','RestoreIt','restore.png','','','')
    setView('movies', 'MAIN')
def Wipe_Kodi():
    mybackuppath = xbmc.translatePath(os.path.join(USB,''))
    dp = xbmcgui.DialogProgress()	
    choice = xbmcgui.Dialog().yesno("Are you sure!!!", 'This will revert back to a blank Kodi but will leave this plugin?', '', 'Dont blame me if it goes wrong!', yeslabel='Yes',nolabel='No')
    if choice == 1:
        if skin!= "skin.confluence":
            Dialog.ok('Fire TV Updater','Please Change to the default Confluence skin','before performing a wipe.','')
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            return
        else:
            choice = xbmcgui.Dialog().yesno("Fire TV Guru", 'This will completely wipe your install.', 'Are you sure?', '', yeslabel='Yes', nolabel='No')
            if choice == 0:
                if not os.path.exists(mybackuppath):
                    os.makedirs(mybackuppath)
                vq = 'backup.zip'
                if ( not vq ): return False, 0
                title = urllib.quote_plus(vq)
                backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                exclude_dirs_full =  ['plugin.program.fire']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.setup_complete','XBMCHelper.conf']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                GoDev.Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            choice = xbmcgui.Dialog().yesno("Remove Fire TV Updater?", 'Do you also want to remove the Fire TV Updater', 'add-on and have a complete fresh start or would you', 'prefer to keep this on your system?', yeslabel='Remove',nolabel='Keep')
            if choice == 0:
                GoDev.Remove_Textures()
                trpath = xbmc.translatePath(os.path.join(ADDONS,AddonID,''))
                trtemp = xbmc.translatePath(os.path.join(HOME,'..','backup.zip'))
                GoDev.Archive_File(trpath, trtemp)
                deppath = xbmc.translatePath(os.path.join(ADDONS,'script.module.addon.common',''))
                deptemp = xbmc.translatePath(os.path.join(HOME,'..','backupdep.zip'))
                GoDev.Archive_File(deppath, deptemp)
                GoDev.Destroy_Path(HOME)
                if not os.path.exists(trpath):
                    os.makedirs(trpath)
                if not os.path.exists(deppath):
                    os.makedirs(deppath)
                time.sleep(1)
                GoDev.Read_Zip(trtemp)
                DialogProcess.create("Fire TV Updater","Checking ",'', 'Please Wait')
                DialogProcess.update(0,"", "Extracting Zip Please Wait")
                extract.all(trtemp,trpath,DialogProcess)
                GoDev.Read_Zip(deptemp)
                extract.all(deptemp,deppath,DialogProcess)
                DialogProcess.update(0,"", "Extracting Zip Please Wait")
                DialogProcess.close()
                time.sleep(1)
                killxbmc()
            elif choice == 1:
                cache.Remove_Textures()
                extras.Destroy_Path(HOME)
                dp.close()
                killxbmc()
            else: return
		
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Are you Sure?', 'This will delete all your Cache', 'It can help with Buffering issue','and can clear alot of space', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Wipe_Cache()	
        Dialog.ok("Cache Deleted", '', 'Done','')
def Remove_Crash_Logs():
    choice = xbmcgui.Dialog().yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are', 'log files generated when Kodi crashes and are','only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Delete_Logs()
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder?', 'This will free up space by deleting the zip install', 'files of your addons.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
	GoDev.Delete_Packages()	
        Dialog.ok("Packages Deleted", '', 'Done','')		
def Remove_Textures():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your textures13.db file.', 'These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Remove_Textures()
def Remove_Thumbs():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your thumbnail files.', 'These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Destroy_Path(THUMBNAILS)
        Dialog.ok("Thumbnails Removed", '', 'Dont forget to restart Kodi to reload the thumbnails and backgrounds!!!','')		
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR dodgerblue]Fire TV Updater[/COLOR]","Downloading ",'', 'Please be Patient')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Installing Please be Patient")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    Dialog = xbmcgui.Dialog()
    Dialog.ok("Fire TV Updater", 'Unfortunately the only way to get the new changes to stick is', 'to force close kodi. Click ok to force Kodi to close,', 'DO NOT use the quit/exit options in Kodi.')
    killxbmc()
def addXMLMenu(name,url,mode,iconimage,FanArt,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&FanArt="+urllib.quote_plus(FanArt)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "FanArt_Image", FanArt )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addFolder(type,name,url,mode,iconimage = '',FanArt = '',video = '',description = ''):
    if type != 'folder2' and type != 'addon':
        if len(iconimage) > 0:
            iconimage = Images + iconimage
        else:
            iconimage = 'DefaultFolder.png'
    if type == 'addon':
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = 'none'
    if FanArt == '':
        FanArt = FanArt
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&FanArt="+urllib.quote_plus(FanArt)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "FanArt_Image", FanArt )
    liz.setProperty( "Build.Video", video )
    if (type=='folder') or (type=='folder2') or (type=='tutorial_folder') or (type=='news_folder'):
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    else:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder) 
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param
def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'		

params=get_params()
url=None
name=None
mode=None
iconimage=None
FanArt=None
description=None
addon_id=None
audioaddons=None
author=None
buildname=None
data_path=None
description=None
DOB=None
email=None
fanart=None
forum=None
iconimage=None
link=None
local=None
messages=None
mode=None
name=None
posts=None
programaddons=None
provider_name=None
repo_id=None
repo_link=None
skins=None
sources=None
updated=None
unread=None
version=None
video=None
videoaddons=None
welcometext=None
zip_link=None

try:    addon_id=urllib.unquote_plus(params["addon_id"])
except: pass
try:    audioaddons=urllib.unquote_plus(params["audioaddons"])
except: pass
try:    author=urllib.unquote_plus(params["author"])
except: pass
try:    buildname=urllib.unquote_plus(params["buildname"])
except: pass
try:    data_path=urllib.unquote_plus(params["data_path"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    DOB=urllib.unquote_plus(params["DOB"])
except: pass
try:    email=urllib.unquote_plus(params["email"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    forum=urllib.unquote_plus(params["forum"])
except: pass
try:    guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    link=urllib.unquote_plus(params["link"])
except: pass
try:    local=urllib.unquote_plus(params["local"])
except: pass
try:    messages=urllib.unquote_plus(params["messages"])
except: pass
try:    mode=str(params["mode"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except: pass
try:    posts=urllib.unquote_plus(params["posts"])
except: pass
try:    programaddons=urllib.unquote_plus(params["programaddons"])
except: pass
try:    provider_name=urllib.unquote_plus(params["provider_name"])
except: pass
try:    repo_link=urllib.unquote_plus(params["repo_link"])
except: pass
try:    repo_id=urllib.unquote_plus(params["repo_id"])
except: pass
try:    skins=urllib.unquote_plus(params["skins"])
except: pass
try:    sources=urllib.unquote_plus(params["sources"])
except: pass
try:    updated=urllib.unquote_plus(params["updated"])
except: pass
try:    unread=urllib.unquote_plus(params["unread"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    version=urllib.unquote_plus(params["version"])
except: pass
try:    video=urllib.unquote_plus(params["video"])
except: pass
try:    videoaddons=urllib.unquote_plus(params["videoaddons"])
except: pass
try:    zip_link=urllib.unquote_plus(params["zip_link"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    mode=int(params["mode"])
except: pass
try:    FanArt=urllib.unquote_plus(params["FanArt"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass


print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )


if mode==None or url==None or len(url)<1:
        MainMenu()
elif mode == 'FireTVBuildMenu' : FireTVBuildMenu() #FireBuildMenu
elif mode == 'Tools' : Tools() #ToolsMenu
elif mode == 'BackupMenu' : BackupMenu() #BackupMenu
elif mode == 'backup_option': Backup_Option() #BackupMenu
elif mode == 'restore_option': Restore_Option()#RestoreMenu
elif mode == 'GeneralMaint' : GeneralMaint() #GeneralMaint
elif mode == 'Clear_Cache' : Clear_Cache() #Clear_Cache
elif mode == 'Remove_Crash_Logs' : Remove_Crash_Logs() #Remove_Crash_Logs
elif mode == 'Remove_Textures' : Remove_Textures() #Remove_Textures
elif mode == 'Remove_Thumbs' : Remove_Thumbs() #Remove_Thumbs
elif mode == 'Remove_Packages' : Remove_Packages() #Remove_Packages
elif mode == 'Wipe_Kodi' : Wipe_Kodi() #Wipe_Kodi
elif mode == 'backupzip': GoDev.Backupzip() #Backitup
elif mode == 'RestoreIt': GoDev.RestoreIt() #RestoreBuild
elif mode==1: wizard(name,url,description) #OpenWizard
xbmcplugin.endOfDirectory(int(sys.argv[1]))