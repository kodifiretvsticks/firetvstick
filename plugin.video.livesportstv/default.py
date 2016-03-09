import os
import sys
import re
import urllib
import base64
import logging

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import net
import pyxbmct.addonwindow as pyxbmct

net = net.Net()
addon_id = 'plugin.video.livesportstv'
selfAddon = xbmcaddon.Addon(id=addon_id)
searchlist = 'http://metalkettle.co/ukturk.jpg'
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
button_quit = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'power.png'))
button_quit_focus = xbmc.translatePath(
	os.path.join('special://home/addons/' + addon_id + '/resources/art', 'power_focus.png'))
button_focus = xbmc.translatePath(
	os.path.join('special://home/addons/' + addon_id + '/resources/art', 'button_focus1.png'))
button_no_focus = xbmc.translatePath(
	os.path.join('special://home/addons/' + addon_id + '/resources/art', 'button_no_focus1.png'))
bg = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art', 'main-bg2.png'))
window = pyxbmct.AddonDialogWindow('')
window.setGeometry(1247, 650, 100, 50)
background = pyxbmct.Image(bg)
window.placeControl(background, -4, 0, 125, 51)


def START():
	global Entertainment
	global Movies
	global Music
	global News
	global Sport
	global Docs
	global Kids
	global Food
	global USA
	global Religion
	global List
	global Icon

	# create butttons
	Entertainment = pyxbmct.Button('Entertainment', focusTexture=button_focus, noFocusTexture=button_no_focus,
								   focusedColor='0xFF000000')
	Movies = pyxbmct.Button('Movies', focusTexture=button_focus, noFocusTexture=button_no_focus,
							focusedColor='0xFF000000')
	Music = pyxbmct.Button('Music', focusTexture=button_focus, noFocusTexture=button_no_focus,
						   focusedColor='0xFF000000')
	News = pyxbmct.Button('News', focusTexture=button_focus, noFocusTexture=button_no_focus, focusedColor='0xFF000000')
	Sport = pyxbmct.Button('Sport', focusTexture=button_focus, noFocusTexture=button_no_focus,
						   focusedColor='0xFF000000')
	Docs = pyxbmct.Button('Documentary', focusTexture=button_focus, noFocusTexture=button_no_focus,
						  focusedColor='0xFF000000')
	Kids = pyxbmct.Button('Kids', focusTexture=button_focus, noFocusTexture=button_no_focus, focusedColor='0xFF000000')
	Food = pyxbmct.Button('Food', focusTexture=button_focus, noFocusTexture=button_no_focus, focusedColor='0xFF000000')
	USA = pyxbmct.Button('USA', focusTexture=button_focus, noFocusTexture=button_no_focus, focusedColor='0xFF000000')
	Religion = pyxbmct.Button('Religion', focusTexture=button_focus, noFocusTexture=button_no_focus,
							  focusedColor='0xFF000000')
	List = pyxbmct.List(buttonFocusTexture=button_focus, buttonTexture=button_no_focus, _space=11, _itemTextYOffset=-7,
						textColor='0xFFFFFFFF')
	Icon = pyxbmct.Image(icon, aspectRatio=2)
	Icon.setImage(icon)
	Quit = pyxbmct.Button(' ', noFocusTexture=button_quit, focusTexture=button_quit_focus)

	# place buttons
	window.placeControl(Entertainment, 20, 1, 8, 5)
	window.placeControl(Movies, 20, 6, 8, 5)
	window.placeControl(Music, 20, 11, 8, 5)
	window.placeControl(News, 20, 16, 8, 5)
	window.placeControl(Sport, 20, 21, 8, 5)
	window.placeControl(Docs, 20, 26, 8, 5)
	window.placeControl(Kids, 20, 31, 8, 5)
	window.placeControl(Food, 20, 36, 8, 5)
	window.placeControl(USA, 20, 41, 8, 5)
	window.placeControl(Religion, 20, 46, 8, 5)
	window.placeControl(List, 30, 1, 90, 30)
	window.placeControl(Icon, 45, 32, 60, 18)
	window.placeControl(Quit, 110, 48, 10, 3)

	# capture mouse moves or up down arrows
	window.connectEventList(
		[pyxbmct.ACTION_MOVE_DOWN,
		 pyxbmct.ACTION_MOVE_UP,
		 pyxbmct.ACTION_MOUSE_MOVE],
		LIST_UPDATE)

	# navigation
	Entertainment.controlRight(Movies)
	Entertainment.controlLeft(Quit)
	Entertainment.controlDown(List)
	Movies.controlRight(Music)
	Movies.controlLeft(Entertainment)
	Movies.controlDown(List)
	Music.controlRight(News)
	Music.controlLeft(Movies)
	Music.controlDown(List)
	News.controlRight(Sport)
	News.controlLeft(Music)
	News.controlDown(List)
	Sport.controlRight(Docs)
	Sport.controlLeft(News)
	Sport.controlDown(List)
	Docs.controlRight(Kids)
	Docs.controlLeft(Sport)
	Docs.controlDown(List)
	Kids.controlRight(Food)
	Kids.controlLeft(Docs)
	Kids.controlDown(List)
	Food.controlRight(USA)
	Food.controlLeft(Kids)
	Food.controlDown(List)
	USA.controlRight(Religion)
	USA.controlLeft(Food)
	USA.controlDown(List)
	Religion.controlRight(Quit)
	Religion.controlLeft(USA)
	Religion.controlDown(List)
	List.controlUp(Entertainment)
	List.controlLeft(Entertainment)
	List.controlRight(Quit)
	Quit.controlLeft(Religion)
	Quit.controlRight(Entertainment)
	window.setFocus(Entertainment)
	Icon.setImage(icon)

	# button actions
	window.connect(Entertainment, ENT)
	window.connect(Movies, MOVIES)
	window.connect(Music, MUSIC)
	window.connect(News, NEWS)
	window.connect(Sport, SPORT)
	window.connect(Docs, DOCS)
	window.connect(Kids, KIDS)
	window.connect(Food, FOOD)
	window.connect(USA, USAMERICA)
	window.connect(Religion, RELIGION)
	window.connect(List, PLAY_STREAM)
	window.connect(Quit, window.close)
	GetChannels(1)


