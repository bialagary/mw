# -*- coding: utf-8 -*-
from webutils import *
import re,client
from BeautifulSoup import BeautifulSoup as bs
FINDERS = 6



def find_link(url):
    try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    except: referer = url
    html=client.request(url,referer=referer)
    finders = FINDERS
    ref=url
    for i in range(finders):
        resolved = eval("finder%s(html,ref)"%(str(i+1)))
        if resolved:
            return resolved
            break

def resolve(url):
    try:
        url=find_link(url)
        
        url=resolve_it(url)
    except:
        url= None

    return url

def resolve_it(url):

    if '.m3u8' in url or 'rtmp:' in url or '.flv' in url or '.mp4' in url:
        return url
    
    elif 'sawlive' in url:
    	from resources.lib.resolvers import sawlive
        print(url)
    	return sawlive.resolve(url)
    
    elif 'lshstream' in url:
        from resources.lib.resolvers import lshunter
        return lshunter.resolve(url)
    elif 'abcast' in url:
        from resources.lib.resolvers import abcast
        return abcast.resolve(url)
    elif 'filmon' in url:
        from resources.lib.resolvers import filmon
        return filmon.resolve(url)
    elif 'hdcast' in url:
        from resources.lib.resolvers import hdcast
        return hdcast.resolve(url)
    elif 'sawlive' in url:
        from resources.lib.resolvers import sawlive
        return sawlive.resolve(url)
    elif 'vaughn' in url:
        from resources.lib.resolvers import vaughnlive
        return vaughnlive.resolve(url)
    elif 'p2pcast' in url:
    	print(url)
        from resources.lib.resolvers import p2pcast
        return p2pcast.resolve(url)
    elif 'veetle' in url:
        from resources.lib.resolvers import veetle
        return veetle.resolve(url)
    elif 'mybeststream' in url:
        from resources.lib.resolvers import mybeststream
        return mybeststream.resolve(url)
    elif 'dailymotion' in url:
        from resources.lib.resolvers import dailymotion
        return dailymotion.resolve(url)
    elif 'youtube' in url:
        from resources.lib.resolvers import youtube
        return youtube.resolve(url)
    elif 'acestream://' in url or 'sop://' in url:
        from resources.lib.resolvers import sop_ace
        return sop_ace.resolve(url,title)
   	
    elif 'ucaster' in url:
    	from resources.lib.resolvers import ucaster
    	return ucaster.resolve(url)
    elif 'castalba' in url:
        from resources.lib.resolvers import castalba
        return castalba.resolve(url)


    return url

#vlc_config
def finder2(html,url):
    try:
        soup=bs(html)
        try:
            link=soup.find('embed',{'id':'vlc'})
            link=link['target']

        except:
            link=soup.find('embed',{'name':'vlc'})
            link=link['target']  
        return link          
    except:
        return 

#sawlive
def finder1(html,url):
    try:
        uri = re.compile("[\"']([^\"\']*sawlive.tv\/embed\/[^\"'\/]+)\"").findall(html)[0] + '?referer=' +url
        return uri
    except:
        try:
            uri = re.compile("src=(?:\'|\")(http:\/\/sawlive.tv\/embed\/.+?)(?:\'|\")").findall(html)[0]+ '?referer=' +url
            return uri
        except: 
            return

#jw_config
def finder3(html,url):
    try:
        try:
            link = re.compile('file *: *"(.+?)"').findall(html)[0]
        except:
            link = re.compile("file *: *'(.+?)'").findall(html)[0]
        return link
    except:
        return 
#castalba
def finder4(html,url):
    try:
        reg=re.compile('<script type="text/javascript"> id="(.+?)"; ew=".+?"; eh=".+?";</script><script type="text/javascript" src="http://www.castalba.tv/js/embed.js"></script>')
        id=re.findall(reg,html)[0]
        url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380&r=goatd.net'%id
        return url
    except:
      return


#zunox
def finder6(html,url):
    ref=url
    try:
        urls=bs(html).findAll('iframe')
        for url in urls:
            
            if 'http' not in url['src']:
                if 'zunox' in html:
                    uri = 'http://zunox.hk' + url['src'] 
                elif 'serbiaplus' in html:
                    uri = 'http://www.serbiaplus.com' + url['src']
            else:
                uri = url['src']
            resolved = find_link(uri) #malo rekurzije ;)
            if resolved:
                break
        return resolved
    except:
        return
def finder5(html,url):
    try:
        reg = re.compile('[^\"\'](http://www.lshstream.com[^\"\']*)')
        url = re.findall(reg,html)[0]
        return url
    except:
        return