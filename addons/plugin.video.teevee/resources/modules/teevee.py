
from BeautifulSoup import BeautifulSoup as bs
import urllib2
import urllib
import HTMLParser
import sys
import json
import re
import threading
import Queue

try:
    from addon.common.net import Net
    from addon.common.addon import Addon

except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("TeeVee Import Failure", "Failed to import addon.common", "A component needed by TeeVee is missing on your system", "Please visit www.tvaddons.ag.com for support")
addon = Addon('plugin.video.teevee', sys.argv)


domain='http://tvonline.tw'

def read_url(url):
    net = Net()

    html=net.http_GET(url).content
    
    h = HTMLParser.HTMLParser()
    html = h.unescape(html)
    return html.encode('utf-8')



def new_episodes():
	url=domain + '/new-episodes/'
	html=read_url(url)
	soup=bs(html)

	tag=soup.find('div',{'class':'home'})
	
	reg=re.compile('<a href="(.+?)".+?>(.+?) S(\d+)E(\d+)</a>')

	episodes=re.findall(reg,str(tag))
	return episodes

def popular_today():
	url=domain + '/popular-today/'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'home'})
	reg=re.compile('<a href="(.+?)".+?>(.+?) \((\d+)\)</a>')

	shows=re.findall(reg,str(tag))
	return shows

def search(query):

	url=domain + '/search.php?key=%s'%(urllib.quote_plus(query))
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'found'})
	reg=re.compile('<a href="(.+?)" target="_blank">(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(tag))

	return shows

def most_popular():
	url=domain + '/most-popular/'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'home'})
	reg=re.compile('<a href="(.+?)".+?>(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(tag))

	return shows

def latest_added():
	url=domain + '/latest-added/'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'home'})
	reg=re.compile('<a href="(.+?)".+?>(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(tag))

	return shows

def get_letters():
	url=domain+'/tv-listings/a'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'tv_letter'})
	reg=re.compile('<a href="(.+?)">(.+?)</a>')
	letters=re.findall(reg,str(tag))

	return letters

def get_shows_letter(letter):
	url=letter
	if domain not in url:
		url=domain+ letter
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'home'})
	reg=re.compile('<a href="(.+?)".+?>(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(tag))

	return shows

def get_genres():
	url=domain+'/genres/action'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'tv_letter'})
	reg=re.compile('<a href="(.+?)">(.+?)</a>')
	genres=re.findall(reg,str(tag))

	return genres

def get_shows(genre):
	url=domain+genre
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'home'})
	reg=re.compile('<a href="(.+?)".+?>(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(tag))

	return shows


def get_seasons(show):
	url=show
	if show[0]!='/' and 'http' not in show:
		show='/'+show

		url=domain + show
	if domain not in url:
		url=domain+url
	html=read_url(url)
	soup=bs(html)

	reg=re.compile('<h3><a href=[\"\'](.+?)[\"\'].+?>Season (\d+)</a></h3>')
	
	seasons=re.findall(reg,str(soup))
	imdb=re.compile('(?:\"|\')http://www.imdb.com/title/(.+?)(?:\"|\')')
	imdb=re.findall(imdb,html)[0]
	return imdb,seasons
	
def get_episodes(season,season_num):
	url=season
	if domain not in url:
		url=domain + season
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'Episode'})
	reg=re.compile('<a href="(.+?)".+?>')
	links=list(re.findall(reg,str(tag)))
	reg2=re.compile('</strong> (\d+) - (.+?)</a>')
	names=re.findall(reg2,str(tag))
	out=[]
	last_num=0
	spec=addon.get_setting('specials')
	if spec=='false':
		for i in range(len(links)):
			check=int(names[i][0])-last_num
			if 'special:' not in names[i][1].lower() and check==1:
				out+=[[links[i],names[i][1],season_num,names[i][0]]]
				last_num=int(names[i][0])

		imdb=re.compile('[\"\']http://www.imdb.com/title/(.+?)[\"\']')
		imdb=re.findall(imdb,str(soup))[0]
		return imdb,out

	else:
		for i in range(len(links)):
			out+=[[links[i],names[i][1],season_num,names[i][0]]]

		imdb=re.compile('[\"\']http://www.imdb.com/title/(.+?)[\"\']')
		imdb=re.findall(imdb,str(soup))[0]
		return imdb,out

