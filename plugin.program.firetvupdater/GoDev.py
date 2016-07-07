import threading,xbmc,xbmcplugin,xbmcgui,re,os,xbmcaddon,sys
import shutil
import glob
import zipfile
import urlparse
import xbmcgui
import time
import extract
global debuglog

ADDON          =  xbmcaddon.Addon(id='plugin.program.firetvupdater')
dialog         =  xbmcgui.Dialog()
dialogprocess  =  xbmcgui.DialogProgress()
log_path       =  xbmc.translatePath('special://logpath/')
zip            =  ADDON.getSetting('zip')
USERDATA       =  xbmc.translatePath(os.path.join('special://home/userdata',''))
GUI            =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX         =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL        =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS           =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE         =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED       =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES       =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS            =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS        =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
HOME           =  xbmc.translatePath('special://home/')
USB            =  xbmc.translatePath(os.path.join(zip))
homedir        =  xbmc.translatePath('special://home/')
packagesfolder =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
thumbsfolder   =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))
addondatafolder=  xbmc.translatePath(os.path.join('special://home/userdata','addon_data'))
addondir       =  xbmc.translatePath('special://home/addons/plugin.program.firetvupdater')
mainaddondir   =  xbmc.translatePath('special://home/addons')
temp1          =  xbmc.translatePath('special://home/userdata')
temp2          =  xbmc.translatePath('special://temp')
images_path    =  os.path.join(addondir, 'resources/images')
skin           =  xbmc.getSkinDir()

try:
	from sqlite3 import dbapi2 as database
except:
	from pysqlite2 import dbapi2 as database

