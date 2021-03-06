import json
import re
import urlparse
			
domain="http://dizipub.com"
encoding="utf-8"


def crawl_movie_page(mpage):
	#check pub player
	google=re.findall('(http\://dizipub.com/player/.*?)"',mpage)
	if len(google)>0:
		return ("google",{"url":google[0],"referer":domain})
	okru=re.findall('mid\%3D(.*?)"',mpage)
	if len(okru)>0:
		return ("okru",okru[0])
	okru2=re.findall('"http://ok.ru/videoembed/(.*?)"',mpage)
	if len(okru2)>0:
		return ("okru",okru2[0])
	vkfix=re.findall('iframe.*?src="(http://vkfix.com.*?)"',mpage)
	if len(vkfix)>0:
		return ("vkfix",vkfix[0])
	cloudy=re.findall('iframe.*?src="(.*?cloudy.*?)"',mpage)
	if len(cloudy)>0:
		hash=urlparse.parse_qs(urlparse.urlparse(cloudy[0]).query).get("id")[0]
		return ("cloudy",hash)
	openload=re.findall('<iframe src="https://openload.co/embed/(.*?)/',mpage)
	if len(openload)>0:
		return ("openload",openload[0])
	return None,None

def return_links(name,mp,h):
	parts=[{"url_provider_name":mp, "url_provider_hash":h}]
	mname="[HS:TR]%s" % (name,)
	ump.add_mirror(parts,mname)

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not("tvshowtitle" in i.keys() and not i["tvshowtitle"]==""):
		return None
	names=[i["tvshowtitle"]]
	results=[]
	found=False
	if "tvshowalias" in i.keys():
		names.extend(i["tvshowalias"].split("|"))
	for name in names:
		ump.add_log("dizipub is searching %s" % name)
		q={"action":"ajax_search","fn":"get_ajax_search","terms":name}
		results=json.loads(ump.get_page(domain+"/wp-admin/admin-ajax.php",encoding,query=q))
		if len(results)==0 or len(results)==1 and "Arama kriterlerinize" in results[0]: 
			ump.add_log("dizipub can't find any links for %s"%name)
			continue
		for result in results:
			if ump.is_same(result["value"],name):
				found=True
				break
		if found:
			break
	
	if not found: return
	src=ump.get_page(result["url"],encoding)
	epis=re.findall('</div><h3> <a href="(.*?)">.*?([0-9]*?)\.S.*?([0-9]*?)\.B.*?</a></h3>',src)
	if len(epis)==0 and i["season"]==1:
		epis=re.findall('<h3> ?<a href="(.*?)">.*?([0-9]*?)\..*?</a></h3>',src)
		epis=[(x[0],1,x[1]) for x in epis]
	for epi in epis:
		u,s,e = epi
		s=int(s)
		e=int(e)
		if s==i["season"] and e==i["episode"]:
			ename="%s %dx%d %s" % (result["value"],s,e,i["title"])
			ump.add_log("dizipub matched %s " % (ename,))
			mpage=ump.get_page(u,encoding)
			mp,h=crawl_movie_page(mpage)
			if not mp is None:
				return_links(ename,mp,h)
			alts=re.findall('><a href="(.*?)"><span class="listed-item">',mpage)
			for alt in alts:
				mpage=ump.get_page(alt,encoding)
				mp,h=crawl_movie_page(mpage)
				if not mp is None:
					return_links(ename,mp,h)