def get_imdb(url):
	if url[0]!='/' and 'http' not in url:
			url='/'+url+'/'
			url=domain + url

	else:
			url=url+'/'
	if domain not in url:
		url=domain+url
	html=read_url(url)
	soup=bs(html)
	imdb=re.compile('[\"\']http://www.imdb.com/title/(.+?)[\"\']')
	try:
		imdb=re.findall(imdb,str(soup))[0]
	except:
		imdb=''
	
	return imdb



def get_sources(links):
	sources=[]
	ind=0
	for i in range(len(links)):
		if 'iwatch' not in links[i]:
			reg=re.compile("(?:http|https)://(.+?)/")
			domain=re.findall(reg,links[i])[0]
			domain=domain.replace('www.','').replace('embed.','').replace('beta.','')
			sources+=['%s. '%(i+1)+domain]
		else:
			sources.insert(ind, '%s. iWatch HD link'%(i+1))
			ind+=1
	
	return sources


def get_episodes_calendar(day,month,year):
	url='https://www.iwatchonline.ag/tv-schedule?day=%s&month=%s&year=%s'%(day.lstrip("0"),month.lstrip("0"),year)
	html=read_url(url)
	soup=bs(html)
	table=soup.find('table',{'class':'table table-striped table-hover table-center'})
	
	reg=re.compile('<a href="(.+?)s(\d+)e(\d+)">(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(table))

	return shows

def get_ep_url(ep):
	item=[]
	season=ep[1]
	episode=ep[2]
	show_title=ep[3]
	show_year=ep[4]
	sr=search(show_title)
	for i in range(len(sr)):

		if sr[i][2]==show_year:
			ind=i
			
			
			break
	try:
		lst=list(sr[ind])
		
		url=lst[0]
		url=url+'season-%s-episode-%s'%(season.lstrip("0"),episode.lstrip("0"))
		if url[0]!='/' and 'http' not in url:
			url='/'+url+'/'
		else:
			url=url+'/'
		link=url
		
		item=[link,show_title,season,episode,ep[0]]
		return item
	except:
		return ['0',0,0,0,0]
def get_ep_urll(ep,queue):
	item=[]
	season=ep[1]
	episode=ep[2]
	show_title=ep[3]
	show_year=ep[4]
	sr=search(show_title)
	for i in range(len(sr)):

		if sr[i][2]==show_year:
			ind=i
			
			
			break
	try:
		lst=list(sr[ind])
		
		url=lst[0]
		url=url+'season-%s-episode-%s'%(season.lstrip("0"),episode.lstrip("0"))
		if url[0]!='/' and 'http' not in url:
			url='/'+url+'/'
		else:
			url=url+'/'
		link=url
		
		item=[link,show_title,season,episode,ep[0]]
		queue.put(item)
	except:
		pass

def fetch_parallel(eps):
    result = Queue.Queue()
    threads = [threading.Thread(target=get_ep_urll, args = (ep,result)) for ep in eps]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

def get_all_queue_result(queue):

    result_list = []
    while not queue.empty():
        result_list.append(queue.get())

    return result_list

def get_parallel(eps):
	from multiprocessing.dummy import Pool as ThreadPool 

	pool = ThreadPool(10) 


	results=pool.map(get_ep_url, eps)


	pool.close() 
	pool.join() 
	return results

def get_iwatch_links(url):
	try:
		links=[]
		hosts=[]
		html=read_url(url)
		soup=bs(html)
		table=soup.find('table',{'id':'streamlinks'})
		trs=table.findAll('tr')
		trs.pop(0)
		for i in range(len(trs)):
			try:
				item=trs[i]

			
				link=item.find('td').find('a')['href']
				host=item.find('td').find('a').getText().lstrip().rstrip().lower().lstrip('.')
				
				ind=host.index('<')
				links.append(link)
				hosts.append(host[:ind])
			except:
				pass
			
		

		return links,hosts
	except:
		return [],[]


def resolve_iwatch(url):
	html=read_url(url)
	reg='<iframe name="frame" class="frame" src="(.+?)"'
	return re.findall(re.compile(reg),html)[0]