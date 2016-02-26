import urllib
import os
import re
import sys
import random

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import urllib2
import urlresolver
from resources.libs.common_addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.firelivetv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
searchicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'search.png'))
adultopt = selfAddon.getSetting('adult')
adultpass = selfAddon.getSetting('password')
iconimage = addon.queries.get('iconimage', '')
metaset = selfAddon.getSetting('enable_meta')
ftvfavs = xbmc.translatePath(os.path.join('special://home/userdata/Database', 'firelivetv.db'))
ytapi1 = 'https://www.googleapis.com/youtube/v3/search?q='
ytapi2 = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyBAdxZCHbeJwnQ7dDZQJNfcaF46MdqJ24E&type=video&maxResults=50'
ytpl = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
ytpl2 = '&maxResults=50&key=AIzaSyBAdxZCHbeJwnQ7dDZQJNfcaF46MdqJ24E'
searchlist = 'http://metalkettle.co/ukturk.jpg'


def Search():
	keyb = xbmc.Keyboard('', 'Search Fire Live TV')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm = keyb.getText()
		searchterm = searchterm.upper()
	else:
		quit()
	link = open_url(searchlist)
	slist = re.compile('<link>(.+?)</link>').findall(link)
	for item in slist:
		link = open_url(item)
		match = re.compile('name="(.+?)".+?url="(.+?)".+?img="(.+?)"', re.DOTALL).findall(link)
		if len(match) > 0:
			for name, url, thumb in match:
				if 'ImageH' in thumb: thumb = searchicon
				normname = name
				name = name.upper()
				if searchterm in name and not 'COLOR' in name:
					if 'txt' in url:
						addDir(normname, url, 3, thumb, fanart)
					elif 'youtube.com/playlist?list=' in url:
						addDir(normname, url, 3, thumb, fanart)
					elif 'youtube.com/results?search_query=' in url:
						addDir(normname, url, 3, thumb, fanart)
					else:
						addLink(normname, url, 3, thumb, fanart)
		else:
			match2 = re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>',
								re.DOTALL).findall(link)
			if len(match2) > 0:
				for name, url, thumb in match2:
					if 'ImageH' in thumb: thumb = searchicon
					if not 'http' in url: pass
					normname = name
					name = name.upper()
					if searchterm in name and not 'COLOR' in name:
						if 'txt' in url:
							addDir(normname, url, 3, thumb, fanart)
						elif 'youtube.com/playlist?list=' in url:
							addDir(normname, url, 3, thumb, fanart)
						elif 'youtube.com/results?search_query=' in url:
							addDir(normname, url, 3, thumb, fanart)
						else:
							addLink(normname, url, 3, thumb, fanart)


def AddToFavs(name, url, iconimage):
	url = url.replace(' ', '%20')
	iconimage = iconimage.replace(' ', '%20')
	string = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<Thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
	favsdb = open(ftvfavs, 'a')
	favsdb.write(string)
	favsdb.close()


def RemoveFavs(name, url, iconimage):
	filedata = None
	file = open(ftvfavs, 'r')
	filedata = file.read()
	newlist = ''
	match = re.compile('<item>(.+?)</item>', re.DOTALL).findall(filedata)
	for data in match:
		string = '\n<FAV><item>\n' + data + '</item>\n'
		if name in data:
			string = string.replace('item', ' ')
		newlist = newlist + string
	file = open(ftvfavs, 'w')
	file.truncate()
	file.write(newlist)
	file.close()
	xbmc.executebuiltin('Container.Refresh')


def Index():
	link = open_url(searchlist)
	baseurl = re.compile('<index>(.+?)</index>').findall(link)[0]
	link = open_url(baseurl)
	match = re.compile('name="(.+?)".+?url="(.+?)".+?img="(.+?)"', re.DOTALL).findall(link)
	for name, url, iconimage in match:
		if not 'XXX' in name:
			addDir(name, url, 1, iconimage, fanart)
		if 'XXX' in name:
			if adultopt == 'true':
				if adultpass == '':
					dialog = xbmcgui.Dialog()
					ret = dialog.yesno('Adult Content', 'You have opted to show adult content', '',
									   'Please set a password to prevent accidental access', 'Cancel', 'Lets Go')
					if ret == 1:
						keyb = xbmc.Keyboard('', 'Set Password')
						keyb.doModal()
						if (keyb.isConfirmed()):
							passw = keyb.getText()
							selfAddon.setSetting('password', passw)
						addDir(name, url, 1, iconimage, fanart)
			if adultopt == 'true':
				if adultpass <> '':
					addDir(name, url, 1, iconimage, fanart)
	addDir('Favourites', ftvfavs, 1, 'http://metalkettle.co/firelivetv2/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg',
		   fanart)
	addDir('Search', 'url', 4, 'http://metalkettle.co/firelivetv2/thumbs/new/Uk%20turk%20thumbnails%20search.jpg', fanart)


# addLink('Fire Live TV Twitter Feed','url',2,'http://www.metalkettle.co/firelivetv/thumbs/twitter.jpg',fanart)

