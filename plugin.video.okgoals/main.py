# -*- coding: utf-8 -*-

""" OKGoals
    2015~2021 fightnight/Leinad4Mind
"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,os,re,sys, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse,html.entities,requests,html.parser

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
art=os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources','art')
MainURL = 'https://www.okgoals.com/'
TugaURL = 'https://www.goalsoftheworld.tk/goals-in-Portugal.html'
h = html.parser.HTMLParser()

def main_menu():
      addDir(translation(30010),MainURL,2,os.path.join(art,'ulgolos.png'),1)
      '''addDir(translation(30011),TugaURL,7,os.path.join(art,'ligapt.png'),1)'''
      addDir(translation(30012),MainURL,3,os.path.join(art,'ugolosl2.png'),1)
      addDir(translation(30001),MainURL,4,os.path.join(art,'semana.png'),1)
      addDir(translation(30013),MainURL + 'seasons-archive.php',5,os.path.join(art,'epoca.png'),1)
      addDir(translation(30002),MainURL,6,os.path.join(art,'lupa.png'),1)
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def portugueseleague(url):
      contents= re.compile("""class='linkgoal sapo' id='(.+?)'><h1.+?><img.+?src='.+?'.+?><span.+?>(.+?)\((.+?):(.+?)\)\s*-\s*(.+?)\s*([0-9]*)\s*vs\s*([0-9]*)\s*(.+?)</span></h1>""").findall(open_url(url))
      from random import randint
      for urllink,data,hour1,hour2,team1,result1,result2,team2 in contents:
            if len(result1)==0 : result1=str('#')
            if len(result2)==0 : result2=str('#')
            addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange](%sh%s)[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hour1,hour2,clean(team1.encode('ascii','xmlcharrefreplace')),result1,result2,clean(team2.encode('ascii','xmlcharrefreplace'))),'https://www.goalsoftheworld.tk/getcontent.php?rand=%s&id_results=%s' % (str(randint(1, 100)),urllink),1,os.path.join(art,'pt.png'),len(contents),pasta=False)
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def leaguelists(url):
      leagues=re.compile("""<li class='active'><a href='(.+?)' class="menulinks">.+?alt="(.+?)" src="https://www.okgoals.com/images/(.+?)"> (.+?)</span>""").findall(open_url(url))
      for urllink,liga,thumb,country in leagues:
            liga=liga.replace('England','Premiere League')
            addDir('%s (%s)' % (liga.capitalize().title(),country.capitalize().title()),MainURL + urllink,2,os.path.join(art,thumb),len(leagues))
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def previousseasons(url):
      previous=re.compile('<a href="([^"]+?)">([^"]+?)</a><BR />').findall(open_url(url).replace('amp;',''))
      for urllink,title in previous:
            addDir(title,MainURL + urllink,8,os.path.join(art,'proxima.png'),len(previous))
      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def request(url,special=False):
      link=open_url(url).replace('&nbsp;','')
      if special:
            listagolos=re.compile('<div id=".+?"><a href="([a-z0-9-]+?)"><img.+?src="images/([a-z]+?).png" />\s+?([0-9]{4}\.[0-9]{2}\.[0-9]{2})\s*(\([0-9]{2}h[0-9]{2}\))\s*-\s*([A-Za-z ]+?)\s*([0-9]*)\s*-\s*([0-9]*)\s*(.+?)</a></div>').findall(link)
            for urllink,thumb,data,hora,team1,result1,result2,team2, *extras in listagolos:
                  addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange]%s[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora,team1,result1,result2,team2),MainURL + urllink,1,os.path.join(art,'%s.png' % (thumb)),len(listagolos),pasta=False)
      else:
            listagolos=re.compile('<div id=".+?"><a href="([a-z0-9-]+?)"><img.+?src="(images/|https://www.okgoals.com/images/)([a-z]+?).png" />\s+?([0-9]{4}\.[0-9]{2}\.[0-9]{2})\s*(\([0-9]{2}h[0-9]{2}\))\s*-\s*([A-Za-z ]+?)\s*([0-9]*)\s*-\s*([0-9]*)\s*(.+?)</a></div>').findall(link)
            for urllink,trash,thumb,data,hora,team1,result1,result2,team2 in listagolos:
                if(thumb == ''):thumb=pt
                addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange]%s[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora,team1,result1,result2,team2),MainURL + urllink,1,os.path.join(art,'%s.png' % (thumb)),len(listagolos),pasta=False)

      if re.search('page-start', link):
            try:
                  try:pageurl=re.compile('</b> <a href="(.+?)">').findall(link)[0]
                  except: pageurl=re.compile('</b><a href="(.+?)">').findall(link)[0]
                  pagevalue=int(re.compile('page-start_from_(.+?)_archive.+?.html').findall(pageurl)[0])
                  page=int((pagevalue/30)+1)
                  if special==True: mode=8
                  else: mode=2
                  addDir('[COLOR blue][B]%s %s[/COLOR][/B]' % (translation(30003),page),MainURL + pageurl,mode,os.path.join(art,'proxima.png'),1)
            except: pass

      if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")

def capture(name,url):
      link=open_url(url)
      linkoriginal = link
      if re.search('okgoals',url):
            goals=True
            '''
            link=link.replace('<div style="float:left;"><iframe','').replace('"contentjogos">','"contentjogos"></iframe>')
            ij=link.find('"contentjogos">')
            link=link[ij:]
            '''
      else: goals=False
      goals=True
      titles=[]; linking=[]
      aliezref=int(0)
      aliez=re.compile('<iframe.+?src="https://emb.aliez.tv/(.+?)"').findall(link)
      if aliez:
            for code in aliez:
                  aliezref=int(aliezref + 1)
                  if len(aliez)==1: aliez2=str('')
                  else: aliez2=' #' + str(aliezref)
                  titles.append('Aliez' + aliez2)
                  linking.append('https://emb.aliez.tv/' + code)
      dailymotionref=int(0)
      dailymotion=re.compile('src="https://www.dailymotion.com/embed/video/(.+?)"',re.DOTALL|re.M).findall(link)
      if not dailymotion: dailymotion = re.compile('src="https://www.dailymotion.com/embed/video/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)
     
      if dailymotion:
            for code in dailymotion:
                  golo=findgoal(link,code)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Dailymotion' + golo)
                  linking.append('https://www.dailymotion.com/video/' + code)
      fbvideoref=int(0)
      fbvideo=re.compile('src="https://www.facebook.com/video/embed.+?video_id=(.+?)"',re.DOTALL|re.M).findall(link)
      if fbvideo:
           for code in fbvideo:
                 golo=findgoal(link,code)
                 if golo: golo=' (%s)' % (golo)
                 titles.append('Facebook' + golo)
                 linking.append("https://www.facebook.com/video/embed?video_id=" + code)
      kiwiref=int(0)
      kiwi=re.compile('src="https://v.kiwi.kz/v2/(.+?)/"',re.DOTALL|re.M).findall(link)
      if kiwi:
            for code in kiwi:
                  golo=findgoal(link,code)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Kiwi'+ golo)
                  linking.append(code)
      #Falta
      longtailref=int(0)
      longtail=re.compile('flashvars=".+?".+?src="https://player.longtailvideo.com/player5.2.swf"').findall(link)
      if longtail:
            for code in longtail:
                  longtailref=int(longtailref+1)
                  if len(longtail)==1: longtail2=str('')
                  else: longtail2=' #' + str(longtailref)
                  titles.append('Longtail' + longtail2 + ' (' + translation(30004) + ')')
                  linking.append(0)
      metauaref=int(0)
      metaua=re.compile('src="https://video.meta.ua/players/video/3.2.19k/Player.swf.+?fileID=(.+?)&').findall(link)
      if metaua:
            for code in metaua:
                  metauaref=int(metauaref+1)
                  if len(metaua)==1: metaua2=str('')
                  else: metaua2=' #' + str(metauaref)
                  titles.append('Meta.ua' + metaua2 + ' (' + translation(30004) + ')')
                  linking.append(0)
      playwire=re.compile('data-publisher-id="(.+?)" data-video-id="(.+?)"').findall(link)
      if not playwire: playwire=re.compile('https://config.playwire.com/videos/(.+?)/(.+?)/').findall(link)
      if playwire:
          for publisher,code in playwire:
                  if publisher=='v2': publisher='configopener'
                  golo=findgoal(link,code)
                  if golo: golo=' (%s)' % (golo)
                  if "media only" in golo:golo=''
                  
                  titles.append('Playwire' + golo)
                  linking.append('https://cdn.playwire.com/v2/%s/config/%s.json' % (publisher,code))
            
      playwire_v2=re.compile('//config.playwire.com/(.+?)/videos/v2/(.+?).json').findall(link)
      if playwire_v2:
          for publisher,code in playwire_v2:
                  golo=findgoal(link,code)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Playwire' + golo)
                  linking.append('https://config.playwire.com/%s/videos/v2/%s.json' % (publisher,code))
                  
      rutuberef=int(0)
      rutube=re.compile('src=".+?rutube.ru/video/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if not rutube: rutube=re.compile('value="https://video.rutube.ru/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)  
      if not rutube: rutube=re.compile('src="https://rutube.ru/video/embed/(.+?)"',re.DOTALL|re.M).findall(linkoriginal)
      if rutube:
            for code in rutube:
                  golo=findgoal(link,code)
                  if golo: golo=' (%s)' % (golo)
                  titles.append("Rutube" + golo)
                  linking.append(code)
      saporef=int(0)
      sapo=re.compile('src=".+?videos.sapo.pt/playhtml.+?file=(.+?)/1&"',re.DOTALL|re.M).findall(link)
      if not sapo: sapo=re.compile('src=".+?videos.sapo.pt/playhtml.+?file=(.+?)/1"',re.DOTALL|re.M).findall(link)
      if sapo:
            for urllink in sapo:
                  if goals==True:
                        golo=findgoal(link,urllink)
                        if golo: golo=' (%s)' % (golo)
                  else:
                        saporef=int(saporef + 1)
                        if len(sapo)==1: golo=str('')
                        else: golo=' #' + str(saporef)
                  titles.append('Videos Sapo' + golo)
                  linking.append(urllink)
      videaref=int(0)
      videa=re.compile('src="https://videa.hu/(.+?)"',re.DOTALL|re.M).findall(link)
      if videa:
            for code in videa:
                  golo=findgoal(link,code)
                  if golo: golo=' (%s)' % (golo)
                  titles.append('Videa' + golo)
                  linking.append('https://videa.hu/' + code)
      vkref=int(0)
      vk=re.compile('src="https://vk.com/(.+?)"',re.DOTALL|re.M).findall(link)
      if vk:
          for code in vk:
                golo=findgoal(link,code)
                if golo: golo=' (%s)' % (golo)
                titles.append('VK' + golo)
                linking.append('https://vk.com/' + code)
      youtuberef=int(0)
      youtube=re.compile('src="https://www.youtube.com/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if not youtube: youtube=re.compile('src="//www.youtube.com/embed/(.+?)"',re.DOTALL|re.M).findall(link)
      if youtube:
        for code in youtube:     
              golo=findgoal(link,code)
              if golo: golo=' (%s)' % (golo)
              titles.append('Youtube' + golo)
              linking.append(code)
      print(linking)
      if len(linking)==0:
            xbmcgui.Dialog().ok(translation(30000), translation(30005))
            index=-1
      elif len(linking)==1: index=0
      else: index = xbmcgui.Dialog().select(translation(30006), titles)
      if index > -1:
             linkchoice=linking[index]
             servidor=titles[index]
             if linkchoice:
                   if re.search('Rutube',servidor):
                         link=open_url('https://rutube.ru/api/play/options/' + linkchoice)
                         try:streamurl=re.compile('"m3u8": "(.+?)"').findall(link)[0]
                         except:streamurl=re.compile('"default": "(.+?)"').findall(link)[0]
                         startvideo(name,streamurl)
                   elif re.search('Aliez',servidor):
                         linkchoice=linkchoice.replace('amp;','')
                         link=open_url(linkchoice)
                         streamurl=re.compile("file.+?'(.+?)'").findall(link)[0]
                         startvideo(name,streamurl)
                   elif re.search('Playwire',servidor):
                         if re.search('configopener',linkchoice):
                               videoid=''.join(linkchoice.split('/')[-1:]).replace('.json','')
                               streamurl=redirect('https://config.playwire.com/videos/v2/%s/player.json'%videoid).replace('player.json','manifest.f4m')
                         else:
                               link=open_url(linkchoice)
                               try:streamurl=re.compile('"src":"(.+?)"').findall(link)[0]
                               except:streamurl=re.compile('"f4m":"(.+?)"').findall(link)[0]
                         if re.search('.f4m',streamurl):
                               titles=[]
                               linking=[]
                               f4m=open_url(streamurl)
                               baseurl=re.compile('<baseURL>(.+?)</baseURL>').findall(f4m)[0]
                               videos=re.compile('url="(.+?)".+?height="(.+?)"').findall(f4m)
                               for urlname,quality in videos:
                                     titles.append(quality + 'p')
                                     linking.append(urlname)
                               if len(linking)==1:index=0
                               else: index = xbmcgui.Dialog().select("Qualidade", titles)
                               if index > -1: streamurl='%s/%s' % (baseurl,linking[index])
                               else: return
                         streamurl=streamurl.replace('rtmp://streaming.playwire.com/','https://cdn.playwire.com/').replace('mp4:','')
                         startvideo(name,streamurl)
                   elif re.search('VK',servidor):
                         linkchoice=linkchoice.replace('amp;','')
                         link=open_url(linkchoice)
                         link=link.replace('\\','')
                         if re.search('No videos found.',link): xbmcgui.Dialog().ok(translation(30000),translation(30007))
                         else:
                               titles=[]
                               linking=[]
                               try:
                                     streamurl=re.compile('"url1080":"(.+?)"').findall(link)[0]
                                     titles.append("1080p")
                                     linking.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url720":"(.+?)"').findall(link)[0]
                                     titles.append("720p")
                                     linking.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url480":"(.+?)"').findall(link)[0]
                                     titles.append("480p")
                                     linking.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url360":"(.+?)"').findall(link)[0]
                                     titles.append("360p")
                                     linking.append(streamurl)
                               except: pass
                               try:
                                     streamurl=re.compile('"url240":"(.+?)"').findall(link)[0]
                                     titles.append("240p")
                                     linking.append(streamurl)
                               except: pass
                               if len(linking)==1:index=0
                               else: index = xbmcgui.Dialog().select(translation(30014), titles)
                               if index > -1:
                                     linkchoice=linking[index]
                                     startvideo(name,linkchoice)
                   elif re.search('Sapo',servidor): startvideo(name,linkchoice)
                   elif re.search('Facebook',servidor):
                         link=open_url(linkchoice)
                         params = re.compile('"params","([\w\%\-\.\\\]+)').findall(link)[0]
                         html = urllib.parse.unquote(params.replace('\u0025', '%')).decode('utf-8')
                         html = html.replace('\\', '')
                         streamurl = re.compile('(?:hd_src|sd_src)\":\"([\w\-\.\_\/\&\=\:\?]+)').findall(html)[0]
                         startvideo(name,streamurl)
                   elif re.search('Kiwi',servidor):
                         link=urllib.parse.unquote(open_url('https://v.kiwi.kz/v2/'+linkchoice))
                         streamurl=re.compile('&url=(.+?)&poster').findall(link)[0]
                         startvideo(name,streamurl)
                   elif re.search('videa',linkchoice):
                         reference=re.compile('flvplayer.swf.+?v=(.+?)"').findall(linkchoice)[0]
                         link=open_url('https://videa.hu/flvplayer_get_video_xml.php?v='+ reference)
                         streamurl=re.compile('<version quality="standard" video_url="(.+?)"').findall(link)[0]
                         startvideo(name,streamurl)
                   elif re.search('Youtube',servidor):
                         streamurl='plugin://plugin.video.youtube/?action=play_video&videoid='+code
                         startvideo(name,streamurl)
                         
                   elif re.search('dailymotion',linkchoice):
                         import urlresolver
                         sources=[]
                         hosted_media = urlresolver.HostedMediaFile(url=linkchoice)
                         sources.append(hosted_media)
                         source = urlresolver.choose_source(sources)
                         if source:
                                     linkchoice=source.resolve()
                                     if linkchoice==False:
                                           xbmcgui.Dialog().ok(translation(30000),translation(30007))
                                           return
                                     else: startvideo(name,linkchoice)

def startvideo(title,url):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(title)
      listitem.setArt({"icon": "DefaultVideo.png", "thumb": thumb})	
      listitem.setInfo("Video", {"Title":title})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      playlist.add(url, listitem)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
      xbmcPlayer = xbmc.Player()
      xbmcPlayer.play(playlist)

def addDir(name,url,mode,iconimage,total,pasta=True):
      u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&thumb="+urllib.parse.quote_plus(iconimage)
      ok=True
      liz = xbmcgui.ListItem(name)
      liz.setArt({"icon": "DefaultFolder.png", "thumb": iconimage})	
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      #liz.setProperty('fanart_image', os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'fanart.jpg'))
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
      return ok

def searching():
      searching=xbmcgui.Dialog().input(translation(30008),autoclose=60000)
      if searching:
            xbmcgui.Dialog().ok(translation(30000), f"{translation(30009)}")
            link=open_url( MainURL + 'search.php?dosearch=yes&search_in_archives=yes&title=' + urllib.parse.quote(searching))
            jogos=re.compile('<div style="font-family:Arial, Helvetica, sans-serif; font-size:12px;"><a href="/(.+?)">([0-9]{4}\.[0-9]{2}\.[0-9]{2})\s*(\([0-9]{2}h[0-9]{2}\))\s*-\s*([A-Za-z ]+?)\s*([0-9]*)\s*-\s*([0-9]*)\s*([A-Za-z ]+?)</a></div>').findall(link)
            for urllink,data,hora,team1,result1,result2,team2 in jogos:
                  addDir('[COLOR orange]%s[/COLOR] [COLOR darkorange]%s[/COLOR][COLOR blue] - [/COLOR][COLOR white]%s[/COLOR] [COLOR yellow]%s - %s[/COLOR] [COLOR white]%s[/COLOR]' % (data,hora,team1,result1,result2,team2),MainURL + urllink,1,os.path.join(art,'proxima.png'),len(jogos),pasta=False)
            if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin("Container.SetViewMode(51)")
      else: sys.exit(0)
                        
def open_url(url):
      link=requests.get(url, headers={'User-Agent':user_agent},verify=False).text
      return link

def redirect(url):
      req = urllib.request.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib.request.urlopen(req)
      gurl=response.geturl()
      return gurl

def clean(text):
      command={'&#193;':'A','&#194;':'A','&#195;':'A','&#199;':'C','&#201;':'E','&#202;':'E','&#205;':'I','&#211;':'O','&#212;':'O','&#213;':'O','&#217;':'U','&#218;':'U','&#224;':'a','&#225;':'a','&#226;':'a','&#227;':'a','&#231;':'c','&#232;':'e','&#233;':'e','&#234;':'e','&#237;':'i','&#243;':'o','&#244;':'o','&#245;':'o','&#249;':'u','&#250;':'u'}
      regex = re.compile("|".join(map(re.escape, list(command.keys()))))
      return regex.sub(lambda mo: command[mo.group(0)], text)

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
      return param

def findgoal(link, code):
      text=link[:link.find(code)]
      golo=text[max([text.rfind('</iframe>'),text.rfind('</script>'),text.rfind('</a>')]):max([text.rfind('<iframe'),text.rfind('<script')])]
      golo=re.sub('<[^<]+?>', '', golo.replace('\n','').replace('&#39;',"'"))
      return golo

def descape(content):
      content = re.sub('&([^;]+);', lambda m: chr(html.entities.name2codepoint[m.group(1)]), content)
      return content.encode('utf-8')

def translation(text):
      return xbmcaddon.Addon().getLocalizedString(text)

params=get_params()
url=None
name=None
mode=None
thumb=None
try: url=urllib.parse.unquote_plus(params["url"])
except: pass
try: name=urllib.parse.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: thumb=urllib.parse.unquote_plus(params["thumb"])
except: pass

if mode==None or url==None or len(url)<1: main_menu()
elif mode==1: capture(name,url)
elif mode==2: request(url)
elif mode==3: leaguelists(url)
elif mode==4: request(MainURL + re.compile('<a href="([^"]+?)">previous weeks archive').findall(open_url(url))[0].replace('amp;',''))
elif mode==5: previousseasons(url)
elif mode==6: searching()
elif mode==7: portugueseleague(url)
elif mode==8: request(url,special=True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
