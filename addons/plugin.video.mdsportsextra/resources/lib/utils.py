import os
import re
import sys
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcgui

############# A massive thankyou to Jas0n_pc for sending me the code for this twitter window its brilliant#################

from addon.common.net import Net
from addon.common.addon import Addon

net = Net()

addon_id = 'plugin.video.mdsportsextra'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)

sys.path.append(os.path.join(addon.get_path(), 'resources', 'lib'))
data_path = addon.get_profile()

newsurl = 'http://pastebin.com/raw.php?i=uX9XKZtj'

try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)
               
def TWITTER(url):
    #test = net.http_GET(newsurl).content
    #r = re.search(r'<message>(.*?)</message>', test, re.I|re.DOTALL)

    #print r.groups()
    
    try:
      latestnews = re.sub(r'\r|\n', ' ', re.search('<message>(.*?)</message>', net.http_GET(newsurl).content, re.I|re.DOTALL).group(1))
    except: pass
    #print latestnews
    
    html = net.http_GET(url).content
    l = []
    r = re.findall('tem\>.*?title>(.*?)</tit.*?ption>(.*?)</desc.*?bDate>(.*?)\s+\d+\:', html, re.I|re.DOTALL)
    for text, des, date in r:
        
        text = re.sub(r'(?i)(\#\w+)\s', r'[COLOR blue]\1[/COLOR] ', text)
        text = re.sub(r'(?i)(\#\w+)$', r'[COLOR blue]\1[/COLOR] ', text)
        text = re.sub(r'(?i)(pic\.twitter.*?)$', r'', text)
        text = re.sub(r'(?i)^(white\w+)\:', r'[B][COLOR red]<<<[/B][/COLOR]\1:',text)
        text = re.sub(r'(?i)^(\w+)(?!white\w+)\:', r'[B][COLOR red]>>>[/B][/COLOR]\1:',text)
        #text = re.sub(r'(?i)(@.*?)$', r'[COLOR red]@[/COLOR]', text)
        des = des.replace('<![CDATA[','').replace(']]>','')

        final = '[COLOR red]'+date+'[/COLOR]'+'\n'+'\n'+'[COLOR royalblue]'+text+'[/COLOR]'+'\n'+des+'\n'+'\n'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)


def NEWSRSS(url):
    html = net.http_GET(url).content
    l = []
    all_videos = regex_get_all(html, '<item>', '</item>')
    for a in all_videos:
        text = regex_from_to(a, '<content:encoded>', '</content:encoded>')
        date = regex_from_to(a, '<pubDate>', '</pubDate>')
        title = regex_from_to(a, '<title>', '</title>')
        text = text.replace('<p>','').replace('</p>','').replace('<![CDATA[','').replace(']]>','')
        text = text.replace('<li>','').replace('</li>','').replace('<strong>','').replace('</strong>','')
        text = text.replace('<em>','').replace('</em>','').replace('<br />','').replace('&nbsp;','')
        text = text.replace ('<ul>','').replace('</ul>','').replace('&mdash;','[COLOR blue]#[/COLOR]')
        text = text.replace('The post<a rel="nofollow" href=','\n').replace('<a href=','\n').replace('</a>','\n')
        text = text.replace('<a rel="nofollow" href=','\n').replace('<b>','').replace('</b>','')
        text = text.replace('<blockquote>','').replace('</blockquote>','')
        text = text.replace('</span>','').replace('<span style="font-weight: 400;">','').replace('</script>','')
        text = text.replace('<script async src="//platform.twitter.com/widgets.js?2ebbea" charset="utf-8">','')
        text = re.sub(r'(?i)(http://.*?)$', r'', text)
        


        text = re.sub(r'(?i)(\#\w+)\s', r'[COLOR blue]\1[/COLOR] ', text)
        text = re.sub(r'(?i)(\#\w+)$', r'[COLOR blue]\1[/COLOR] ', text)
        text = re.sub(r'(?i)(pic\.twitter.*?)$', r'', text)
        text = re.sub(r'(?i)^(white\w+)\:', r'[B][COLOR red]<<<[/B][/COLOR]\1:',text)
        text = re.sub(r'(?i)^(\w+)(?!white\w+)\:', r'[B][COLOR red]>>>[/B][/COLOR]\1:',text)

        final = '[COLOR red]'+date+'[/COLOR]'+'\n'+'\n'+'[COLOR royalblue]'+title+'[/COLOR]'+'\n'+text+'\n'+'\n'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)



def RESFIX(url):
    html = net.http_GET(url).content
    l = []
    all_videos = regex_get_all(html, '<tr class="match" id=".*?">', '</td>\n <td>\n </td>')
    for a in all_videos:
        date = regex_from_to(a, '<span class="date"><a href=".*?" title="', '"')
        ht = regex_from_to(a, '<td class="team homeTeam">\n <a href=".*?" title=".*?">', '</a>')
        at = regex_from_to(a, '<td class="team awayTeam">\n <a href=".*?" title=".*?">', '</a>')
        res = regex_from_to(a, '<td class="score">\n <a href="#" class="vs" title="View Match info"><em>', '</em></a>')
        res = res.replace('</em>&nbsp;-&nbsp;<em>',' - ')

        final = '[COLOR royalblue]'+date+'[/COLOR]'+'\t'+ht+'\t'+res+'\t'+at+'\n'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)