def GetChans(name, url, iconimage):
	if 'Index' in url:
		GetIndex(url)
	if 'XXX' in url:
		if adultpass <> '':
			dialog = xbmcgui.Dialog()
			ret = dialog.yesno('Adult Content', 'Please enter the password you set', 'to continue', '', 'Cancel',
							   'Show me the money')
			if ret == 1:
				try:
					keyb = xbmc.Keyboard('', 'Set Password')
					keyb.doModal()
					if (keyb.isConfirmed()):
						passw = keyb.getText()
					if passw == adultpass:
						channels = GetContent(url)
					for name, url, icon in channels:
						addLink(name, url, 3, iconimage, fanart)
				except:
					pass
	if 'movies' in url:
		channels = GetContent(url)
		cnt = len(channels)
		for name, url, icon in channels:
			print
			name
			addLinkMeta(name, url, 3, iconimage, cnt, isFolder=False)
		if 'Index' in url:
			xbmc.executebuiltin('Container.SetViewMode(50)')
	elif 'XXX' not in url:
		burl = url
		link = open_url(url)
		ISFAV = ''
		if '<FAV>' in link: ISFAV = 'yes'
		if 'SportsList' in url: ISFAV = ISFAV + 'BL'
		if 'Live%20TV' in url: ISFAV = ISFAV + 'BL'
		match = re.compile('<item>(.+?)</item>', re.DOTALL).findall(link)
		for item in match:
			links = re.compile('<link>(.+?)</link>').findall(item)
			if len(links) == 1:
				channels = re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>',
									  re.DOTALL).findall(item)
				for name, url, icon in channels:
					if 'youtube.com/results?search_query=' in url:
						addDir(name, url, 3, icon, fanart, ISFAV)
					elif 'youtube.com/playlist?list=' in url:
						addDir(name, url, 3, icon, fanart, ISFAV)
					else:
						if 'txt' in url:
							addDir(name, url, 3, icon, fanart, ISFAV)
						else:
							if 'ImageH' in icon:
								addLink(name, url, 3, iconimage, fanart, ISFAV)
							else:
								addLink(name, url, 3, icon, fanart, ISFAV)
			else:
				name = re.compile('<title>(.+?)</title>').findall(item)[0]
				iconimage = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
				addLink(name, burl, 5, iconimage, fanart, ISFAV)


