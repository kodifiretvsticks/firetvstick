import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys
import shutil
import urllib2, urllib
import re, glob
import time
import downloader
import zipfile
import extract
import GoDev
import zipfile
import ntpath

global debuglog

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ADDON = xbmcaddon.Addon(id='plugin.program.firetvupdater')
AddonID = 'plugin.program.firetvupdater'
MainPath = xbmc.translatePath(os.path.join('special://home', 'addons', AddonID));
Images = xbmc.translatePath(os.path.join('special://home', 'addons', AddonID, 'resources', 'images/'));
FanArt = xbmc.translatePath(os.path.join(MainPath, 'FanArt.png'));
HOME = xbmc.translatePath('special://home/')
ADDONS = xbmc.translatePath(os.path.join('special://home', 'addons', ''))
Dialog = xbmcgui.Dialog()
DialogProcess = xbmcgui.DialogProgress()
USERDATA = xbmc.translatePath(os.path.join('special://home/userdata', ''))
GUISETTINGS = os.path.join(USERDATA, 'guisettings.xml')
THUMBNAILS = xbmc.translatePath(os.path.join(USERDATA, 'Thumbnails'))
zip = ADDON.getSetting('zip')
USB = xbmc.translatePath(os.path.join(zip))
skin = xbmc.getSkinDir()
VERSION = ""
PATH = "Fire TV Updater"


def MainMenu():
    addFolder('folder', '[COLOR orangered][B]Fire TV Updates[/COLOR][/B]', 'fanart', 'FireTVBuildMenu',
              'firetvbuilds.png', '', '', '')
    addFolder('folder', '[COLOR orangered][B]Extra Addons and Fixes[/COLOR][/B]', 'fanart', 'FixesMenu',
              'Generalmaintenance.png', '', '', '')
    addFolder('folder', '[COLOR orangered][B]Maintenance and Tools[/COLOR][/B]', 'fanart', 'Tools', 'maintenance.png',
              '', '', '')
    addFolder('folder', '[COLOR cyan][B]Force Close Kodi/Media Center[/COLOR][/B]', 'fanart', 'ForceClose',
              'maintenance.png', '', '', '')
    addFolder('folder', '[COLOR red][B]!!!-->Fresh Start<--!!![/COLOR][/B]', 'fanart', 'FreshStart', 'freshstart.png',
              '', '', '')  # ForceClose
    setView('movies', 'MAIN')


def FireTVBuildMenu():
    link = OPEN_URL('http://johnsrepairs.com/firetv/builds/toolbox.xml').replace('\n', '').replace('\r', '')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name, url, iconimage, FanArt, description in match:
        addXMLMenu(name, url, 1, iconimage, FanArt, description)
    setView('movies', 'MAIN')


def FixesMenu():
    link = OPEN_URL('http://firetvguru.net/build/fixes.xml').replace('\n', '').replace('\r', '')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name, url, iconimage, FanArt, description in match:
        addXMLMenu(name, url, 1, iconimage, FanArt, description)
    setView('movies', 'MAIN')


def GeneralMaint():
    addFolder('', '[COLOR orange][B]Clear Cache[/COLOR][/B]', 'none', 'Clear_Cache', 'clearcache.png', '', '', '')
    addFolder('', '[COLOR orange][B]Clear Crash Logs[/COLOR][/B]', 'none', 'Remove_Crash_Logs', 'crashlogs.png', '', '',
              '')
    addFolder('', '[COLOR orange][B]Clear Textures[/COLOR][/B]', 'none', 'Remove_Textures', 'cleartextures.png', '', '',
              '')
    addFolder('', '[COLOR orange][B]Clear Thumbnails[/COLOR][/B]', 'none', 'Remove_Thumbs', 'thumbnails.png', '', '',
              '')
    addFolder('', '[COLOR orange][B]Clear Packages[/COLOR][/B]', 'none', 'Remove_Packages', 'packages.png', '', '', '')
    setView('movies', 'MAIN')


def Tools():
    addFolder('folder', '[COLOR orange][B]General Maintenance & Fixes[/COLOR][/B]', 'none', 'GeneralMaint',
              'Generalmaintenance.png', '', '', '')
    addFolder('folder', '[COLOR orange][B]Backup/Restore[/COLOR][/B]', 'none', 'BackupMenu', 'backuprestore.png', '',
              '', '')
    addFolder('', '[COLOR lime][B]Force Update Addons/Repos[/COLOR][/B]', 'none', 'forceUpdate', 'freshstart.png', '',
              '', '')
    addFolder('', '[COLOR red][B]Fresh Start[/COLOR][/B]', 'none', 'Wipe_Kodi', 'freshstart.png', '', '', '')
    setView('movies', 'MAIN')


