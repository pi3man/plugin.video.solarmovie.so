### ############################################################################################################
###	#	
### # Project: 			#		SolarMovie.so - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		v0.1.4
### # Description: 	#		http://www.solarmovie.so
###	#	
### ############################################################################################################
### ############################################################################################################
##### Imports #####
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,urlresolver,urllib,urllib2,re,os,sys,htmllib,string,StringIO,logging,random,array,time,datetime,unicodedata,requests
#import zipfile ### Removed because it caused videos to not play. ###
import HTMLParser, htmlentitydefs
try: 		import StorageServer
except: import storageserverdummy as StorageServer
try: 		from t0mm0.common.addon 				import Addon
except: from t0mm0_common_addon 				import Addon
try: 		from t0mm0.common.net 					import Net
except: from t0mm0_common_net 					import Net
try: 		from sqlite3 										import dbapi2 as sqlite; print "Loading sqlite3 as DB engine"
except: from pysqlite2 									import dbapi2 as sqlite; print "Loading pysqlite2 as DB engine"
try: 		from script.module.metahandler 	import metahandlers
except: from metahandler 								import metahandlers
### 
from teh_tools 		import *
from config 			import *
##### /\ ##### Imports #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
__plugin__=ps('__plugin__'); __authors__=ps('__authors__'); __credits__=ps('__credits__'); _addon_id=ps('_addon_id'); _domain_url=ps('_domain_url'); _database_name=ps('_database_name'); _plugin_id=ps('_addon_id')
_database_file=os.path.join(xbmc.translatePath("special://database"),ps('_database_name')+'.db'); 
### 
_addon=Addon(ps('_addon_id'), sys.argv); _plugin=xbmcaddon.Addon(id=ps('_addon_id')) #; _plug=xbmcplugin
addon=_addon
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Paths #####
### # ps('')
_addonPath	=xbmc.translatePath(_plugin.getAddonInfo('path'))
_artPath		=xbmc.translatePath(os.path.join(_addonPath,ps('_addon_path_art')))
_datapath 	=_addon.get_profile(); _artIcon		=_addon.get_icon(); _artFanart	=_addon.get_fanart()
##### /\
##### Important Functions with some dependencies #####
def art(f,fe=ps('default_art_ext')): ### for Making path+filename+ext data for Art Images. ###
	return xbmc.translatePath(os.path.join(_artPath,f+fe))
def addst(r,s=''): ## Get Settings
	return _addon.get_setting(r)
def addpr(r,s=''): ## Get Params
	return _addon.queries.get(r,s)
def cFL(t,c=ps('default_cFL_color')): ### For Coloring Text ###
	return '[COLOR '+c+']'+t+'[/COLOR]'
##### /\
##### Settings #####
_setting={}
_setting['debug-enable']=	_debugging			=tfalse(addst("debug-enable"))
_setting['debug-show']	=	_shoDebugging		=tfalse(addst("debug-show"))
_setting['enableMeta']	=	_enableMeta			=tfalse(addst("enableMeta"))
##### /\
_artSun=art('sun'); _art404=art('404'); GENRES=ps('GENRES'); _default_section_=ps('default_section'); net=Net(); DB=_database_file; BASE_URL=_domain_url;
if (_debugging==True): print 'Addon Path: '+_addonPath
if (_debugging==True): print 'Art Path: '+_artPath
if (_debugging==True): print 'Addon Icon Path: '+_artIcon
if (_debugging==True): print 'Addon Fanart Path: '+_artFanart
### ############################################################################################################
def sunNote(header='',msg='',delay=5000,image=_artSun):
	_addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
