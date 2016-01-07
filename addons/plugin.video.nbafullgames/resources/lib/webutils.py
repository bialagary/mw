try:
	from BeautifulSoup import BeautifulSoup as bs
except:
	from bs4 import BeautifulSoup as bs
try:
	import urllib2
except:
	import urllib.request as urllib2
	
import urllib
from addon.common.net import Net


def read_url(url):
    net = Net()

    html=net.http_GET(url).content
    import HTMLParser
    h = HTMLParser.HTMLParser()
    html = h.unescape(html)
    try:
    	return html.encode('utf-8')
    except:
    	return html

def get_soup(url):
	return bs(read_url(url))