def freshstart():

	choice = xbmcgui.Dialog().yesno('[COLOR blue][B]Fire TV Updater[/COLOR][/B]  [COLOR=red][B]WARNING !!![/COLOR][/B]', 'This will erase all data and reset Kodi to defaults!','Kodi will try to force close after the process is complete.', '[COLOR=red][B]Do you want to continue?[/COLOR][/B]', nolabel='Nope',yeslabel='YES')
	if choice == 0:
		return
	elif choice == 1:
		pass

		dp = xbmcgui.DialogProgress()
	dp.create("Fire TV Updater","Please Wait")
	dp.update(1)

	
	path  = xbmc.translatePath('special://Database')
	files = glob.glob(os.path.join(path, 'Textures*.db'))
	for f in files:		
		try:
			os.remove(f)
		except:
			Shrink(f)



	for root, dirs, files in os.walk(homedir):
			for f in files:
							try:
									if f == "kodi.log" or f == "build.zip":
										pass
									else:
										path = os.path.join(root, f)
										if 'repository.firetvstick' not in path and 'plugin.program.firetvupdater' not in path and 'skin.ftv' not in path:
											dp.update(1, '', '', 'Deleting: ' + f)
											os.unlink(path)
											print 'from HOMEDIR deleted: ' + root + f
							except:
									pass
			for d in dirs:
							try:
									if d == "Database" or d == "addon_data" or d == "userdata" or d == "packages" or d == "addons" or d == "Thumbnails" or d == "temp" or d == "repository.firetvstick" or d == "plugin.program.firetvupdater" or d == "skin.ftv":
										pass
									else:
										path = os.path.join(root, d)
										if 'repository.firetvstick' not in path and 'plugin.program.firetvupdater' not in path and 'skin.ftv' not in path:
											dp.update(1, '', '', 'Deleting: ' + d)
											shutil.rmtree(os.path.join(root, d))
											print 'from HOMEDIR removed folder: ' + os.path.join(root, d)
							except:
									pass
											
			
	dp.update(30)



			
			
	for root, dirs, files in os.walk(addondatafolder):
			for f in files:
							try:
									dp.update(30, '', '', 'Deleting: ' + f)
									path = os.path.join(root, f)
									if 'repository.firetvstick' not in path:
										os.unlink(os.path.join(root, f))
										print 'from ADDONDATA deleted: ' + root + f
							except:
									pass
			for d in dirs:
							try:
									dp.update(30, '', '', 'Deleting: ' + d)
									path = os.path.join(root, d)
									if 'repository.firetvstick' not in path:
										shutil.rmtree(os.path.join(root, d))
										print 'from ADDONDATA removed folder: ' + os.path.join(root, d)
							except:
												pass		
				
			
	dp.update(50)


	for root, dirs, files in os.walk(temp1):
			for f in files:
							try:
									dp.update(50, '', '', 'Deleting: ' + f)
									path = os.path.join(root, f)
									if 'repository.firetvstick' not in path:
										os.unlink(os.path.join(root, f))
										print 'from TEMP1 deleted: ' + root + f
							except:
									pass
			for d in dirs:
							try:
									if d == "Database" or d == "addon_data" or d == "Thumbnails":
										pass
									else:
										dp.update(50, '', '', 'Deleting: ' + d)
										path = os.path.join(root, d)
										if 'repository.firetvstick' not in path :
											shutil.rmtree(os.path.join(root, d))
											print 'from TEMP1 removed folder: ' + os.path.join(root, d)
							except:
									pass	


	dp.update(65)



	for root, dirs, files in os.walk(temp2):
			for f in files:
							try:
									if f == "kodi.log" or f == "build.zip":
										pass
									else:
										dp.update(50, '', '', 'Deleting: ' + f)
										os.unlink(os.path.join(root, f))
										print 'from TEMP1 deleted: ' + root + f
							except:
									pass
			for d in dirs:
							try:
									dp.update(50, '', '', 'Deleting: ' + d)
									shutil.rmtree(os.path.join(root, d))
									print 'from TEMP2 removed folder: ' + os.path.join(root, d)
							except:
									pass	


	dp.update(70)




	for root, dirs, files in os.walk(packagesfolder):
		for f in files:
						try:
								if f == "kodi.log" or f == "build.zip":
									pass
								else:
									dp.update(50, '', '', 'Deleting: ' + f)
									os.unlink(os.path.join(root, f))
									print 'from PACKAGES deleted: ' + root + f
						except:
								pass
		for d in dirs:
						try:
								dp.update(50, '', '', 'Deleting: ' + d)
								shutil.rmtree(os.path.join(root, d))
								print 'from PACKAGES removed folder: ' + os.path.join(root, d)
						except:
								pass	


	dp.update(75)


	for root, dirs, files in os.walk(thumbsfolder):
			for f in files:
							try:
									dp.update(75, '', '', 'Deleting: ' + f)
									os.unlink(os.path.join(root, f))
									print 'from THUMBS deleted: ' + root + f
							except:
									pass
			for d in dirs:
							try:
									dp.update(75, '', '', 'Deleting: ' + d)
									shutil.rmtree(os.path.join(root, d))
									print 'from THUMBS removed folder: ' + os.path.join(root, d)
							except:
									pass	

			
			
	dp.update(85)


	for root, dirs, files in os.walk(mainaddondir):
			for f in files:
							try:
									if f == "kodi.log" or f == "build.zip":
										pass
									else:
										path = os.path.join(root, f)
										if 'repository.firetvstick' not in path and 'plugin.program.firetvupdater' not in path and 'skin.ftv' not in path:
											dp.update(85, '', '', 'Deleting: ' + f)
											os.unlink(path)
											print 'from MAINADDONDIR deleted: ' + root + f
							except:
									pass
			for d in dirs:
							try:
									if d == "packages" or d == "repository.firetvstick" or d == "plugin.program.firetvupdater" or d == "skin.ftv":
										pass
									else:
										if 'repository.firetvstick' not in path and 'plugin.program.firetvupdater' not in path and 'skin.ftv' not in path:
											dp.update(85, '', '', 'Deleting: ' + d)
											shutil.rmtree(os.path.join(root, d))
											print 'from MAINADDONDIR removed folder: ' + os.path.join(root, d)
							except:
									pass	






	dp.close

	xbmc.executebuiltin("ReloadSkin()")
	xbmc.executebuiltin("UpdateLocalAddons")
	
	killkodi()	
	
def killkodi():

	dialog = xbmcgui.Dialog()
	dialog.ok("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]", "[COLOR red][B]Kodi needs to be closed. Press OK to attempt to close Kodi[/COLOR][/B]")
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
		try: os.system('adb shell am force-stop org.xbmc.cemc')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc.cemc_pro')
		except: pass
		try: os.system('adb shell am force-stop com.semperpax.spmc16') 
		except: pass
		try: os.system('adb shell am force-stop org.lodi.mobi') 
		except: pass
		try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc.xbmc') 
		except: pass
		try: os.system('adb shell am force-stop org.xbmc')
		except: pass
		try: os.system('adb shell kill org.xbmc.kodi')
		except: pass
		try: os.system('adb shell kill org.kodi')
		except: pass
		try: os.system('adb shell kill org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell kill org.xbmc')
		except: pass
		try: os.system('adb shell kill com.semperpax.spmc16')
		except: pass
		try: os.system('adb shell kill com.semperpax')
		except: pass
		try: os.system('adb shell kill com.perfectzoneproductions.jesusboxmedia')
		except: pass
		try: os.system('adb shell kill org.xbmc.cemc')
		except: pass
		try: os.system('adb shell kill org.xbmc.cemc_pro')
		except: pass
		try: os.system('adb shell kill org.lodi.mobi')
		except: pass
		try: os.system('adb shell kill com.semperpax')
		except: pass
		dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
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
			os.system('tskill SMC.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im Kodi.exe /f')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im SMC.exe /f')
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
		
