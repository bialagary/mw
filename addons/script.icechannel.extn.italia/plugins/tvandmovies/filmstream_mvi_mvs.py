'''
    filmstream  # thanks to to shani for the decrypter.py
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
#from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui

import re
decoded_stuff = ""
filmstream_function = """def MYFUNC(<FUNCTION_PARAMS>):
    global decoded_stuff
<FUNCTION>

<FUNCTION_CALL>
"""

try:
    import json
except:
    import simplejson as json

class filmstream(MovieIndexer,MovieSource):
    implements = [MovieIndexer,MovieSource]
    
    name = "filmstream (Italia)"
    display_name = "Filmstream (Italia)"
    base_url = 'http://filmstream.me/'
    #img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/92bed8a40419803f31f90e2268956db50d306997/flixanity.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    #cookie_file = os.path.join(common.cookies_path, 'NRlogin.cookie')
    icon = common.notify_icon
    
    '''
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="Enter your noobroom email" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '<setting label="Premium account will allow for 1080 movies and the TV Shows section" type="lsep" />\n'
        xml += '<setting id="premium" type="bool" label="Enable Premium account" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
    '''

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'al-cinema':
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'page/' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            if total_pages == '':
                r= '<a class="last" href="http://filmstream.me/al-cinema/page/(.+?)/">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, 'al-cinema', url, type, str(page), total_pages)

            for item in re.finditer(r'<h2> <a href="(.+?)">(.+?)</a> </h2>\s*<div class=".+?">.+?</div>\s*</div>\s*<a href=".+?" title="">\s*<img src="(.+?)" alt="(.+?)"',html,re.I):
                url=item.group(1)
                name=item.group(4)
                name=name.split('Stream')[0]
                image=item.group(3)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name, img=image, plot='')
                

          
        else:
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'page/' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            if total_pages == '':
                r= '<a class="last" href="http://filmstream.me/.+?/page/(.+?)/">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, 'al-cinema', url, type, str(page), total_pages)

            for item in re.finditer(r'<h2> <a href="(.+?)">(.+?)</a> </h2>\s*<div class=".+?">.+?</div>\s*</div>\s*<a href=".+?" title="">\s*<img src="(.+?)" alt="(.+?)"',html,re.I):
                url=item.group(1)
                name=item.group(4)
                name=name.split('Stream')[0]
                image=item.group(3)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name, img=image, plot='') 

                    
       
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        
        net = Net()

        url_type = ''
        content_type = ''
        
        if indexer == common.indxr_Movies:#'[COLOR orange]'+year+'[/COLOR]'

            if section == 'main':
                self.AddSection(list, indexer,'al-cinema','Al-Cinema',self.base_url +'al-cinema/',indexer)
                self.AddSection(list, indexer,'piu-visti','Piu-Visti',self.base_url +'piu-visti/',indexer)
                self.AddSection(list, indexer,'sub-ita','Sub-Ita',self.base_url +'film/sub-ita/',indexer)
                self.AddSection(list, indexer,'anno','Anno','http://filmstream.me/news/',indexer)
                self.AddSection(list, indexer,'genre','Genere','http://filmstream.me/news/',indexer)
                #self.AddSection(list, indexer,'popular','Popular',self.base_url +'movies/favorites/',indexer)         
                           
            elif section == 'genre':
                r = re.findall(r'<li><a href="(http://filmstream.me/film/.+?)">(.+?)</a></li>', net.http_GET(url).content, re.I)
                for genres_url,genres in r[0:]:
                    genres_title = genres.upper()
                    self.AddSection(list, indexer, 'genres_title', genres_title, genres_url, indexer)

            elif section == 'anno':
                r = re.findall(r'<li><a href="(http://filminstreaming.eu/anno/.+?)">(.+?)</a></li>', net.http_GET(url).content, re.I)
                for anno_url,anno in r[0:]:
                    anno_title = anno.upper()
                    self.AddSection(list, indexer, 'anno_title', anno_title, anno_url, indexer)
                
                

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

            
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net()
                  
        self.AddFileHost(list, 'NA', url)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        import urllib
        name = name.lower()
        
        main_url='http://filmstream.me/index.php/?s=%s' %(name.replace(' ','+'))
        
        if type == 'movies':
            html = net.http_GET(main_url).content
            item_url=re.compile('<h2> <a href="(.+?)">.+?</a> </h2>').findall(html)[0]
            print item_url
            print '#item_url##########################################'
            self.GetFileHosts(item_url, list, lock, message_queue)
            
    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        if page and len(page) > 0 and total_pages and len(total_pages) > 0 and int(page) > int(total_pages):
            return
        
        if page=='': page='1'
        
        from entertainment.net import Net
        net = Net()
        search_url ='%spage/%s/?s=%s' %(self.base_url, page, keywords.replace(' ','+'))
        print search_url
        import re
        
        html = net.http_GET(search_url).content
        if total_pages == '':
            r= '<a class="last" href="http://filmstream.me/page/(.+?)/'
            try:
                total_pages = re.compile(r).findall(html)[0]
            except:
                total_pages = '1'
            
                
        self.AddInfo(list, indexer, 'search', self.base_url, type, str(page), total_pages)

        for item in re.finditer(r'<h2> <a href="(.+?)">(.+?)</a> </h2>\s*<div class=".+?">.+?</div>\s*</div>\s*<a href=".+?" title="">\s*<img src="(.+?)" alt="(.+?)"',html,re.I):
            url=item.group(1)
            name=item.group(4)
            name=name.split('Stream')[0]
            image=item.group(3)
            name = self.CleanTextForSearch(name)
            self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name, img=image, plot='') 
    
    def decode(self, encoded_stuff):
        global filmstream_function
        
        f0 = encoded_stuff.split('eval(')
        f1 = re.search('unescape\([\'"](.+?)[\'"]',f0[1]).group(1)

        import urllib
        f1 = urllib.unquote(f1)
        print f1
        f11 = re.search('function \((.+?)\)', f1).group(1)
        filmstream_function = filmstream_function.replace('<FUNCTION_PARAMS>', f11)

        f2 = re.search('\{(.*)\}', f1).group(1)

        f31 = re.sub('for\((.+?)=(.+?);.+?<(.+?);.+?\)', r'for \1 in xrange(\2, \3)', f2 )

        f3 = re.sub('[^a-zA-Z0-9]([a-zA-Z0-9]+?)\.length', r'len(\1)', f31)

        f4 = re.sub('[^a-zA-Z0-9]{1}([a-zA-Z0-9]+?)=([a-zA-Z0-9]+?)\.replace\(.+?\(([a-zA-Z0-9\[\]]+?),.+?,([a-zA-Z0-9\[\]]+?)\)', r':\1=re.sub(\3,\4,\2)', f3)

        f5 = re.sub('[^a-zA-Z0-9]{1}[a-zA-Z0-9]+?=[a-zA-Z0-9]+?\.replace\(.+? RegExp\([\'"]%.+?\);', '', f4)

        f61 = re.sub('document.write\((.+?)\);', r'decoded_stuff=\1;', f5)

        f6 = "    " + f61.replace(" } ", "").replace("} ", "").replace(" }", "").replace("}", "").replace(" ; ", "\n    ").replace(" ;","\n    ").replace("; ", "\n    ").replace(";", "\n    ").replace(":",":\n        ")

        callf = re.sub('(?s)unescape\((.+?)\);.*', r'MYFUNC(\1', f0[2])
        callf = re.sub('[\r\n]+', ' ', callf)
        callf = re.sub(';"([ &]{1})', r';\\"\1', callf)
        
        filmstream_function = filmstream_function.replace('<FUNCTION>', f6)
        filmstream_function = filmstream_function.replace('<FUNCTION_CALL>', callf)
        print filmstream_function
        exec filmstream_function


    def Resolve(self, url):
        import decrypter
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        html = net.http_GET(url).content
        encoded_stuff = re.search('(?s)(<script>eval.+?</script>)', html)
        if encoded_stuff:
            encoded_stuff = encoded_stuff.group(1)
            self.decode(encoded_stuff)
            
            kplayer_root_url = re.search('KPlayer.kplayer_root_url = [\'"](.+?)[\'"]', decoded_stuff).group(1).replace('\/','/')
            kplayer_e = re.search('KPlayer.init\([\'"](.+?)[\'"]\)', decoded_stuff).group(1)
            html = net.http_POST(kplayer_root_url, {'url':kplayer_e}, headers={'Referer':url}).content
            j = json.loads(html)
            captcha_k = ""
            if j['status'] == False and j['code']==3:
                captcha_dict = common.handle_captcha(url, '<script type="text/javascript" src="http://www.google.com/recaptcha/api/js/recaptcha_ajax.js">', params={'site':j['k']})
                if captcha_dict['status'] == 'ok':
                    html = net.http_POST(kplayer_root_url, {'url':kplayer_e, 'chall':captcha_dict['challenge'], 'res':captcha_dict['captcha']}, headers={'Referer':url}).content
                    print html
                    playfiles = json.loads(html)
                    
                    res_name = []
                    res_url = []
                    
                    if playfiles['status']==True and playfiles['code']==1000:
                        for playfile in playfiles['source']:
                            res_name.append(playfile['label'])
                            res_url.append(playfile['file'])
                            
                        dialog = xbmcgui.Dialog()
                        ret = dialog.select('Please Select Stream Quality.',res_name)
                        if ret < 0:
                            return None

                        else:
                            return res_url[ret].replace('\/','/').replace('\u003d','=').replace('\u0026','&')

        else:
            headers={'Host':'r20---googlevideo.com', 'Referer': url , 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
            html = net.http_GET(url).content
            if '<div id="embedHolder" style="display:none;"><iframe src="' in html:
                item_url=re.compile('<div id="embedHolder" style="display:none;"><iframe src="(.+?)"').findall(html)[0]
                headers={'Host':'r20---googlevideo.com', 'Referer': url , 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}

                content = net.http_GET(item_url,headers).content

                new_url = re.search("[\"']{1}file[\"']{1}\:[\"']{1}(.+?)[\"']{1}", content)
                if new_url:
                    new_url = new_url.group(1).replace("\/", "/")

                    headers.update({'Referer':item_url, 'Accept':'*/*', 'Accept-Encoding':'identity;q=1, *;q=0', 'Range':'bytes=0-'})
                    import urllib2
                    try:
                        new_content =  net.http_GET(new_url,headers,auto_read_response=False)
                        play_url = new_content.get_url()
                    except urllib2.HTTPError, error:
                        play_url = error.geturl()
                    
                    return play_url        
                
            else:
                url = re.compile('FlashVars="config=http://filmstream.me/config.xml.+?proxy.link=filmstream\*(.+?)&.+?"').findall(html)[0]
                url = decrypter.decrypter(198,128).decrypt(url,'OdrtKapH2dNRpVHxhBtg','ECB').split('\0')[0]
            
                result = net.http_GET(url).content

                res_name = []
                res_url = []

                r = re.findall('\,(\d+\,\d+)\,\"(http://redirector.googlevideo.com/videoplayback?.*?)\"',result)
                for quality, url in r:
                    if '1920' in quality:
                        quality = '1080P'
                    elif '1280' in quality:
                        quality = '720P'
                    elif '852' in quality:
                        quality = 'SD'
                    else:
                        quality ='LOW QUALITY'
                    res_name.append(quality)                
                    res_url.append(url)

                dialog = xbmcgui.Dialog()
                ret = dialog.select('Please Select Stream Quality.',res_name)

                if ret <= 0:
                    return None

                elif ret >1:

                    return res_url[ret].replace('\u003d','=').replace('\u0026','&')
                

            


        
