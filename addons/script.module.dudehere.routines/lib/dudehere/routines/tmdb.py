import json
import urllib
import unicodedata
from dudehere.routines import *
from metahandler.TMDB import TMDB
MOVIE_GENRES =  enum(
		ACTION = 28,
		ADVENTURE = 12,
		ANIMATION = 16,
		COMEDY = 35,
		CRIME = 80,
		DOCUMENTARY = 99,
		DRAMA = 18,
		FAMILY = 10751,
		FANTASY = 14,
		HISTORY = 36,
		HORROR = 27,
		MUSIC = 10402,
		MYSTERY = 9648,
		ROMACE = 10749,
		SCIFI = 878,
		THRILLER = 53,
		WAR = 10752,
		WESTERN = 37
)

TV_GENRES =  enum(
		ACTION = 10759,
		ADVENTURE = 10759,
		ANIMATION = 16,
		COMEDY = 35,
		DOCUMENTARY = 99,
		DRAMA = 18,
		EDUCATION = 10761,
		FAMILY = 10751,
		FANTASY = 10765,
		KIDS = 10762,
		HISTORY = 36,
		MYSTERY = 9648,
		NEWS = 10763,
		POLITICS = 10768,
		REALITY = 10764,
		SCIFI = 10765,
		WAR = 10768,
		WESTERN = 37
)

backdrop_sizes = ["w300","w780","w1280","original"]
logo_sizes = ["w45","w92","w154","w185","w300","w500","original"]
poster_sizes = ["w92","w154","w185","w342","w500","w780","original"]
profile_sizes = ["w45","w185","h632","original"]
still_sizes = ["w92","w185","w300","original"
			]
class TMDB_API():
	api_key = 'af95ef8a4fe1e697f86b8c194f2e5e11'
	def __init__(self):
		pass
	
	def normalize(self, string):
		return unicodedata.normalize('NFKD', unicode(string)).encode('utf-8','ignore')
	
	def lookup(self, media, id):
		if media=='movie':
			base_uri = 'movie/%s' % id
			record = self.request(base_uri)
		metadata = self.process_record(record, media)	
		return metadata
	
	def discover_movies(self, query):
		base_uri = "discover/movie"
		return self.request(base_uri, urllib.urlencode(query))
	
	def movie_trailers(self, id):
		base_uri = "movie/%s/videos" % id
		results = self.request(base_uri)
		trailers = []
		for result in results['results']:
			if result['site'] == 'YouTube':
				record = {"name": result['name'], "key": result['key']}
				trailers.append(record)
		return trailers
		
	def list_movie_genre(self, id, page=1):
		base_uri = "genre/%s/movies?page=%s" % (id, page)
		results = self.request(base_uri, '')
		return results
	
	def list_tv_genre(self, id, page=1):
		base_uri = "discover/tv"
		query = 'with_genres=%s&sort_by=popularity.desc&page=%s' % (id, page)
		results = self.request(base_uri, query)
		return results
	
	def query_person_id(self, person):
		ids = []
		base_uri = "search/person"
		query = {"query": person}
		results = self.request(base_uri, urllib.urlencode(query))
		for r in results['results']:
			if r['name'].lower() == person.lower():
				ids.append(str(r['id']))
		return ids
	
	def query_keyword_id(self, keyword, strict=False):
		ids = []
		base_uri = "search/keyword"
		query = {"query": keyword}
		results = self.request(base_uri, urllib.urlencode(query))
		for r in results['results']:
			if strict and r['name'].lower() != keyword.lower(): 
				continue
			ids.append(str(r['id']))
		return ids
	
	def process_record(self, record, media=None):
		if media=='movie':
			meta = self.process_movie(record)
			return meta
		elif media=='episode':
			meta = self.process_episode(record)
			return meta
		elif media=='tvshow':
			meta = self.process_show(record)
			return meta
	
	def meta_map(self, path, object, default=''):
		try:
			if isinstance(path, list):
				for k in path:
					object = object[k]
			else:
				object = object[path]
				object = self.normalize(object) if object is not None else default
			return object
		except:
			return default
		
	def process_movie(self, record):
		meta = {}
		meta['imdb_id'] = None
		meta['tmdb_id'] = self.meta_map('id', record)
		meta['title'] = self.meta_map('title', record)
		meta['year'] = record['release_date'][0:4] if self.meta_map('release_date', record) else 0
		meta['writer'] = ''
		meta['director'] = ''
		meta['tagline'] = ''
		meta['cast'] = []
		meta['rating'] = self.meta_map('vote_average', record)
		meta['votes'] =self.meta_map('vote_count', record)
		meta['duration'] = ''
		meta['plot'] = self.meta_map('overview', record)
		meta['mpaa'] = ''
		meta['premiered'] = self.meta_map('release_date', record)
		meta['trailer_url'] = ''
		meta['genre'] = ''
		meta['studio'] = ''
		meta['thumb_url'] = 'http://image.tmdb.org/t/p/w780%s' % record['poster_path']
		meta['cover_url'] = 'http://image.tmdb.org/t/p/w780%s' % record['poster_path']
		meta['backdrop_url'] = 'http://image.tmdb.org/t/p/original%s' % record['backdrop_path']
		meta['overlay'] = 6
		meta['playcount'] = 0
		return meta	
	
	def process_show(self, record):
		meta = {}
		meta['imdb_id'] = None
		meta['tmdb_id'] = record['id']
		meta['title'] = self.meta_map('name', record)
		meta['TVShowTitle'] = self.meta_map('name', record)
		meta['rating'] = self.meta_map('popularity', record)
		meta['duration'] = ''
		meta['plot'] = self.meta_map('overview', record)
		meta['mpaa'] = ''
		meta['premiered'] = self.meta_map('first_air_date', record)
		meta['year'] = record['first_air_date'][0:4] if self.meta_map('first_air_date', record) else 0
		meta['trailer_url'] = ''
		meta['genre'] = ''
		meta['studio'] = ''
		meta['status'] = ''      
		meta['cast'] = []
		meta['banner_url'] = ''	
		meta['cover_url'] = 'http://image.tmdb.org/t/p/w780%s' % record['poster_path']
		meta['backdrop_url'] = 'http://image.tmdb.org/t/p/original%s' % record['backdrop_path']
		meta['overlay'] = 6
		meta['episode'] = 0
		meta['playcount'] = 0
		return meta
	
	def request(self, base_uri, query=''):
		
		tmdb = TMDB(api_key = self.api_key)
		results = tmdb._do_request(base_uri, query)
		return results
		