def FreshStart():
    addFolder('', '[COLOR red][B]Fresh Start[/COLOR][/B]', 'none', 'Wipe_Kodi', 'freshstart.png', '', '', '')
    setView('movies', 'MAIN')


def ForceClose():
    addFolder('', '[COLOR red][B]Force Close[/COLOR][/B]', 'none', 'ForceClose', 'Generalmaintenance.png', '', '', '')
    setView('movies', 'MAIN')


def BackupMenu():
    addFolder('folder', '[COLOR orange][B]Backup[/COLOR][/B]', 'none', 'backup_option', 'Backup.png', '', '', '')
    addFolder('folder', '[COLOR orange][B]Restore[/COLOR][/B]', 'none', 'restore_option', 'Restore.png', '', '', '')
    setView('movies', 'MAIN')


def Backup_Option():
    addFolder('', '[COLOR orange][B]Full Backup[/COLOR][/B]', 'url', 'backupzip', 'Backup.png', '', '', '')
    setView('movies', 'MAIN')


def Restore_Option():
    addFolder('', '[COLOR orange][B]Full restore[/COLOR][/B]', 'url', 'RestoreIt', 'restore.png', '', '', '')
    setView('movies', 'MAIN')


def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('[COLOR blue][B]Fire TV Updater[/COLOR][/B]',
                                    '									  [COLOR red][B]Are you Sure?[/COLOR][/B]',
                                    '					  [COLOR red][B]This will delete all your Cache.[/COLOR][/B]',
                                    nolabel='Cancel', yeslabel='Delete')
    if choice == 1:
        GoDev.Wipe_Cache()
        Dialog.ok("[COLOR blue][B]Fire TV Updater[/COLOR][/B]", '',
                  '						   [COLOR lime][B]Cache Deleted[/COLOR][/B]', '')


def Remove_Crash_Logs():
    choice = xbmcgui.Dialog().yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are',
                                    'log files generated when Kodi crashes and are',
                                    'only used for debugging purposes.', nolabel='Cancel', yeslabel='Delete')
    if choice == 1:
        GoDev.Delete_Logs()


def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('[COLOR blue][B]Fire TV Updater[/COLOR][/B]',
                                    '							   [COLOR red][B]Delete Packages Folder?[/COLOR][/B]',
                                    '		   [COLOR red][B]This will free up space by deleting unused zips.[/COLOR][/B]',
                                    '', nolabel='Cancel', yeslabel='Delete')
    if choice == 1:
        GoDev.Delete_Packages()
        Dialog.ok("[COLOR blue][B]Fire TV Updater[/COLOR][/B]", '',
                  '									[COLOR lime][B]Packages Deleted[/COLOR][/B]', '')


def Remove_Textures():
    choice = xbmcgui.Dialog().yesno('[COLOR cyan][B]Clear Cached Images?[/COLOR][/B]',
                                    'This will clear your textures13.db file.', 'These will automatically be',
                                    'repopulated after a restart.', nolabel='Cancel', yeslabel='Delete')
    if choice == 1:
        GoDev.Remove_Textures()


def Remove_Thumbs():
    choice = xbmcgui.Dialog().yesno('[COLOR blue][B]Fire TV Updater[/COLOR][/B]',
                                    '						[COLOR lime][B]Clear Cached Images?[/COLOR][/B]',
                                    '				[COLOR lime][B]This will clear your thumbnail files.[/COLOR][/B]',
                                    '			 [COLOR lime][B]These will be repopulated after a restart.[/COLOR][/B]',
                                    nolabel='Cancel', yeslabel='Delete')
    if choice == 1:
        GoDev.Destroy_Path(THUMBNAILS)
        Dialog.ok("[COLOR blue][B]Fire TV Updater[/COLOR][/B]",
                  '						[COLOR lime][B]Thumbnails Removed[/COLOR][/B]',
                  '		 [COLOR red][B]Dont forget to restart Kodi to reload the thumbnails and backgrounds!!![/COLOR][/B]',
                  '')


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def wizard(name, url, description):
    path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]", "Downloading ", '', 'Please be Patient')
    lib = os.path.join(path, 'build.zip')
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
    time.sleep(2)
    dp.update(0, "", "[COLOR lime][B]Installing Please be Patient[/COLOR][/B]")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.allWithProgress(lib, addonfolder, dp)
    choice = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]",
                                    'Just installed the build or a fix choose reset',
                                    'If you did something else choose Force Close', '', yeslabel='FORCE CLOSE',
                                    nolabel='RESET')
    if choice == 0:
        FASTRESET()
        return
    elif choice == 1:
        killkodi()