def GETMULTI(name, url, iconimage):
	streamurl = []
	streamname = []
	streamicon = []
	link = open_url(url)
	link = re.sub(r'\(.*\)', '', link)
	name = re.sub(r'\(.*\)', '', name)
	urls = re.compile('<item>.+?<title>' + name + '</title>(.+?)</item>', re.DOTALL).findall(link)[0]
	iconimage = re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
	links = re.compile('<link>(.+?)</link>').findall(urls)
	i = 1
	for sturl in links:
		streamurl.append(sturl)
		streamname.append('Link ' + str(i))
		dialog = xbmcgui.Dialog()
		i = i + 1
	select = dialog.select(name, streamname)
	if select == -1:
		quit()
	else:
		url = streamurl[select]
		ok = True
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage);
		liz.setInfo(type="Video", infoLabels={"Title": name})
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
		liz.setPath(url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def GetIndex(url):
	link = open_url(url)
	match = re.compile('name="(.+?)".+?url="(.+?)".+?img="(.+?)"', re.DOTALL).findall(link)
	for name, url, icon in match:
		if 'youtube.com/playlist?list=' in url:
			addDir(name, url, 3, icon, fanart)
		elif 'youtube.com/results?search_query=' in url:
			addDir(name, url, 3, icon, fanart)
		else:
			addDir(name, url, 1, icon, fanart)


def GetContent(url):
	link = open_url(url)
	list = re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>', re.DOTALL).findall(link)
	return list


def PLAYLINK(url, name, iconimage):
	try:
		if 'search' in iconimage: iconimage = icon
	except:
		pass
	if 'txt' in url:
		GetChans(name, url, iconimage)
	else:
		if 'youtube.com/results?search_query=' in url:
			searchterm = url.split('search_query=')[1]
			ytapi = ytapi1 + searchterm + ytapi2
			req = urllib2.Request(ytapi)
			req.add_header('User-Agent',
						   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link = response.read()
			response.close()
			link = link.replace('\r', '').replace('\n', '').replace('  ', '')
			match = re.compile('"videoId": "(.+?)".+?"title": "(.+?)"', re.DOTALL).findall(link)
			for ytid, name in match:
				url = 'https://www.youtube.com/watch?v=' + ytid
				addLink(name, url, 3, iconimage, fanart)
		elif 'youtube.com/playlist?list=' in url:
			searchterm = url.split('playlist?list=')[1]
			ytapi = ytpl + searchterm + ytpl2
			req = urllib2.Request(ytapi)
			req.add_header('User-Agent',
						   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link = response.read()
			response.close()
			link = link.replace('\r', '').replace('\n', '').replace('  ', '')
			match = re.compile('"title": "(.+?)".+?"videoId": "(.+?)"', re.DOTALL).findall(link)
			for name, ytid in match:
				url = 'https://www.youtube.com/watch?v=' + ytid
				addLink(name, url, 3, iconimage, fanart)
		else:
			if urlresolver.HostedMediaFile(url).valid_url():
				streamurl = urlresolver.HostedMediaFile(url).resolve()
			else:
				streamurl = url
			liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
			liz.setInfo(type="Video", infoLabels={"Title": name})
			liz.setPath(streamurl)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


#################################################################################
def showText(heading, text):
	id = 10147
	xbmc.executebuiltin('ActivateWindow(%d)' % id)
	xbmc.sleep(100)
	win = xbmcgui.Window(id)
	retry = 50
	while (retry > 0):
		try:
			xbmc.sleep(10)
			retry -= 1
			win.getControl(1).setLabel(heading)
			win.getControl(5).setText(text)
			return
		except:
			pass


def open_url(url):
	if 'firelivetv.db' in url:
		favsdb = open(ftvfavs, 'r')
		link = favsdb.read()
	else:
		url = url.replace(' ', '%20')
		url += '?%d=%d' % (random.randint(1, 10000), random.randint(1, 10000))
		req = urllib2.Request(url)
		req.add_header('User-Agent',
					   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link = response.read()
		link = link.replace('\r', '').replace('\t', '').replace('&nbsp;', '').replace('\'', '')
		response.close()
	return link


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


def addDir(name, url, mode, iconimage, fanart, description=''):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
		name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&description=" + urllib.quote_plus(description)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
	liz.setProperty('fanart_image', fanart)
	cmenu = []
	cmenu.append(('[COLOR white]Add to Fire Live TV Favourites[/COLOR]',
				  'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
	if description == 'yes':
		cmenu.append(('[COLOR red]Remove from Fire Live TV Favourites[/COLOR]',
					  'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
	liz.addContextMenuItems(items=cmenu, replaceItems=True)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addLink(name, url, mode, iconimage, fanart, description=''):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
		name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&description=" + urllib.quote_plus(description)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	if not mode == 2:
		liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
		liz.setProperty("IsPlayable", "true")
		cmenu = []
		if not 'BL' in description:
			cmenu.append(('[COLOR white]Add to Fire Live TV Favourites[/COLOR]',
						  'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % (
						  sys.argv[0], name, url, iconimage)))
		if 'yes' in description:
			cmenu.append(('[COLOR red]Remove from Fire Live TV Favourites[/COLOR]',
						  'XBMC.RunPlugin(%s?mode=8&name=%s&url=%s&iconimage=%s)' % (
						  sys.argv[0], name, url, iconimage)))
		liz.addContextMenuItems(items=cmenu, replaceItems=True)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok


def addLinkMeta(name, url, mode, iconimage, itemcount, isFolder=False):
	if metaset == 'true':
		if not 'COLOR' in name:
			splitName = name.partition('(')
			simplename = ""
			simpleyear = ""
			if len(splitName) > 0:
				simplename = splitName[0]
				simpleyear = splitName[2].partition(')')
			if len(simpleyear) > 0:
				simpleyear = simpleyear[0]
			mg = metahandlers.MetaData()
			meta = mg.get_meta('movie', name=simplename, year=simpleyear)
			u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&site=" + str(site) + "&mode=" + str(
				mode) + "&name=" + urllib.quote_plus(name)
			ok = True
			liz = xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
			liz.setInfo(type="Video", infoLabels=meta)
			liz.setProperty("IsPlayable", "true")
			contextMenuItems = []
			contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
			contextMenuItems.append(('[COLOR white]Add to Fire Live TV Favourites[/COLOR]',
									 'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % (
									 sys.argv[0], name, url, meta['cover_url'])))
			liz.addContextMenuItems(contextMenuItems, replaceItems=True)
			if not meta['backdrop_url'] == '':
				liz.setProperty('fanart_image', meta['backdrop_url'])
			else:
				liz.setProperty('fanart_image', fanart)
			ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder,
											 totalItems=itemcount)
			return ok
	else:
		u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&site=" + str(site) + "&mode=" + str(
			mode) + "&name=" + urllib.quote_plus(name)
		ok = True
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		liz.setInfo(type="Video", infoLabels={"Title": name})
		liz.setProperty('fanart_image', fanart)
		liz.setProperty("IsPlayable", "true")
		cmenu = []
		cmenu.append(('[COLOR white]Add to Fire Live TV Favourites[/COLOR]',
					  'XBMC.RunPlugin(%s?mode=6&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
		liz.addContextMenuItems(items=cmenu, replaceItems=True)
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
		return ok


def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if selfAddon.getSetting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType))


params = get_params();
url = None;
name = None;
mode = None;
site = None;
iconimage = None
try:
	site = urllib.unquote_plus(params["site"])
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
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass

if mode == None or url == None or len(url) < 1:
	Index()
elif mode == 1:
	GetChans(name, url, iconimage)
elif mode == 3:
	PLAYLINK(url, name, iconimage)
elif mode == 4:
	Search()
elif mode == 5:
	GETMULTI(name, url, icon)
elif mode == 6:
	AddToFavs(name, url, iconimage)
elif mode == 7:
	GETFAVS(url)
elif mode == 8:
	RemoveFavs(name, url, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
