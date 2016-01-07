import urllib2
import re

def _get_video_link_dict(url):
	header = {'GData-Version' : '3.0' }
	req = urllib2.Request(url, None, header)
	try:
		response = urllib2.urlopen(req)
	except urllib2.URLError as e:
		if hasattr(e, 'reason'):
			raise RuntimeError(str(e.reason))
		elif hasattr(e, 'code'):
			raise RuntimeError(str(e.code))
	else:
		response_data = response.read()

	for r in re.finditer('"(fmt_stream_map)":"([^\"]+)"', response_data):
		(urlType, urls) = r.groups()
	
	try:
		urls.index('ServiceLogin')
		raise RuntimeError('Authentication required')
	except ValueError:
		pass

	urls = re.sub('\\\\u003d', '=', urls)
	urls = re.sub('\\\\u0026', '&', urls)

	urls = urls.split(',')

	url_dict = {}

	for u in urls:
		r = re.search('(\d+)\|(.+)', u)
		url_dict[r.group(1)] = re.sub('\%2C', ',', r.group(2))
	
	return url_dict
	

def _check_if_quality(itag_dict, url_dict):
	if list(itag_dict):
		max_qual = max(list(itag_dict))
		for itag in itag_dict[max_qual]:
			if itag in url_dict:
				return url_dict[itag]
		else:
			max_qual = max(list(itag_dict))
			del itag_dict[max_qual]
			return _check_if_quality(itag_dict, url_dict)
	else:
		return None

def get_quality_video_link(quality, url, DASH):
	url = re.sub(r'[^/]+$', 'preview', url)

	# itag code reference http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs
	# 					  https://github.com/rg3/youtube-dl/pull/1279
	itag_dict = {1080: ['37', '46'], 720: ['22', '45'],
				480: ['59', '44', '35'], 360: ['43', '34', '18', '6'],
				240: ['5', '36'], 144: ['17']}
	if DASH == 'true':
		itag_dict[1080].extend(['137', '248'])
		itag_dict[720].extend(['136', '247'])
		itag_dict[480].extend(['135', '246', '245', '244'])
		itag_dict[360].extend(['134', '243'])
		itag_dict[240].extend(['133', '242'])
		itag_dict[144].extend(['160'])

	
	quals = list(itag_dict)
	for qual in quals:
		if qual > quality:
			del itag_dict[qual]
			
	url_dict = _get_video_link_dict(url)
	
	return _check_if_quality(itag_dict, url_dict)