from webutils import *
import re,sys
from addon.common.addon import Addon
addon = Addon('plugin.video.nbafullgames', sys.argv)


base_url='http://www.nbahd.com'




def get_games(site):
	soup=get_soup(site)
	items=soup.findAll('div',{'class':'thumb'})
	out=[]
	for item in items:
		url=item.find('a')['href']
		title=item.find('a')['title']
		thumb=item.find('img')['src']

		out+=[[title,url,thumb]]
	try:
		next_page=soup.find('div',{'class':'wp-pagenavi'}).find('a',{'class':'nextpostslink'})['href']
	except:
		next_page='0'
	return out,next_page


def get_teams():
    team_list = [[u'http://nbahd.com/tag/philadelphia-76ers/', u'Philadelphia 76Ers', u'http://i.imgur.com/KtSDfDX.png'], [u'http://nbahd.com/tag/portland-trail-blazers/', u'Portland Trail Blazers', u'http://i.imgur.com/fLa6krI.png'], [u'http://nbahd.com/tag/milwaukee-bucks/', u'Milwaukee Bucks', u'http://i.imgur.com/4rMpMsV.png'], [u'http://nbahd.com/tag/chicago-bulls/', u'Chicago Bulls', u'http://i.imgur.com/RpF3amJ.png'], [u'http://nbahd.com/tag/cleveland-cavaliers/', u'Cleveland Cavaliers', u'http://i.imgur.com/1B2LieQ.png'], [u'http://nbahd.com/tag/boston-celtics/', u'Boston Celtics', u'http://i.imgur.com/9poCmBL.png'], [u'http://nbahd.com/tag/los-angeles-clippers/', u'Los Angeles Clippers', u'http://i.imgur.com/SEwO6KA.png'], [u'http://nbahd.com/tag/memphis-grizzlies/', u'Memphis Grizzlies', u'http://i.imgur.com/651AtvO.png'], [u'http://nbahd.com/tag/atlanta-hawks/', u'Atlanta Hawks', u'http://i.imgur.com/PKXfzFb.png'], [u'http://nbahd.com/tag/miami-heat/', u'Miami Heat', u'http://i.imgur.com/uiT6LZV.png'], [u'http://nbahd.com/tag/charlotte-hornets/', u'Charlotte Hornets', u'http://i.imgur.com/ZaTTvAt.png'], [u'http://nbahd.com/tag/utah-jazz/', u'Utah Jazz', u'http://i.imgur.com/5pw1NIR.png'], [u'http://nbahd.com/tag/sacramento-kings/', u'Sacramento Kings', u'http://i.imgur.com/NfvLz4g.png'], [u'http://nbahd.com/tag/new-york-knicks/', u'New York Knicks', u'http://i.imgur.com/VDv8ntK.png'], [u'http://nbahd.com/tag/los-angeles-lakers/', u'Los Angeles Lakers', u'http://i.imgur.com/1p3nEZu.png'], [u'http://nbahd.com/tag/orlando-magic/', u'Orlando Magic', u'http://i.imgur.com/0dqVPuU.png'], [u'http://nbahd.com/tag/dallas-mavericks/', u'Dallas Mavericks', u'http://i.imgur.com/P1tPEpC.png'], [u'http://nbahd.com/tag/brooklyn-nets/', u'Brooklyn Nets', u'http://i.imgur.com/EVVastT.png'], [u'http://nbahd.com/tag/denver-nuggets/', u'Denver Nuggets', u'http://i.imgur.com/B6Gyq3Z.png'], [u'http://nbahd.com/tag/indiana-pacers/', u'Indiana Pacers', u'http://i.imgur.com/glh7tDS.png'], [u'http://nbahd.com/tag/new-orleans-pelicans/', u'New Orleans Pelicans', u'http://i.imgur.com/XvqBSFK.png'], [u'http://nbahd.com/tag/detroit-pistons/', u'Detroit Pistons', u'http://i.imgur.com/Ze2GGX0.png'], [u'http://nbahd.com/tag/toronto-raptors/', u'Toronto Raptors', u'http://i.imgur.com/4ZFUqRD.png'], [u'http://nbahd.com/tag/houston-rockets/', u'Houston Rockets', u'http://i.imgur.com/BuXlW6e.png'], [u'http://nbahd.com/tag/san-antonio-spurs/', u'San Antonio Spurs', u'http://i.imgur.com/9M775dI.png'], [u'http://nbahd.com/tag/phoenix-suns/', u'Phoenix Suns', u'http://i.imgur.com/001dpsM.png'], [u'http://nbahd.com/tag/oklahoma-city-thunder/', u'Oklahoma City Thunder', u'http://i.imgur.com/M1vLzwN.png'], [u'http://nbahd.com/tag/minnesota-timberwolves/', u'Minnesota Timberwolves', u'http://i.imgur.com/VgjbiWm.png'], [u'http://nbahd.com/tag/golden-state-warriors/', u'Golden State Warriors', u'http://i.imgur.com/Frs8DtL.png'], [u'http://nbahd.com/tag/washington-wizards/', u'Washington Wizards', u'http://i.imgur.com/X4UagVO.png']]
    lista = sorted(team_list,key=lambda x: x[1])
    team_links = [[x[1],x[0],x[2]] for x in lista]
    return team_links



