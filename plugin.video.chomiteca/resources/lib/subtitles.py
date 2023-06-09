import xbmc,os

def getsubtitles(name,lang1=None,lang2=None):
	name = name.split('[/B]')[0].replace('[B]','')[:-4]
	quality = ['bluray','blueray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
	moviequality = []	
	langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}
	for q in quality: 
		if q in name.lower():
			try: moviequality.append(q)
			except: pass
			
	langs = []
	try: langs.append(langDict[lang1])
	except: pass
	try: langs.append(langDict[lang2])
	except: pass
	langs = ','.join(langs)

	import xmlrpc.client
	counterloop = 0
	result = []
	while not result and counterloop <=5 :
		try:
			if counterloop != 0: xbmc.sleep(1000)	
			server = xmlrpc.client.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
			token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
			result = server.SearchSubtitles(token, [{'query': name, 'sublanguageid': langs }])['data']
			result = [i for i in result if i['SubSumCD'] == '1']
		except: pass
		counterloop = counterloop + 1
	
	subtitles = []
	subtitles2 = []	
	for lang in langs.split(','):
		filter = [i for i in result if lang == i['SubLanguageID']]
		if filter == []: continue
		subtitles += [i for i in filter if name.lower() in i['MovieReleaseName'].lower()]
		if subtitles != []:
			try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
			except: pass
			break		
		else:		
			if moviequality != []: 
				for mq in moviequality: subtitles += [i for i in filter if mq in i['MovieReleaseName'].lower()]
			if subtitles != []:				
				try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
				except: pass
				break
			else:
				for q in quality: subtitles2 += [i for i in filter if q in i['MovieReleaseName'].lower()]
				subtitles2 += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]	
				try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
				except: pass
	import zlib, base64
	try:
		if not subtitles: content = [subtitles2[0]["IDSubtitleFile"],]
		else: content = [subtitles[0]["IDSubtitleFile"],]
		content = server.DownloadSubtitles(token, content)
		content = base64.b64decode(content['data'][0]['data'])
		content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

		subtitle = xbmc.translatePath('special://temp/')
		subtitle = os.path.join(subtitle, 'DownloadedSubtitles.%s.srt' % lang)
		file = open(subtitle, 'wb')
		file.write(content)
		file.close()
		return subtitle		
	except: pass
