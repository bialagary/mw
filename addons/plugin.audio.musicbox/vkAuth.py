#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2015 Techdealer

##############LIBRARIES TO IMPORT AND SETTINGS####################

import urllib,urllib2,re,json
from HTMLParser import HTMLParser
import cookielib

###################################################################################
#Token Parser

class TokenParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.url = None
		self.params = {}
		self.in_form = False
		self.form_parsed = False
		self.method = "GET"

	def handle_starttag(self, tag, attrs):
		tag = tag.lower()
		if tag == "form":
			if self.form_parsed:
				raise RuntimeError("Second form on page")
			if self.in_form:
				raise RuntimeError("Already in form")
			self.in_form = True 
		if not self.in_form:
			return
		attrs = dict((name.lower(), value) for name, value in attrs)
		if tag == "form":
			self.url = attrs["action"] 
			if "method" in attrs:
				self.method = attrs["method"]
		elif tag == "input" and "type" in attrs and "name" in attrs:
			if attrs["type"] in ["hidden", "text", "password"]:
				self.params[attrs["name"]] = attrs["value"] if "value" in attrs else ""

	def handle_endtag(self, tag):
		tag = tag.lower()
		if tag == "form":
			if not self.in_form:
				raise RuntimeError("Unexpected end of <form>")
			self.in_form = False
			self.form_parsed = True

###################################################################################
#Login to vk.com

def getToken(email, password, client_id, scope):
	opener = urllib2.build_opener(
								  urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
								  urllib2.HTTPRedirectHandler())
	response = opener.open(
						   "https://oauth.vk.com/oauth/authorize?" + \
						   "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
						   "client_id=%s&scope=%s&display=wap" % (client_id, scope)
						   )
	parser = TokenParser()
	parser.feed(response.read())
	parser.params["email"] = email
	parser.params["pass"] = password
	response = opener.open(parser.url, urllib.urlencode(parser.params))
	try:
		return re.search('access_token=(.+?)&', response.geturl()).group(1)
	except:
		try:
			#if the previous step fail, maybe is necessary give permissions to the application (if used by 1st time), lets try...
			parser = TokenParser()
			parser.feed(response.read())
			response = opener.open(parser.url, urllib.urlencode(parser.params))
			return re.search('access_token=(.+?)&', response.geturl()).group(1)
		except: #login failed
			return False

###################################################################################
#Check if the vk.com token is valid

def isTokenValid(token):
	req = urllib2.Request('https://api.vk.com/method/audio.search.json?q=eminem&access_token='+token)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
	response = urllib2.urlopen(req)
	codigo_fonte=response.read()
	response.close()
	decoded_data = json.loads(codigo_fonte)
	if 'error' in decoded_data:
		#return the detailed error message
		try: return str(decoded_data['error']['error_msg'])
		except: return str(decoded_data['error'])
	else:
		return True