def get_title(url):
    soup=get_soup(url)
    return soup.find('div',{'class':'entry-content rich-content'}).findAll('p')[0].getText().replace('Watch ','')
def get_urls(url,option):
    soup=get_soup(url)
    tags=soup.find('div',{'class':'entry-content rich-content'}).findAll('p')
    tags.pop(0)
    tags.pop(-1)
    tag=tags[option]
    
    tmp=tag.findAll('a')
    urls=[]

    for t in tmp:
        urls+=[t['href']]

    return urls

def get_link_hd(url):
    html=read_url(url)
    soup=bs(html)
    try:
        link=soup.find('iframe',{'frameborder':'0'})['src']
    except:    
        sd = re.findall('<source src="(.+?)" type=\'video/mp4\' data-res="360p">',html)[0]
        try:
            hd = re.findall('<source src="(.+?)" type=\'video/mp4\' data-res="720p">',html)[0]
        except:
            hd = sd
        HD_en = addon.get_setting('enable_hd')
        if HD_en =='true':
            return hd,True
        else:
            return sd,True

    if 'http' not in link:
        link = 'http://nbahd.com' + link
    return link,False

def get_parts(url):
    soup=get_soup(url)
    tags=soup.find('div',{'class':'entry-content rich-content'}).findAll('p')
    tags.pop(0)
    out=[]
    tag=tags[0]
    parts=tag.findAll('a')
    i = 1
    for part in parts:
        url = part['href']
        title = 'Part %s'%i
        img = ''
        i+=1
        out.append((title,url,img))

    if len(out)==0:
        html=read_url(url)
        links=re.findall('<p><img src="(.+?)"/>\s*</p>\s*<p>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*<a href="(.+?)" target="_blank">\s*<img src=".+?"/></a>\s*',html)
        i = 1
        pos = 0
        for link in links:
            img = link[0]
            for i in range(4):
                url = link[i+1]
                title = 'Part %s'%(i+1)

                out.append((title,url,img))


    return out
def get_game_options(url):
    soup=get_soup(url)
    tags=soup.find('div',{'class':'entry-content rich-content'}).findAll('p')
    tags.pop(0)
    tags.pop(-1)
    options=[]
    for tag in tags:
        try:
            title=''
            title=re.compile('src="http://(?:nba|NBA|nfl|NFL)hd.com/wp-content/uploads/(.+?).png"').findall(str(tag))[0].title()

            if 'p1' in title.lower() or 'p2' in title.lower() or 'p3' in title.lower() or 'p4' in title.lower():
                return
            tmp=tag.findAll('a')
            urls,titles=[],[]
            for t in tmp:
                url=t['href']
                title2=t.getText()
                titl=title+' '+title2
                options+=[[titl,url]]
        except:
            pass
    return options

def resolve_nbahd(url):
    try:
        HD = addon.get_setting('enable_hd')
        soup=get_soup(url)
        if HD=='true':
            try:
                url=soup.find('video').findAll('source')[1]['src']
            except:
                url=soup.find('video').findAll('source')[0]['src']
        else:
            url=soup.find('video').findAll('source')[0]['src']
        return url
    except:
        try:
            import urlresolver
            resolved = urlresolver.resolve(url)
            return resolved
        except:
            return

def getlink_nbahd(link):
    link=link.replace('temporarylink.net','moevideo.net')
    if 'nbahd.com' not in link:
        return link,True
    resolved=resolve_nbahd(link)
    if resolved:
        return resolved,False
    soup=get_soup(link)
    link=soup.find('iframe',{'frameborder':'0'})['src']
    return link,True