try:
	debuglog = xbmcplugin.getSetting(int(sys.argv[1]), 'debuglog')
except:
	debuglog = "0"	
		
def Add_Directory_Item(handle, url, listitem, isFolder):
	xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
def Read_Zip(url):
	z = zipfile.ZipFile(url, "r")
	for filename in z.namelist():
		if 'guisettings.xml' in filename:
			a = z.read(filename)
			r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
			match=re.compile(r).findall(a)
			for type,string,setting in match:
				setting=setting.replace('&quot;','') .replace('&amp;','&') 
				xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))
		if 'favourites.xml' in filename:
			a = z.read(filename)
			f = open(FAVS, mode='w')
			f.write(a)
			f.close()
		if 'sources.xml' in filename:
			a = z.read(filename)
			f = open(SOURCE, mode='w')
			f.write(a)
			f.close()
		if 'advancedsettings.xml' in filename:
			a = z.read(filename)
			f = open(ADVANCED, mode='w')
			f.write(a)
			f.close()
		if 'RssFeeds.xml' in filename:
			a = z.read(filename)
			f = open(RSS, mode='w')
			f.write(a)
			f.close()
		if 'keyboard.xml' in filename:
			a = z.read(filename)
			f = open(KEYMAPS, mode='w')
			f.write(a)
			f.close()  	
def Archive_File(sourcefile, destfile):
	zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
	rootlen = len(sourcefile)
	for_progress = []
	ITEM =[]
	dialogprocess.create("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]","Archiving...",'', 'Please Wait')
	for base, dirs, files in os.walk(sourcefile):
		for file in files:
			ITEM.append(file)
	N_ITEM =len(ITEM)
	for base, dirs, files in os.walk(sourcefile):
		for file in files:
			for_progress.append(file) 
			progress = len(for_progress) / float(N_ITEM) * 100  
			dialogprocess.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
			dialogprocess.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
			fn = os.path.join(base, file)
			if not 'temp' in dirs:
				if not 'plugin.program.firetvupdater' in dirs:
				   import time
				   FORCE= '01/01/1980'
				   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
				   if FILE_DATE > FORCE:
					   zipobj.write(fn, fn[rootlen:])  
	zipobj.close()
	dialogprocess.close()	
def Delete_Packages():
	print 'DELETING PACKAGES'
	packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
	for root, dirs, files in os.walk(packages_cache_path):
		file_count = 0
		file_count += len(files)
	# Count files and give option to delete
		if file_count > 0:
			for f in files:
				os.unlink(os.path.join(root, f))
			for d in dirs:
				shutil.rmtree(os.path.join(root, d))
def Delete_Logs():  
	for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
		 File=infile
		 print infile
		 os.remove(infile)
		 dialog = xbmcgui.Dialog()
  