def addXMLMenu(name, url, mode, iconimage, FanArt, description):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&FanArt=" + urllib.quote_plus(
        FanArt) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("FanArt_Image", FanArt)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addFolder(type, name, url, mode, iconimage='', FanArt='', video='', description=''):
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
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&FanArt=" + urllib.quote_plus(FanArt) + "&video=" + urllib.quote_plus(
        video) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("FanArt_Image", FanArt)
    liz.setProperty("Build.Video", video)
    if (type == 'folder') or (type == 'folder2') or (type == 'tutorial_folder') or (type == 'news_folder'):
        ok = Add_Directory_Item(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    else:
        ok = Add_Directory_Item(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def killkodi():
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]",
              "[COLOR red][B]Kodi needs to be closed. Press OK to attempt to close Kodi[/COLOR][/B]")
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx':  # OSX
        print "############   try osx force close  #################"
        try:
            os.system('killall -9 XBMC')
        except:
            pass
        try:
            os.system('killall -9 Kodi')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close",
                  "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",
                  '')
    elif myplatform == 'linux':  # Linux
        print "############   try linux force close  #################"
        try:
            os.system('killall XBMC')
        except:
            pass
        try:
            os.system('killall Kodi')
        except:
            pass
        try:
            os.system('killall -9 xbmc.bin')
        except:
            pass
        try:
            os.system('killall -9 kodi.bin')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close",
                  "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",
                  '')
    elif myplatform == 'android':  # Android
        print "############   try android force close  #################"
        try:
            os.system('adb shell am force-stop org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.cemc')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.cemc_pro')
        except:
            pass
        try:
            os.system('adb shell am force-stop com.semperpax.spmc16')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.lodi.mobi')
        except:
            pass
        try:
            os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill com.semperpax.spmc16')
        except:
            pass
        try:
            os.system('adb shell kill com.semperpax')
        except:
            pass
        try:
            os.system('adb shell kill com.perfectzoneproductions.jesusboxmedia')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.cemc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.cemc_pro')
        except:
            pass
        try:
            os.system('adb shell kill org.lodi.mobi')
        except:
            pass
        try:
            os.system('adb shell kill com.semperpax')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ",
                  "[COLOR=yellow][B]MUST[/COLOR][/B] force close Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",
                  "Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows':  # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('tskill SMC.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im SMC.exe /f')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close",
                  "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",
                  "Use task manager and NOT ALT F4")
    else:  # ATV
        print "############   try atv force close  #################"
        try:
            os.system('killall AppleTV')
        except:
            pass
        print "############   try raspbmc force close  #################"  # OSMC / Raspbmc
        try:
            os.system('sudo initctl stop kodi')
        except:
            pass
        try:
            os.system('sudo initctl stop xbmc')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close",
                  "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.",
                  "Your platform could not be detected so just pull the power cable.")


def forceUpdate():
    xbmc.executebuiltin('UpdateAddonRepos()')
    xbmc.executebuiltin('UpdateLocalAddons()')
    Dialog.ok("[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]", '        Addons/Repos updates will be checked ', '', '')


def FASTRESET():
    Dialog.ok("[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]",
              'To start using the build please switch the skin System > Appearance > Skin Confluence... if images are not showing, just restart Kodi',
              'Click OK to Continue', '')
    xbmc.executebuiltin('ActivateWindow(Home)')
    xbmc.executebuiltin('Mastermode')
    xbmc.executebuiltin('LoadProfile(Master user,[prompt])')
    xbmc.executebuiltin('ActivateWindow(Home)')


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


try:
    debuglog = xbmcplugin.getSetting(int(sys.argv[1]), 'debuglog')
except:
    debuglog = "0"
params = get_params()
url = None
name = None
mode = None
iconimage = None
FanArt = None
description = None
addon_id = None
audioaddons = None
author = None
buildname = None
data_path = None
description = None
DOB = None
email = None
fanart = None
forum = None
iconimage = None
link = None
local = None
messages = None
mode = None
name = None
posts = None
programaddons = None
provider_name = None
repo_id = None
repo_link = None
skins = None
sources = None
updated = None
unread = None
version = None
video = None
videoaddons = None
welcometext = None
zip_link = None
try:
    addon_id = urllib.unquote_plus(params["addon_id"])
