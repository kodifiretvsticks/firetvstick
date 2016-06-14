import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, base64, sys, xbmcvfs
import urllib2, urllib
import re
import time

USERDATA = xbmc.translatePath(os.path.join('special://home/userdata', ''))
CHECKVERSION = os.path.join(USERDATA, 'version.txt')
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
checkver = my_addon.getSetting('checkupdates')
dialog = xbmcgui.Dialog()
if not os.path.exists(CHECKVERSION):
    file = open(CHECKVERSION, 'w')
    file.write("<build>FireTv</build><version>0</version>")
    file.close()
checkurl = "http://johnsrepairs.com/firetv/builds/version.txt"
vers = open(CHECKVERSION, "r")
regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
for line in vers:
    if checkver != 'false':
        currversion = regex.findall(line)
        for build, vernumber in currversion:
            if vernumber > 0:
                req = urllib2.Request(checkurl)
                req.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
                match = re.compile('<build>' + build + '</build><version>(.+?)</version>').findall(link)
                for newversion in match:
                    if newversion > vernumber:
                        yes_pressed = xbmcgui.Dialog().yesno("[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]",
                                                             '                    [COLOR lime]There is a new update!![/COLOR]',
                                                             '[COLOR snow]Would you like to install the latest build?[/COLOR]',
                                                             '', yeslabel='YES', nolabel='LATER')
                        if yes_pressed:
                            dialog.ok('[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]',
                                      '[COLOR snow]a FRESH START is required for the update... Run the FRESH START in the NEXT WINDOW then INSTALL the new build version[/COLOR]',
                                      '', '')
                            xbmc.executebuiltin("ActivateWindow(10001,plugin://plugin.program.firetvupdater/,return)")
                        else:
                            dialog.ok('[COLOR dodgerblue][B]Fire TV Updater[/COLOR][/B]',
                                      '[COLOR snow]No Problem, you can always run the update from the wizard when its convenient for you.[/COLOR]',
                                      '', '')