def Wipe_Cache():
	xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
	if os.path.exists(xbmc_cache_path)==True:
		for root, dirs, files in os.walk(xbmc_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					try:
						os.unlink(os.path.join(root, f))
					except:
						pass
				for d in dirs:
					try:
						shutil.rmtree(os.path.join(root, d))
					except:
						pass
	if xbmc.getCondVisibility('system.platform.ATV2'):
		atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
		for root, dirs, files in os.walk(atv2_cache_a):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
		atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')		
		for root, dirs, files in os.walk(atv2_cache_b):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	# Set path to script.module.simple.downloader cache files
	downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
	if os.path.exists(downloader_cache_path)==True:	
		for root, dirs, files in os.walk(downloader_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	# Set path to script.image.music.slideshow cache files
	imageslideshow_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.image.music.slideshow/cache'), '')
	if os.path.exists(imageslideshow_cache_path)==True:	
		for root, dirs, files in os.walk(imageslideshow_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	# Set path to BBC iPlayer cache files
	iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
	if os.path.exists(iplayer_cache_path)==True:	
		for root, dirs, files in os.walk(iplayer_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
	if os.path.exists(itv_cache_path)==True:	
		for root, dirs, files in os.walk(itv_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	navix_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/script.navi-x/cache'), '')
	if os.path.exists(navix_cache_path)==True:	
		for root, dirs, files in os.walk(navix_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	phoenix_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.phstreams/Cache'), '')
	if os.path.exists(phoenix_cache_path)==True:	
		for root, dirs, files in os.walk(phoenix_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	ramfm_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.ramfm/cache'), '')
	if os.path.exists(ramfm_cache_path)==True:	
		for root, dirs, files in os.walk(ramfm_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
	if os.path.exists(wtf_cache_path)==True:	
		for root, dirs, files in os.walk(wtf_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	try:
		genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
		dbcon = database.connect(genesisCache)
		dbcur = dbcon.cursor()
		dbcur.execute("DROP TABLE IF EXISTS rel_list")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS rel_lib")
		dbcur.execute("VACUUM")
		dbcon.commit()
	except:
		pass
def Destroy_Path(path):
	dialogprocess.create("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]","Cleaning...",'', 'Please Wait')
	shutil.rmtree(path, ignore_errors=True)
def Remove_Textures():
	textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
	try:
		dbcon = database.connect(textures)
		dbcur = dbcon.cursor()
		dbcur.execute("DROP TABLE IF EXISTS path")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS sizes")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS texture")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
		dbcon.commit()
	except:
		pass
def Read_Zip(url):
	import zipfile
	z = zipfile.ZipFile(url, "r")
	for filename in z.namelist():
		if 'guisettings.xml' in filename:
			a = z.read(filename)
			r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
			
			match=re.compile(r).findall(a)
			print match
			for type,string,setting in match:
				setting=setting.replace('&quot;','') .replace('&amp;','&') 
				xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
				
		if 'favourites.xml' in filename:
			a = z.read(filename)
			f = open(FAVS, mode='w')
			f.write(a)
			f.close()  
						   
		if 'sources.xml' in filename:
			a = z.read(filename)
			f = open(SOURCE, mode='w')
			f.write(a)
			f.close()	
						 
		if 'advancedsettings.xml' in filename:
			a = z.read(filename)
			f = open(ADVANCED, mode='w')
			f.write(a)
			f.close()				 

		if 'RssFeeds.xml' in filename:
			a = z.read(filename)
			f = open(RSS, mode='w')
			f.write(a)
			f.close()				 
			
		if 'keyboard.xml' in filename:
			a = z.read(filename)
			f = open(KEYMAPS, mode='w')
			f.write(a)
			f.close()  			
def Check_Path():
	if zip=='':
	 if dialog.yesno("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]", "You Have Not Set Your Storage Path", 'Set The Storage Path Now ?',''):
		ADDON.openSettings()
		print '######### ZIP DIRECTORY #########'
		for filename in os.listdir(USB):
			print filename			
def RestoreIt():
	import time
	dialog = xbmcgui.Dialog()
	if zip == '':
		dialog.ok('                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
		ADDON.openSettings(sys.argv[0])
	dialogprocess.create("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]","Restoring",'', 'Please Wait')   
	lib=xbmc.translatePath(os.path.join(zip,'backup.zip'))
	Read_Zip(lib)
	dialogprocess.create("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]","Checking ",'', 'Please Wait')
	HOME = xbmc.translatePath(os.path.join('special://','home'))
	dialogprocess.update(0,"", "Extracting Zip Please Wait")
	extract.all(lib,HOME,dialogprocess)
	time.sleep(1)
	xbmc.executebuiltin('UpdateLocalAddons ')	
	xbmc.executebuiltin("UpdateAddonRepos")
	time.sleep(1)
	xbmc.executebuiltin('UnloadSkin()') 
	xbmc.executebuiltin('ReloadSkin()')	
	xbmc.executebuiltin("Loadialogprocessrofile(Master user)")
	dialogprocess.close()
	dialog.ok("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]", "All Done, DONT PRESS OK", "Wait a 5 minutes and pull the Power Cord then","")	
def Backupzip():  
	if zip == '':
		dialog.ok('                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
		ADDON.openSettings(sys.argv[0])
	to_backup = xbmc.translatePath(os.path.join('special://','home'))
	backup_zip = xbmc.translatePath(os.path.join(USB,'backup.zip'))
	Delete_Packages()	
	import zipfile
	
	dialogprocess.create("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]","Backing Up",'', 'Please Wait')
	zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
	rootlen = len(to_backup)
	for_progress = []
	ITEM =[]
	for base, dirs, files in os.walk(to_backup):
		for file in files:
			ITEM.append(file)
	N_ITEM =len(ITEM)
	for base, dirs, files in os.walk(to_backup):
		for file in files:
			for_progress.append(file) 
			progress = len(for_progress) / float(N_ITEM) * 100  
			dialogprocess.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
			fn = os.path.join(base, file)
			if not 'temp' in dirs:
				if not 'plugin.program.firetvupdater' in dirs:
				   import time
				   Spaf= '01/01/1980'
				   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
				   if FILE_DATE > Spaf:
					   zipobj.write(fn, fn[rootlen:])  
	zipobj.close()
	dialogprocess.close()
	dialog.ok("                    [COLOR blue][B]Fire TV Updater[/COLOR][/B]", "You Are Now Backed Up", '','')