import urllib
import urllib2
import re
import time
import os

def _get_page_source(url,data=None,header=None):
	req = urllib2.Request(url, data, header)
	try:
		response = urllib2.urlopen(req)
	except urllib2.URLError as e:
		if hasattr(e, 'reason'):
			raise RuntimeError(str(e.reason))
		elif hasattr(e, 'code'):
			raise RuntimeError(str(e.code))
	else:
		return response.read()

def get_quality_video_link(url,data=None,header=None):
	response_data = _get_page_source(url,data,header)
	
	re_form_data = re.compile(r'<input type="hidden" name="(\w+)" value="(\w+)">')
	form_data = re.findall(re_form_data, response_data)
	data = urllib.urlencode(form_data)
	
	time.sleep(1.8)
	
	response_data = _get_page_source(url, data, header)
	re_video_url = re.compile(r'(http://\S*?/d/.*?)"')
	url = re.search(re_video_url, response_data).group(1)
	url = urllib.quote(url, ':/')
	return url
