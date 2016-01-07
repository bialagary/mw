import sys
import os
import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult

class movietvScraper(CommonScraper):
	broken = True
	
	def __init__(self):
		self.service='movietv'
		self.name = 'movietv.to'
		self.referrer = 'http://www.movietv.to'
		self.base_url = 'http://www.movietv.to'
		self.timeout = 2

		
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		soup = self.request(uri, return_soup=True)
		results = self.process_results(soup)
		return results
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		#soup = self.request(uri, return_soup=True)
		#results = self.process_results(soup)
		return results
	
	def process_results(self, soup):
		results = []
		links = soup.findAll('a', {"rel": "nofollow", "target": "_blank"})
		for link in links:
			host_name = link.string.lower()
			if host_name in self.domains:
				url = "%s://%s" % (self.service, link['href'])
				result = ScraperResult(self.service, host_name, url)
				result.quality = QUALITY.UNKNOWN
				results.append(result)	
		return results
	
	def get_resolved_url(self, raw_url):
		import urlresolver
		resolved_url = ''
		raw_url = self.get_redirect(raw_url)
		source = urlresolver.HostedMediaFile(url=raw_url)
		resolved_url = source.resolve() if source else None
		return resolved_url
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = args[0].lower().replace(" ", "_")
			season = args[1]
			episode = args[2]
			uri = "/Serie/%s-Season-%s-Episode-%s" % (showname, season, episode)
		else:
			title = args[0]	
			year = args[1]
			uri = "/search"
			html = self.request(uri, query={'qe': title})
			print html
		return uri