def CLTABLES(url):
    html = net.http_GET(url).content
    l = []
    r = re.findall('<strong class="text-transform">(.*?)</th>', html, re.I|re.DOTALL)
    for text in r:
        text= text.replace('</strong>',' Updated')
        final = '[COLOR skyblue]'+text+'[/COLOR]'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)
    

def LTABLES(url):
    html = net.http_GET(url).content
    l = []
    r = re.findall('<tr class=".*?">\r\n              <td>(.*?)</td>\r\n              <td class="teams"><a href=".*?" title="(.*?)">.*?</a></td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td></td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td></td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n              <td>(.*?)</td>\r\n            </tr>', html, re.I|re.DOTALL)
    for pos, team, pld, gd, pts, wh, dh, lh, fh, ah, wa, da, la, fa, aa in r:
        final = '[COLOR skyblue]['+pos+'][/COLOR]'+'\t'+team+'\t[COLOR skyblue]'+'Pld= '+pld+' '+'GD= '+gd+' '+'Pts= '+pts+'[/COLOR]\tH,W= '+wh+'  H,D= '+dh+'  H,L= '+lh+'  H,F= '+fh+'  H,A= '+ah+'\t[COLOR skyblue]A,W= '+wa+'  A,D= '+da+'  A,L= '+la+'  A,F: '+fa+'  A,A= '+aa+'[/COLOR]\n'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)




def OF(url):
    text = net.http_GET(url).content
    l = []
    text = text.replace('Matchday','[COLOR skyblue]Matchday[/COLOR]').replace('(','[COLOR skyblue]([/COLOR]').replace(')','[COLOR skyblue])[/COLOR]')
    text = text.replace('1','[COLOR skyblue]1[/COLOR]').replace('2','[COLOR skyblue]2[/COLOR]').replace('3','[COLOR skyblue]3[/COLOR]').replace('4','[COLOR skyblue]4[/COLOR]').replace('5','[COLOR skyblue]5[/COLOR]')
    text = text.replace('6','[COLOR skyblue]6[/COLOR]').replace('7','[COLOR skyblue]7[/COLOR]').replace('8','[COLOR skyblue]8[/COLOR]').replace('9','[COLOR skyblue]9[/COLOR]').replace('0','[COLOR skyblue]0[/COLOR]')
    text = text.replace('#','[COLOR skyblue]#[/COLOR]').replace('@','[COLOR skyblue]@[/COLOR]').replace('-','[COLOR skyblue]-[/COLOR]')
    text = text.replace('#note: only used for checksum (will NOT get loaded into database)','')
    final = text
    l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)



def LIVESHEAD(url):
    html = net.http_GET(url).content
    l = []
    r = re.findall('<description>(.*?)</description>', html, re.I|re.DOTALL)
    r = r[0]
    for text in r:
        text= text.replace('Soccer','Football')
        final = '[COLOR skyblue]'+text+'[/COLOR]'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)





def LIVESCORE(url):
    html = net.http_GET(url).content
    l = []
    r = re.findall('tem\>.*?title>(.*?)</tit.*?ption>(.*?)</desc.*?bDate>(.*?)\s+\d+\:', html, re.I|re.DOTALL)
    for text, des, date in r:
        text = text.replace('Soccer #Livescore: ','')
        text = text.replace('1','[COLOR skyblue]1[/COLOR]').replace('2','[COLOR skyblue]2[/COLOR]').replace('3','[COLOR skyblue]3[/COLOR]').replace('4','[COLOR skyblue]4[/COLOR]').replace('5','[COLOR skyblue]5[/COLOR]')
        text = text.replace('6','[COLOR skyblue]6[/COLOR]').replace('7','[COLOR skyblue]7[/COLOR]').replace('8','[COLOR skyblue]8[/COLOR]').replace('9','[COLOR skyblue]9[/COLOR]').replace('0','[COLOR skyblue]0[/COLOR]')
        text = text.replace('#','[COLOR skyblue]#[/COLOR]').replace('@','[COLOR skyblue]@[/COLOR]').replace('-','[COLOR skyblue]-[/COLOR]')
        text = text.replace(' vs ',' [COLOR gold]vs[/COLOR] ')
        des = des.replace('<![CDATA[','').replace(']]>','')

        final = '[COLOR skyblue]'+date+'[/COLOR]'+'\n'+'\n'+text+'\n'+'[COLOR gold]'+des+'[/COLOR]'+'\n\n'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)




def LIVESCORE2(url):
    html = net.http_GET(url).content
    l = []
    all_videos = regex_get_all(html, '<td height="16">', '<td></td>')
    for a in all_videos:
        time = regex_from_to(a, '<b>', '<')
        stat = regex_from_to(a, '<input type="hidden" value="live" />', '<')
        time2 = regex_from_to(a, "<font color='red'><b>", "<")
        league = regex_from_to(a, 'onclick="leagueData(.*?); return false;">', '<')
        ht = regex_from_to(a, '<td style="white-space: nowrap;">', '<')
        at = regex_from_to(a, '<div style="white-space: nowrap; overflow: hidden; width: 160px">', '</a>')
        htscore = regex_from_to(a, '<td class="score">\n <a href="#" class="vs" title="View Match info"><em>', '</em></a>')
        score = regex_from_to(a, '<td><b>', '<')

        final = '[COLOR skyblue]'+time+'[/COLOR]'+'\t'+stat+'\t'+time2+'\t'+league+'\n'+ht+at+'\n'+score
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)



def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r


def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r     
    
    

    


        