except:
    pass
try:
    audioaddons = urllib.unquote_plus(params["audioaddons"])
except:
    pass
try:
    author = urllib.unquote_plus(params["author"])
except:
    pass
try:
    buildname = urllib.unquote_plus(params["buildname"])
except:
    pass
try:
    data_path = urllib.unquote_plus(params["data_path"])
except:
    pass
try:
    description = urllib.unquote_plus(params["description"])
except:
    pass
try:
    DOB = urllib.unquote_plus(params["DOB"])
except:
    pass
try:
    email = urllib.unquote_plus(params["email"])
except:
    pass
try:
    fanart = urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    forum = urllib.unquote_plus(params["forum"])
except:
    pass
try:
    guisettingslink = urllib.unquote_plus(params["guisettingslink"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    link = urllib.unquote_plus(params["link"])
except:
    pass
try:
    local = urllib.unquote_plus(params["local"])
except:
    pass
try:
    messages = urllib.unquote_plus(params["messages"])
except:
    pass
try:
    mode = str(params["mode"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    pictureaddons = urllib.unquote_plus(params["pictureaddons"])
except:
    pass
try:
    posts = urllib.unquote_plus(params["posts"])
except:
    pass
try:
    programaddons = urllib.unquote_plus(params["programaddons"])
except:
    pass
try:
    provider_name = urllib.unquote_plus(params["provider_name"])
except:
    pass
try:
    repo_link = urllib.unquote_plus(params["repo_link"])
except:
    pass
try:
    repo_id = urllib.unquote_plus(params["repo_id"])
except:
    pass
try:
    skins = urllib.unquote_plus(params["skins"])
except:
    pass
try:
    sources = urllib.unquote_plus(params["sources"])
except:
    pass
try:
    updated = urllib.unquote_plus(params["updated"])
except:
    pass
try:
    unread = urllib.unquote_plus(params["unread"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    version = urllib.unquote_plus(params["version"])
except:
    pass
try:
    video = urllib.unquote_plus(params["video"])
except:
    pass
try:
    videoaddons = urllib.unquote_plus(params["videoaddons"])
except:
    pass
try:
    zip_link = urllib.unquote_plus(params["zip_link"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    FanArt = urllib.unquote_plus(params["FanArt"])
except:
    pass
try:
    description = urllib.unquote_plus(params["description"])
except:
    pass
print str(PATH) + ': ' + str(VERSION)
print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "IconImage: " + str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType))


if mode == None or url == None or len(url) < 1:
    MainMenu()
elif mode == 'FireTVBuildMenu':
    FireTVBuildMenu()  # FireBuildMenu
elif mode == 'ForceClose':
    ForceClose()  # ForceClose
elif mode == 'FreshStart':
    FreshStart()  # FreshStart
elif mode == 'forceUpdate':
    forceUpdate()  # ForceUpdate
elif mode == 'Tools':
    Tools()  # ToolsMenu
elif mode == 'BackupMenu':
    BackupMenu()  # BackupMenu
elif mode == 'backup_option':
    Backup_Option()  # BackupMenu
elif mode == 'restore_option':
    Restore_Option()  # RestoreMenu
elif mode == 'GeneralMaint':
    GeneralMaint()  # GeneralMaint
elif mode == 'Clear_Cache':
    Clear_Cache()  # Clear_Cache
elif mode == 'Remove_Crash_Logs':
    Remove_Crash_Logs()  # Remove_Crash_Logs
elif mode == 'Remove_Textures':
    Remove_Textures()  # Remove_Textures
elif mode == 'Remove_Thumbs':
    Remove_Thumbs()  # Remove_Thumbs
elif mode == 'Remove_Packages':
    Remove_Packages()  # Remove_Packages
elif mode == 'Wipe_Kodi':
    GoDev.freshstart()  # Wipe_Kodi
elif mode == 'backupzip':
    GoDev.Backupzip()  # Backitup
elif mode == 'RestoreIt':
    GoDev.RestoreIt()  # RestoreBuild
elif mode == 1:
    wizard(name, url, description)  # OpenWizard
elif mode == 'FixesMenu':
    FixesMenu()  # FixesMenu
xbmcplugin.endOfDirectory(int(sys.argv[1]))