def PLAY_STREAM():
	window.close()
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	xbmc.Player().play(playurl, liz, False)


def ENT():
	List.reset()
	logging.warning('ENT SELECTED')
	sec = 1
	GetChannels(sec)


def MOVIES():
	List.reset()
	logging.warning('MOVIES SELECTED')
	sec = 2
	GetChannels(sec)


def MUSIC():
	List.reset()
	logging.warning('MUSIC SELECTED')
	sec = 3
	GetChannels(sec)


def NEWS():
	List.reset()
	logging.warning('NEWS SELECTED')
	sec = 4
	GetChannels(sec)


def SPORT():
	List.reset()
	logging.warning('SPORT SELECTED')
	sec = 5
	GetChannels(sec)


def DOCS():
	List.reset()
	logging.warning('DOCS SELECTED')
	sec = 6
	GetChannels(sec)


def KIDS():
	List.reset()
	logging.warning('KIDS SELECTED')
	sec = 7
	GetChannels(sec)


def FOOD():
	List.reset()
	logging.warning('FOOD SELECTED')
	sec = 8
	GetChannels(sec)


def USAMERICA():
	List.reset()
	logging.warning('USA SELECTED')
	sec = 10
	GetChannels(sec)


def RELIGION():
	List.reset()
	logging.warning('RELIGION SELECTED')
	sec = 9
	GetChannels(sec)


def GetChannels(sec):
	global chname
	global chicon
	global chstream1
	global chstream2
	chname = []
	chicon = []
	chstream1 = []
	chstream2 = []
	match = GetContent()
	for name, iconimage, stream1, stream2, cat in match:
		if not 'Planett' in name:
			if name == 'null': name = 'Channel'
			name = name.replace('"', '').replace('.', '')
			thumb = 'https://app.uktvnow.net/' + iconimage + '|User-Agent=Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G920F Build/LMY47X)'
			if int(cat) == sec:
				chname.append(name)
				chicon.append(thumb)
				chstream1.append(stream1)
				chstream2.append(stream2)
				List.addItem(name)


def GetContent():
	token = getAPIToken('https://app.uktvnow.net/v1/get_all_channels', 'metalkettle2')
	headers = {'User-Agent': 'USER-AGENT-UKTVNOW-APP-V1',
			   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			   'Accept-Encoding': 'gzip',
			   'app-token': token,
			   'Connection': 'Keep-Alive',
			   'Host': 'app.uktvnow.net'}
	postdata = {'username': 'admin'}
	channels = net.http_POST('https://app.uktvnow.net/v1/get_all_channels', postdata, headers).content
	channels = channels.replace('\/', '/')
	channellist = re.compile(
		'"channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"').findall(
		channels)
	return channellist


def local_time(zone='Asia/Karachi'):
	from datetime import datetime
	from pytz import timezone
	other_zone = timezone(zone)
	other_zone_time = datetime.now(other_zone)
	return other_zone_time.strftime('%B-%d-%Y')


def getAPIToken(url, username):
	dt = local_time()
	s = "uktvnow-token-" + dt + "-" + "_|_-" + url + "-" + username + "-" + "_|_" + "-" + base64.b64decode(
		"MTIzNDU2IUAjJCVedWt0dm5vd14lJCNAITY1NDMyMQ==")
	import hashlib
	return hashlib.md5(s).hexdigest()


def cleanHex(text):
	def fixup(m):
		text = m.group(0)
		if text[:3] == "&#x":
			return unichr(int(text[3:-1], 16)).encode('utf-8')
		else:
			return unichr(int(text[2:-1])).encode('utf-8')

	try:
		return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
	except:
		return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))


########################################## ADDON SPECIFIC FUNCTIONS
def LIST_UPDATE():
	global playurl
	global playurl2
	global iconimage
	global name
	if window.getFocus() == List:
		pos = List.getSelectedPosition()
		iconimage = chicon[pos]
		name = chname[pos]
		Icon.setImage(iconimage)
		playurl = chstream1[pos]
		playurl2 = chstream2[pos]


def addLink(name, url, mode, iconimage, fanart, description=''):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
		name) + "&description=" + str(description)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok


START()
window.doModal()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