### ############################################################################################################
### ############################################################################################################
##### Queries #####
_param={}
_param['mode'],_param['url']=addpr('mode',''),addpr('url',''); _param['pagesource'],_param['pageurl'],_param['pageno'],_param['pagecount']=addpr('pagesource',''),addpr('pageurl',''),addpr('pageno',0),addpr('pagecount',1)
_param['img']=addpr('img',''); _param['fanart']=addpr('fanart',''); _param['thumbnail'],_param['thumbnail'],_param['thumbnail']=addpr('thumbnail',''),addpr('thumbnailshow',''),addpr('thumbnailepisode','')
_param['section']=addpr('section','movies'); _param['title']=addpr('title',''); _param['year']=addpr('year',''); _param['genre']=addpr('genre','')
_param['by']=addpr('by',''); _param['letter']=addpr('letter',''); _param['showtitle']=addpr('showtitle',''); _param['showyear']=addpr('showyear',''); _param['listitem']=addpr('listitem',''); _param['infoLabels']=addpr('infoLabels',''); _param['season']=addpr('season',''); _param['episode']=addpr('episode','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
##_param['pagestart']=addpr('pagestart',0)
##### /\

### ############################################################################################################
### ############################################################################################################
def initDatabase():
	print "Building solarmovie Database"
	if ( not os.path.isdir( os.path.dirname(_database_file) ) ): os.makedirs( os.path.dirname( _database_file ) )
	db = sqlite.connect( _database_file )
	cursor = db.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS seasons (season UNIQUE, contents);')
	cursor.execute('CREATE TABLE IF NOT EXISTS favorites (type, name, url, img);')
	db.commit()
	db.close()

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Player Functions #####
def PlayVideo(url, infoLabels, listitem):
	WhereAmI('@ PlayVideo -- Getting ID From:  %s' % url)
	My_infoLabels=eval(infoLabels)
	#My_infoLabels={ "Title": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
	infoLabels={ "Studio": My_infoLabels['Studio'], "ShowTitle": My_infoLabels['ShowTitle'], "Title": My_infoLabels['Title'], "Year": My_infoLabels['Year'], "Plot": My_infoLabels['Plot'], 'IMDbURL': My_infoLabels['IMDbURL'], 'IMDbID': My_infoLabels['IMDbID'], 'IMDb': My_infoLabels['IMDb'] }
	li=xbmcgui.ListItem(_param['title'], iconImage=_param['img'], thumbnailImage=_param['img'])
	match=re.search( '/.+?/.+?/(.+?)/', url) ## Example: http://www.solarmovie.so/link/show/1052387/ ##
	videoId=match.group(1); deb('Solar ID',videoId)
	url=BASE_URL + '/link/play/' + videoId + '/' ## Example: http://www.solarmovie.so/link/play/1052387/ ##
	html=net.http_GET(url).content
	match=re.search( '<iframe.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
	link=match.group(1); link=link.replace('/embed/', '/file/'); deb('hoster link',link)
	#if (_debugging==True): print listitem
	#if (_debugging==True): print infoLabels
	##xbmc.Player( xbmc.PLAYER_CORE_PAPLAYER ).play(stream_url, li)
	##infoLabels.append('url': stream_url)
	li.setInfo(type="Video", infoLabels=infoLabels )
	li.setProperty('IsPlayable', 'true')
	##if (urlresolver.HostedMediaFile(link).valid_url()):
	##else: 
	### _addon.resolve_url(link)
	### _addon.resolve_url(stream_url)
	try: stream_url = urlresolver.HostedMediaFile(link).resolve()
	except: 
		if (_debugging==True): print 'Link URL Was Not Resolved: '+link
		notification("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL.")
		return
	_addon.end_of_directory()
	#xbmc.Player().stop()
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	play.play(stream_url, li)
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
	#xbmc.sleep(7000)

def PlayTrailer(url):
	sources=[]; url=url.decode('base-64'); WhereAmI('@ PlayVideo:  %s' % url)
	try: 
		hosted_media=urlresolver.HostedMediaFile(url=url)
		sources.append(hosted_media)
		source=urlresolver.choose_source(sources)
		if (source): stream_url=source.resolve()
	except:
		deb('Stream failed to resolve',url); return
	else: stream_url = ''
	try: xbmc.Player().play(stream_url)
	except: 
		deb('Video failed to play',stream_url); return

##### /\
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Weird, Stupid, or Plain up Annoying Functions. #####
def netURL(url): ### Doesn't seem to work.
	return net.http_GET(url).content
def remove_accents(input_str): ### Not even sure rather this one works or not.
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

##### /\
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Menus #####
def mGetItemPage(url):
	deb('Fetching html from Url',url)
	try: html=net.http_GET(url).content
	except: html=''
	if (html=='') or (html=='none') or (html==None) or (html==False): return ''
	else:
		html=HTMLParser.HTMLParser().unescape(html)
		html=ParseDescription(html)
		html=html.encode('ascii', 'ignore')
		html=html.decode('iso-8859-1')
		html=_addon.decode(html); html=_addon.unescape(html)
		deb('Length of HTML fetched',str(len(html)))
	return html

def mGetDataTest(html,toGet):
	resultCnt=0; results={} #results=[]
	debob(toGet)
	for item in toGet:
		item=item.lower();parseMethod=''; parseTag=''; parseTag2=''; parseTag3=''; rCheck=False
		parseTag='<p id="plot_\d+">(.+?)</p>'
		results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		return results

def mGetDataPlot(html,parseTag='<p id=\"plot_\d+\">(.+?)</p>'):
	if ('<p id="plot_' in html):
		try: return (re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		except: return ''
	else: return ''

def mGetData(html,toGet):
	#if (html=='') or (html=='none') or (html==None) or (html==False): 
	#	deb('mGetData','html is empty')
	#	return None
	resultCnt=0; results={} #results=[]
	debob(toGet)
	for item in toGet:
		item=item.lower();parseMethod=''; parseTag=''; parseTag2=''; parseTag3=''; rCheck=False
		if (item=='plot') or (item=='movieplot') or (item=='showplot'): ### 
			parseTag='<p id=\"plot_\d+\">(.+?)</p>'
			parseMethod='re.compile'
			if ('<p id="plot_' in html): 
				rCheck=True
				print "found: '<p id=\"plot_'"
			#rCheck=True
		##if (item=='description'): ### 
		##	parseTag='<p id="plot_\d+">(.+?)</p>'
		##	parseMethod='re.compile'
		##	if ('<p id="plot_' in html): rCheck=True
		##	#<meta name="description" content="Watch full The Heat movie produced in 2013. Genres are Comedy, Crime, Action." />
		#elif (item=='latestepisodeplot'): ### 
		#	parseTag='<p id="plot_\d+">(.+?)</p>'
		#	parseMethod='re.compile2'
		#	if ('<p id="plot_' in html): rCheck=True
		#elif (item=='imdbid'): ### 0816711
		#	parseTag='<strong>IMDb ID:</strong>[\n]\s+<a href=".+?">(\d+)</a>'
		#	parseMethod='re.compile'
		#	if ('<strong>IMDb ID:</strong>' in html): rCheck=True
		#elif (item=='imdburl'): ### http://anonym.to/?http%3A%2F%2Fwww.imdb.com%2Ftitle%2Ftt0816711%2F
		#	parseTag='<strong>IMDb ID:</strong>[\n]\s+<a href="(.+?)">\d+</a>'
		#	parseMethod='re.compile'
		#	if ('<strong>IMDb ID:</strong>' in html): rCheck=True
		#elif (item=='imdrating'): ### 7.3
		#	parseTag='<strong>IMDb rating:</strong>[\n]\s+(.+?)\s+\(.+? votes\)'
		#	parseMethod='re.compile'
		#	if ('<strong>IMDb rating:</strong>' in html): rCheck=True
		#elif (item=='imdvotes'): ### 2,814
		#	parseTag='<strong>IMDb rating:</strong>[\n].+?\((.+?) votes\)'
		#	parseMethod='re.compile'
		#	if ('<strong>IMDb rating:</strong>' in html): rCheck=True
		#elif (item=='duration'): ### 116 min
		#	parseTag='<strong>Duration:</strong>[\n]\s+(.+?)<'
		#	parseMethod='re.compile'
		#	if ('<strong>Duration:</strong>' in html): rCheck=True
		#elif (item=='duration2'):
		#	parseTag='<strong>Duration:</strong>'
		#	parseTag2='<'
		#	parseMethod='strip'
		#	if ('<strong>Duration:</strong>' in html): rCheck=True
		#elif (item=='reelasedate'): ### June 21, 2013
		#	parseTag='<strong>Release Date:</strong>[\n]\s+(.+?)\s+[\n]\s+</div>'
		#	parseMethod='re.compile'
		#	if ('<strong>Release Date:</strong>' in html): rCheck=True
		#elif (item=='reelasedate2'):
		#	parseTag='<strong>Release Date:</strong>'
		#	parseTag2='<'
		#	parseMethod='strip'
		#	if ('<strong>Release Date:</strong>' in html): rCheck=True
		#elif (item=='Votes'): ### 86
		#	parseTag='<strong>Solar rating:</strong>[\n]\s+<span class="js-votes"[\n]\s+>(\d+\s+votes</span>'
		#	parseMethod='re.compile'
		#	if ('<strong>Solar rating:</strong>' in html) and ('<span class="js-votes"' in html) and ('votes</span>' in html): rCheck=True
		#elif (item=='coverimage'): ### http://static.solarmovie.so/images/movies/0460681_150x220.jpg
		#	parseTag='coverImage">.+?src="(.+?)"'
		#	parseMethod='re.search'
		#	if ('coverImage">' in html): rCheck=True
		#elif (item=='season'): ### 
		#	parseTag="toggleSeason\('(\d+)'\)"
		#	parseMethod='re.search'
		#	if ('toggleSeason' in html): rCheck=True
		#elif (item=='seasons'): ### 
		#	parseTag="toggleSeason\('(\d+)'\)"
		#	parseMethod='re.search.group'
		#	if ('toggleSeason' in html): rCheck=True
		#elif (item=='episode'): ### 
		#	parseTag='<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>'
		#	parseMethod='re.compile'
		#	if ('<span class="epname">' in html) and (' links</a>' in html): rCheck=True
		#elif (item=='episodes'): ### 
		#	parseTag='<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>'
		#	parseMethod='re.compile.group'
		#	##episodes=re.compile('<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>', re.IGNORECASE | re.MULTILINE | re.DOTALL).findall(html) #; if (_debugging==True): print episodes
		#	##for ep_url, episode_name, season_number, episode_number, num_links in episodes:
		#	if ('<span class="epname">' in html): rCheck=True
		else: rCheck=False
		#
		### Year
		#
		#                    Fantasy</a>                                    produced in
		#        <a href="/tv/watch-tv-shows-2005.html">
		#                2005</a>
		#
		### Country
		#                    [<a href="/tv/tv-shows-from-usa.html">USA</a>]
		#
		### Latest Episode
		#            <div class="mediaDescription latestTvEpisode">
		#
		#        <h5>Latest Episode:
		#            <a href="/tv/supernatural-2005/season-8/episode-23/">
		#                Sacrifice                (<span>s08e23</span>)</a>
		#              <em class="releaseDate">May 15, 2013</em>
		#        </h5>
		#
		#<p id="plot_476403">Sam and Dean capture Crowley to finish the trials and close the gates of Hell. Castiel and Metatron continue the trials to close the gates of Heaven. Sam is left with a huge decision.</p>
		#                        </div>
		### Genres
		#<meta name="description" content="Watch full The Heat movie produced in 2013. Genres are Comedy, Crime, Action." />
		#
		#
		#
		#
		#
		#
		#
		#
		if (rCheck==True):
			if (parseMethod=='re.compile2'): ## returns 2nd result
				#results.append((re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[1]).strip()); resultCnt=resultCnt+1
				results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[1]).strip()
				resultCnt=resultCnt+1
			if (parseMethod=='re.compile'): ## returns 1st result
				#results.append((re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()); resultCnt=resultCnt+1
				#results[item]=(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0].strip()
				resultCnt=resultCnt+1
			if (parseMethod=='re.compile.group'): ## returns a group of results
				results.append(re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)); resultCnt=resultCnt+1
				results[item]=re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html); resultCnt=resultCnt+1
			if (parseMethod=='split'):
				results.append((((html.split(parseTag)[1])).split(parseTag2)[0]).strip()); resultCnt=resultCnt+1
				results[item]=(((html.split(parseTag)[1])).split(parseTag2)[0]).strip(); resultCnt=resultCnt+1
			if (parseMethod=='re.search2'): ## returns 2nd result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results.append(match.group(2)); resultCnt=resultCnt+1
				results[item]=match.group(2); resultCnt=resultCnt+1
			if (parseMethod=='re.search'): ## returns 1st result
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results.append(match.group(1)); resultCnt=resultCnt+1
				results[item]=match.group(1); resultCnt=resultCnt+1
			if (parseMethod=='re.search.group'): ## returns a group of results
				match=re.search(parseTag, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
				results.append(match.group()); resultCnt=resultCnt+1
				results[item]=match.group(); resultCnt=resultCnt+1
				#results.append(match); resultCnt=resultCnt+1  ## Not sure which one to use yet. ##
				#results[item]=match; resultCnt=resultCnt+1  ## Not sure which one to use yet. ##
			else: 
				results[item]=None; resultCnt=resultCnt+1
		else: 
			results[item]=None; resultCnt=resultCnt+1
		#
		#
		#elif (parseMethod==''):
		#elif (parseMethod==''):
		#
	if debugging==True: print results
	return results
	#

def listLinks(section, url, showtitle='', showyear=''): ### Menu for Listing Hosters (Host Sites of the actual Videos)
	WhereAmI('@ the Link List: %s' % url); sources=[]; listitem=xbmcgui.ListItem()
	if (url==''): return
	html=net.http_GET(url).content
	html=html.encode("ascii", "ignore")
	#if (_debugging==True): print html
	if  ( section == 'tv'): ## TV Show
		match=re.compile('<title>Watch (.+?) Online for Free - (.+?) - .+? - (\d+)x(\d+) - SolarMovie</title>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		### <title>Watch The Walking Dead Online for Free - Prey - S03E14 - 3x14 - SolarMovie</title>
		if (_debugging==True): print match
		if (match==None): return
		#ShowYear=showyear
		ShowYear=_param['year']
		ShowTitle=match[0].strip(); EpisodeTitle=match[1].strip(); Season=match[2].strip(); Episode=match[3].strip()
		ShowTitle=HTMLParser.HTMLParser().unescape(ShowTitle); ShowTitle=ParseDescription(ShowTitle); ShowTitle=ShowTitle.encode('ascii', 'ignore'); ShowTitle=ShowTitle.decode('iso-8859-1')
		EpisodeTitle=HTMLParser.HTMLParser().unescape(EpisodeTitle); EpisodeTitle=ParseDescription(EpisodeTitle); EpisodeTitle=EpisodeTitle.encode('ascii', 'ignore'); EpisodeTitle=EpisodeTitle.decode('iso-8859-1')
		if ('<p id="plot_' in html):
			ShowPlot=(re.compile('<p id="plot_\d+">(.+?)</p>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
			ShowPlot=HTMLParser.HTMLParser().unescape(ShowPlot); ShowPlot=ParseDescription(ShowPlot); ShowPlot=ShowPlot.encode('ascii', 'ignore'); ShowPlot=ShowPlot.decode('iso-8859-1')
		else: ShowPlot=''
		match=re.compile('<strong>IMDb ID:</strong>[\n]\s+<a href="(.+?)">(\d+)</a>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		(IMDbURL,IMDbID)=match
		IMDbURL=IMDbURL.strip(); IMDbID=IMDbID.strip()
		#
		My_infoLabels={ "Studio": ShowTitle+'  ('+ShowYear+'):  '+Season+'x'+Episode+' - '+EpisodeTitle, "Title": ShowTitle, "ShowTitle": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'Season': Season, 'Episode': Episode, 'EpisodeTitle': EpisodeTitle, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
		listitem.setInfo(type="Video", infoLabels=My_infoLabels )
		#
		#
		#match=re.search('bradcramp.+?href=".+?>(.+?)<.+?href=".+?>        Season (.+?) .+?[&nbsp;]+Episode (.+?)<', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		#if (_debugging==True): print match
		#if (match==None): return
		#listitem.setInfo('video', {'TVShowTitle': match.group(1), 'Season': int(match.group(2)), 'Episode': int(match.group(3)) } )
	else:	#################### Movie
		#match=re.search('float:left;">(.+?)<em.+?html">[\n]*(.+?)</a>', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		#<title>Watch Full The Dark Knight (2008)  Movie Online - Page 1 - SolarMovie</title>
		#match=re.search('<title>Watch Full (.+?) \((.+?)\) .+?</title>', html, re.MULTILINE | re.IGNORECASE | re.DOTALL)
		match=re.compile('<title>Watch Full (.+?) \((.+?)\) .+?</title>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		if (match==None): return
		ShowYear=match[1].strip(); ShowTitle=match[0].strip()
		ShowTitle=HTMLParser.HTMLParser().unescape(ShowTitle); ShowTitle=ParseDescription(ShowTitle); ShowTitle=ShowTitle.encode('ascii', 'ignore'); ShowTitle=ShowTitle.decode('iso-8859-1')
		#
		ShowPlot=(re.compile('<p id="plot_\d+">(.+?)</p>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]).strip()
		ShowPlot=HTMLParser.HTMLParser().unescape(ShowPlot); ShowPlot=ParseDescription(ShowPlot); ShowPlot=ShowPlot.encode('ascii', 'ignore'); ShowPlot=ShowPlot.decode('iso-8859-1')
		#
		match=re.compile('<strong>IMDb ID:</strong>[\n]\s+<a href="(.+?)">(\d+)</a>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)[0]
		if (_debugging==True): print match
		(IMDbURL,IMDbID)=match
		IMDbURL=IMDbURL.strip(); IMDbID=IMDbID.strip()
		#
		My_infoLabels={ "Studio": ShowTitle+'  ('+ShowYear+')', "Title": ShowTitle, "ShowTitle": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
		##liz.setInfo( type="Video", infoLabels={ "Title": showtitle, "Studio": Studio } )
		listitem.setInfo(type="Video", infoLabels=My_infoLabels )
		#listitem.setInfo('video', {'Title': match.group(1).strip(), 'Year': int(match.group(2).strip())} )
	#
	match =  re.compile('<tr id=.+?href="(.+?)">(.+?)<.+?class="qualityCell">(.+?)<.+?<td class="ageCell .+?">(.+?)</td>', re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(html)
	#match =  re.compile('<tr id=.+?href="(.+?)">(.+?)<.+?class="qualityCell">(.+?)<', re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(html)
	### print ' length of match is %d' % len(match)
	if (len(match) > 0):
		count=1
		for url, host, quality, age in match:
			host=host.strip(); quality=quality.strip(); name=str(count)+". "+host+' - [[B]'+quality+'[/B]] - ([I]'+age+'[/I])'
			if urlresolver.HostedMediaFile(host=host, media_id='xxx'):
				img='http://www.google.com/s2/favicons?domain='+host
				My_infoLabels['quality']=quality
				My_infoLabels['age']=age
				My_infoLabels['host']=host
				#_addon.add_item(url,{'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  name})
				_addon.add_directory({'section': section, 'img': _param['img'], 'mode': 'PlayVideo', 'url': url, 'quality': quality, 'age': age, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img, is_folder=False)
				#_addon.add_item({'mode': 'PlayVideo', 'url': url, 'quality': quality, 'age': age, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img, is_folder=False)
				#_addon.add_video_item({'mode': 'PlayVideo', 'url': url, 'quality': quality, 'age': age, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img)
				##_addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  name})
				count=count+1 
		_addon.end_of_directory()
	else:
		return

def Menu_BrowseByGenre(section=_default_section_):
	url=''; WhereAmI('@ the Genre Menu')#print 'Browse by genres screen'
	for genre in GENRES:
		if section == 'movies': url=_domain_url+'/watch-'   +(genre.lower())+  '-movies.html'
		else: 									url=_domain_url+'/tv/watch-'+(genre.lower())+'-tv-shows.html'
		_addon.add_directory({'section': section,'mode': 'GetTitles','url': url,'genre': genre,'pageno': '1','pagecount': '3'}, {'title':  genre})
	_addon.end_of_directory()

def Menu_BrowseByYear(section=_default_section_):
	url=''; WhereAmI('@ the Year Menu'); EarliestYear=1929 #1930 ### This is set to 1 year earlier so that it will display too ### 
	try: thisyear=int(datetime.date.today().strftime("%Y"))
	except: thisyear=2013
	for year in range(thisyear, EarliestYear, -1):
		if section == 'movies': url=_domain_url+   '/watch-movies-of-'+str(year)+'.html'
		else: 									url=_domain_url+'/tv/watch-tv-shows-' +str(year)+'.html'
		_addon.add_directory({'section': section,'mode': 'GetTitles', 'url': url,'year': year,'pageno': '1','pagecount': '3'}, {'title':  str(year)})
	_addon.end_of_directory()

##def listItems(section=_default_section_, url='', html='', episode=False, startPage='1', numOfPages='1', genre='', year='', stitle=''): # List: Movies or TV Shows
def listItems(section=_default_section_, url='', startPage='1', numOfPages='1', genre='', year='', stitle='', season='', episode='', html='', chck=''): # List: Movies or TV Shows
	if (url==''): return
	#if (chck=='Latest'): url=url+chr(35)+'latest'
	WhereAmI('@ the Item List -- url: %s' % url)
	last=2; start=int(startPage); end=(start+int(numOfPages)); html=''; html_last=''; nextpage=startPage
	try: html_=net.http_GET(url).content
	except: 
		try: html_=getURL(url)
		except: 
			try: html_=getURLr(url,_domain_url)
			except: html_=''
	#print html_
	if (html_=='') or (html_=='none') or (html_==None): return
	pmatch=re.findall('<li><a href=.+?page=([\d]+)"', html_)
	if pmatch: last=pmatch[-1]
	for page in range(start,min(last,end)):
		if (int(startPage)> 1): pageUrl=url+'?page='+startPage
		else: pageUrl=url
		try: 
			try: html_last=net.http_GET(pageUrl).content
			except: 
				try: html_=getURL(url)
				except: t=''
			if (_shoDebugging==True) and (html_last==''): notification('Testing','html_last is empty')
			if (html_last in html): t=''
			else: html=html+'\r\n'+html_last
			##if (_debugging==True): print html_last
		except: t=''
	if ('<li class="next"><a href="http://www.solarmovie.so/' in html_last): 
		if (_debugging==True): print 'A next-page has been found.'
		nextpage=re.findall('<li class="next"><a href=.+?page=([\d]+)"', html_last)[0] #nextpage=re.compile('<li class="next"><a href="http://www.solarmovie.so/.+?.html?page=(\d+)"></a></li>').findall(html_last)[0]
		if (int(nextpage) > end) or (end < last): ## Do Show Next Page Link ##
			if (_debugging==True): print 'A next-page is being added.'
			_addon.add_directory({'mode': 'GetTitles', 'url': url, 'pageno': nextpage, 'pagecount': numOfPages}, {'title': '  >  Next...'}, img=art('icon-next'))
	##	### _addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': 'Next...'})
	##html=nolines(html)
	html=ParseDescription(html); html=remove_accents(html) #if (_debugging==True): print html
	if   (section=='tv') and (season=='') and (episode==''): ## TV Show
		deb('listItems >> ',section); deb('listItems >> chck',chck)
		if   (chck=='NewPopular'): 		html=(html.split('<h2>Most Popular New TV Shows</h2>')[1]).split('<h3>')[0]
		elif (chck=='Popular'): 			html=(html.split('<h2>Most Popular TV Shows</h2>')[1]).split('<h2>')[0]
		elif (chck=='Latest'): 				html=(html.split('<h2>Latest TV Shows</h2>')[1]).split('<h3>')[0]
		iitems=re.compile('class="coverImage" title="(.+?)".+?href="(.+?)".+?src="(.+?)".+?<a title=".+?\(([\d]+)\)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		for name, item_url, thumbnail, year in iitems:
			contextMenuItems=[]; name=ParseDescription(HTMLParser.HTMLParser().unescape(name)); name=name.encode('ascii', 'ignore'); name=name.decode('iso-8859-1'); name=name.strip() #; name = remove_accents(name)
			name=_addon.decode(name); name=_addon.unescape(name)
			try: deb('listItems >> '+section+' >> '+name, item_url)
			except: print item_url
			##### Right Click Menu for: TV #####
			contextMenuItems.append(('Show Information', 			'XBMC.Action(Info)'))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
				contextMenuItems.append(('Search 1Channel', 			'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.1channel/', 'tv-shows', name)))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.primewire'):
				contextMenuItems.append(('Search PrimeWire.ag', 	'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.primewire/', 'tv-shows', name)))
			contextMenuItems.append(('Find AirDates', 			'XBMC.RunPlugin(%s?mode=%s&title=%s)' % (sys.argv[0],'SearchForAirDates', urllib.quote_plus(name))))
			##### Right Click Menu for: TV ##### /\ #####
			if (chck=='Latest'):
				showTitle, season_number, episode_number, episode_name = re.compile('__(.+?) s(\d+)e(\d+) (.+?)__', re.IGNORECASE | re.DOTALL).findall('__'+name+'__')[0] #Unsealed: Conspiracy Files s01e14 Fake World Leaders
				showTitle=showTitle.strip()
				season_number=season_number.strip()
				episode_number=episode_number.strip()
				episode_name=episode_name.strip()
				if (_debugging==True): deb('name',name); deb('year',year)
				try: _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': showTitle, 'year': year, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name }, {'title':  showTitle+'  ('+year+')  '+season_number+'x'+episode_number+' - '+episode_name}, img=thumbnail, contextmenu_items=contextMenuItems)
				except: 
					uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
			else:
				if (_enableMeta==True): ### Doesn't work currently. ###
					metaget=metahandlers.MetaData()
					meta=metaget.get_meta('tvshow', name, year=year)
					if (meta['imdb_id']=='') and (meta['tvdb_id']==''):
						meta=metaget.get_meta('tvshow', name)
						#try: 
						_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': meta['cover_url'], 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=meta['cover_url'], fanart=meta['backdrop_url'], contextmenu_items=contextMenuItems)
						#except: 
						#	uname=name; name='[Unknown]'
						#	try: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': meta['cover_url'], 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=meta['cover_url'], fanart=meta['backdrop_url'], contextmenu_items=contextMenuItems)
						#	except: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail)
					else:
						#try: 
						_addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
						#except: 
						#	uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail)
				else: ### Display without MetaData. ###
					try: _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
					except: 
						uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetSeasons', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
		if (chck=='Latest'): 		set_view('tvshows',515,True)
		else: 										set_view('episodes',515,True)
		_addon.end_of_directory(); return
	elif (section=='tv') and (episode==''): ## Season
		set_view('seasons',515); _addon.end_of_directory(); return
	elif (section=='tv'): ## Episode
		set_view('episodes',515); _addon.end_of_directory(); return
	elif (section=='movies') or (section=='movie'): ## Movie
		deb('listItems >> ',section); deb('listItems >> chck',chck)
		##set_view('movies',515)
		####xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
		##xbmc.executebuiltin("Container.SetSortMethod(%s)" % xbmcplugin.SORT_METHOD_LABEL)
		if   (chck=='NewPopular'): 		html=(html.split('<h2>Most Popular New Movies</h2>')[1]).split('<h2>')[0]
		elif (chck=='HDPopular'): 		html=(html.split('<h2>Most Popular Movies in HD</h2>')[1]).split('<h2>')[0]
		elif (chck=='OtherPopular'): 	html=(html.split('<h2>Other Popular Movies</h2>')[1]).split('<h2>')[0]
		elif (chck=='Latest'): 				html=(html.split('<h2>Latest Movies</h2>')[1]).split('<h2>')[0]
		#elif (chck=='Popular'): ## I guess this isnt used for movies atm.
		iitems=re.compile('class="coverImage" title="(.+?)".+?href="(.+?)".+?src="(.+?)".+?<a title=".+?\(([\d]+)\)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		for name, item_url, thumbnail, year in iitems:
			contextMenuItems=[]; name=ParseDescription(HTMLParser.HTMLParser().unescape(name)); name=name.encode('ascii', 'ignore'); name=name.decode('iso-8859-1') #; name = remove_accents(name)
			name=_addon.decode(name); name=_addon.unescape(name)
			try: deb('listItems >> '+section+' >> '+name, item_url)
			except: print item_url
			##### Right Click Menu for: MOVIE #####
			contextMenuItems.append(('Show Information', 			'XBMC.Action(Info)'))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
				contextMenuItems.append(('Search 1Channel', 			'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.1channel/', 'movies', name)))
			if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.primewire'):
				contextMenuItems.append(('Search PrimeWire.ag', 	'XBMC.Container.Update(%s?mode=7000&section=%s&query=%s)' % ('plugin://plugin.video.primewire/', 'movies', name)))
			##### Right Click Menu for: MOVIE ##### /\ #####
			#
			#
			ihtml=mGetItemPage(_domain_url+item_url)
			##debob(ihtml)
			##plot=mGetData(ihtml,['plot'])['plot']
			##plot=mGetDataTest(ihtml,['plot'])['plot']
			plot=mGetDataPlot(ihtml)
			if (plot==None) or (plot=='none') or (plot==False): plot=''
			#
			#
			#
			try: _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')', 'plot': plot}, img=thumbnail, contextmenu_items=contextMenuItems)
			except: 
				uname=name; name='[Unknown]'; _addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': _domain_url + item_url, 'img': thumbnail, 'title': name, 'year': year }, {'title':  name+'  ('+year+')'}, img=thumbnail, contextmenu_items=contextMenuItems)
		set_view('movies',515); _addon.end_of_directory()
		#
		#
		#
		#
		#
		return
	else: return
	#
	#
	#thumbnail='http://static.solarmovie.so/images/'+(img)+'.jpg'
	#re.compile('(.+?)').findall(link)
	#<li class="next"><a href="http://www.solarmovie.so/watch-action-movies.html?page=2"></a></li>
	#
	#
	#
	#
	#
	_addon.end_of_directory()
	
def listEpisodes(section, url, img='', season=''): #_param['img']
	xbmcplugin.setContent( int( sys.argv[1] ), 'episodes' )
	WhereAmI('@ the Episodes List for TV Show -- url: %s' % url)
	html = net.http_GET(url).content
	if (html=='') or (html=='none') or (html==None):
		if (_debugging==True): print 'Html is empty.'
		return
	if (img==''):
		match=re.search( 'coverImage">.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
		img=match.group(1)
	episodes=re.compile('<span class="epname">[\n].+?<a href="(.+?)"[\n]\s+title=".+?">(.+?)</a>[\n]\s+<a href="/.+?/season-(\d+)/episode-(\d+)/" class=".+?">[\n]\s+(\d+) links</a>', re.IGNORECASE | re.MULTILINE | re.DOTALL).findall(html) #; if (_debugging==True): print episodes
	if not episodes: 
		if (_debugging==True): print 'couldn\'t find episodes'
		return
	for ep_url, episode_name, season_number, episode_number, num_links in episodes:
		if (int(episode_number) > -1) and (int(episode_number) < 10): episode_number='0'+episode_number
		ep_url=_domain_url+ep_url
		episode_name=ParseDescription(HTMLParser.HTMLParser().unescape(episode_name))
		episode_name=episode_name.encode('ascii', 'ignore')
		episode_name=episode_name.decode('iso-8859-1')
		episode_name=episode_name.replace( '_',' ')
		episode_name=_addon.decode(episode_name); episode_name=_addon.unescape(episode_name)
		if (season==season_number) or (season==''): _addon.add_directory({'mode': 'GetLinks', 'year': _param['year'], 'section': section, 'img': img, 'url': ep_url, 'season': season_number, 'episode': episode_number, 'episodetitle': episode_name}, {'title':  season_number+'x'+episode_number+' - '+episode_name+'  [[I]'+num_links+' Links [/I]]'}, img= img)
	set_view('episodes',515); _addon.end_of_directory()

def listSeasons(section, url, img=''): #_param['img']
	xbmcplugin.setContent( int( sys.argv[1] ), 'seasons' )
	WhereAmI('@ the Seasons List for TV Show -- url: %s' % url)
	html = net.http_GET(url).content
	if (html=='') or (html=='none') or (html==None):
		if (_debugging==True): print 'Html is empty.'
		return
	if (img==''):
		match=re.search( 'coverImage">.+?src="(.+?)"', html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
		img=match.group(1)
	##if (_debugging==True): print ParseDescription(html)
	seasons=re.compile("toggleSeason\('(\d+)'\)").findall(html)
	if (_debugging==True): print seasons
	if not seasons: 
		if (_debugging==True): print 'couldn\'t find seasons'
		return
	for season_name in seasons:
		season_name=_addon.decode(season_name); season_name=_addon.unescape(season_name)
		season_name=season_name.replace( '_',  ' '); _addon.add_directory({'mode': 'GetEpisodes', 'year': _param['year'], 'section': section, 'img': img, 'url': url, 'season': season_name}, {'title':  'Season '+season_name}, img= img)
	set_view('seasons',515); _addon.end_of_directory()


def Menu_LoadCategories(section=_default_section_): #Categories
	WhereAmI('@ the Category Menu')
	if  ( section == 'tv'): ## TV Show
		##_addon.add_directory({'section': section, 'mode': 'BrowseLatest'},	 		{'title':  'Latest'})
		##_addon.add_directory({'section': section, 'mode': 'BrowsePopular'}, 		{'title':  'Popular'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 	{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Popular (ALL TIME)'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesNewPopular', 'url': _domain_url+'/tv/', 'pageno': '1','pagecount': '1'}, 	{'title':  'Popular (NEW)'})
	else:	#################### Movie
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/#latest', 'pageno': '1','pagecount': '1'},	 		{'title':  'Latest'})
		##_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/#popular', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (ALL TIME)'})
		#_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 		{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesLatest', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 	{'title':  'Latest'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesNewPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 	{'title':  'Popular (NEW)'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesHDPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (HD)'})
		_addon.add_directory({'section': section, 'mode': 'GetTitlesOtherPopular', 'url': _domain_url+'/', 'pageno': '1','pagecount': '1'}, 			{'title':  'Popular (OTHER)'})
	_addon.add_directory({'section': section, 'mode': 'BrowseGenre'},	 			{'title':  'Genres'})
	_addon.add_directory({'section': section, 'mode': 'BrowseYear'}, 				{'title':  'Year'})
	###_addon.add_directory({'section': section, 'mode': 'BrowseAtoZ'}, 			{'title':  'A-Z'})
	#_addon.add_directory({'section': section, 'mode': 'GetSearchQuery'}, 		{'title':  'Search'})
	###_addon.add_directory({'section': section, 'mode': 'GetTitles'}, 				{'title':  'Favorites'})
	_addon.end_of_directory()
	### http://www.solarmovie.so/latest-movies.html
	### 
	### 
	### 
	### 

def Menu_MainMenu(): #The Main Menu
	WhereAmI('@ the Main Menu')
	_addon.add_directory({'mode': 'LoadCategories', 'section': 'movies'}, {'title':  cFL('M')+'ovies'},img=art('movies'))
	_addon.add_directory({'mode': 'LoadCategories', 'section': 'tv'}, 		{'title':  cFL('T')+'V Shows'},img=art('television'))
	_addon.add_directory({'mode': 'ResolverSettings'}, {'title':  cFL('R')+'esolver Settings'},is_folder=False)
	_addon.add_directory({'mode': 'Settings'}, 				 {'title':  cFL('S')+'ettings'},img=_artSun,is_folder=False)
	_addon.add_directory({'mode': 'TextBoxFile', 'title': "[COLOR cornflowerblue]Local Change Log:[/COLOR]  %s"  % (__plugin__), 'url': 'changelog.txt'}, 				 																																 {'title': cFL('L')+'ocal Change Log'},					img=_artSun,is_folder=False)
	_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest Change Log:[/COLOR]  %s" % (__plugin__), 'url': 'https://raw.github.com/HIGHWAY99/plugin.video.solarmovie.so/master/changelog.txt'}, 		 {'title': cFL('L')+'atest Online Change Log'},	img=_artSun,is_folder=False)
	_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest News:[/COLOR]  %s"       % (__plugin__), 'url': 'https://raw.github.com/HIGHWAY99/plugin.video.solarmovie.so/master/news.txt'}, 				 {'title': cFL('L')+'atest Online News'},				img=_art404,is_folder=False)
	#
	#
	#
	### ############
	_addon.end_of_directory()
	### ############
	#_addon.show_countdown(9000,'Testing','Working...') ### Time seems to be in seconds.
	#_addon.show_small_popup('Testing','Working...',image=_artSun)
	#sunNote('Test','Working...')
	#

##### /\ ##### Menus #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Modes #####
def check_mode(mode=''):
	deb('Mode',mode)
	if (mode=='') or (mode=='main') or (mode=='MainMenu'): 
		initDatabase()
		Menu_MainMenu()
	elif (mode=='ResolverSettings'): urlresolver.display_settings()
	elif (mode=='Settings'): _addon.addon.openSettings() #_plugin.openSettings()
	elif (mode=='PlayVideo'): PlayVideo(_param['url'], _param['infoLabels'], _param['listitem'])
	elif (mode=='LoadCategories'): Menu_LoadCategories(_param['section'])
	#elif (mode=='BrowseAtoZ'): BrowseAtoZ(_param['section'])
	elif (mode=='BrowseYear'): Menu_BrowseByYear(_param['section'])
	elif (mode=='BrowseGenre'): Menu_BrowseByGenre(_param['section'])
	#elif (mode=='BrowseLatest'): BrowseLatest(_param['section'])
	#elif (mode=='BrowsePopular'): BrowsePopular(_param['section'])
	#elif (mode=='GetResults'): GetResults(_param['section'], genre, letter, page)
	elif (mode=='GetTitles'): 						listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'])
	elif (mode=='GetTitlesLatest'): 			listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='Latest')
	elif (mode=='GetTitlesPopular'): 			listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='Popular')
	elif (mode=='GetTitlesHDPopular'): 		listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='HDPopular')
	elif (mode=='GetTitlesOtherPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='OtherPopular')
	elif (mode=='GetTitlesNewPopular'): 	listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck='NewPopular')
	elif (mode=='GetLinks'): listLinks(_param['section'], _param['url'], showtitle=_param['showtitle'], showyear=_param['showyear'])
	elif (mode=='GetSeasons'): listSeasons(_param['section'], _param['url'], _param['img'])
	elif (mode=='GetEpisodes'): listEpisodes(_param['section'], _param['url'], _param['img'], _param['season'])
	elif (mode=='TextBoxFile'): TextBox2().load_file(_param['url'],_param['title'])
	elif (mode=='TextBoxUrl'):  TextBox2().load_url( _param['url'],_param['title'])
	elif (mode=='SearchForAirDates'):  search_for_airdates(_param['title'])
	#elif (mode=='GetSearchQuery'): GetSearchQuery(_param['section'])
	#elif (mode=='Search'): Search(_param['section'], query)
##### /\ ##### Modes #####
### ############################################################################################################
deb('param >> url',_param['url']) ### Simply Logging the current query-passed / param -- URL
check_mode(_param['mode']) ### Runs the function that checks the mode and decides what the plugin should do. This should be at or near the end of the file.
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
