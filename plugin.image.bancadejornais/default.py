#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2013~2017 enen92 & Leinad4Mind
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request, urllib.parse, urllib.error,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,codecs

addon_id = 'plugin.image.bancadejornais'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/icons/'
website = 'uggcf://24.fncb.cg/wbeanvf/'
website2 = 'uggcf://24.fncb.cg'
siteurl = codecs.decode(website, 'rot13')
siteurl2 = codecs.decode(website2, 'rot13')
dialog = xbmcgui.Dialog()

def CATEGORIES():
	link = open_url(siteurl)
	match=re.findall('<a href=\"/jornais/(\w+)\" class=\"\[  \]\">(\w+)', link, re.DOTALL)
	for section,title in match: 
		addDir('[B]'+title+'[/B]',siteurl+section,1,addonfolder+artfolder+section+'.png')

def jornal_list(url):
	link = open_url(url)
	match=re.findall('img data-src=\"(.*?)\"', link, re.DOTALL)
	match2=re.findall('data-title=\"(.*?)- SAPO 24', link, re.DOTALL)
	match3=re.findall('data-original-src=\"(.*?)\"', link, re.DOTALL)
	totalitems = len(match) + len(match2) + len(match3)
	dont = "true"
	for image, title, thumbnail in zip(match, match2, match3):
		if dont == "true":
			dont = "false"
		else:
			addLink('[B]'+title+'[/B]',thumbnail,'http:'+image,totalitems)
	xbmc.executebuiltin("Container.SetViewMode(500)")

############################################################################################################################
def open_url(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib.request.urlopen(req)
	link=response.read()
	response.close()
	return link.decode('utf-8')

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
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param

def addLink(name,url,iconimage,number_of_items):
	ok=True
	liz = xbmcgui.ListItem(name)
	liz.setArt({"icon": "DefaultImage.png", "thumb": iconimage})
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.jpg')
	liz.setInfo( type='image', infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=number_of_items)
	return ok

def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({"icon": "DefaultFolder.png", "thumb": iconimage})
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name })
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
 
params=get_params()
url=None
name=None
mode=None

try: url=urllib.parse.unquote_plus(params["url"])
except: pass
try: name=urllib.parse.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print (f"Mode: {mode}")
print (f"URL: {url}")
print (f"Name: {name}")

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: jornal_list(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
