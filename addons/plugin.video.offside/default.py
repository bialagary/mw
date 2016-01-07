import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import net

from threading import Timer
import json



PLUGIN='plugin.video.offside'
ADDON = xbmcaddon.Addon(id=PLUGIN)
SETTINGS = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('profile'),'settings.xml'))
image='http://xunitytalk.com/stvb/'

auth=ADDON.getSetting('authtoken')
ontapp1=int(ADDON.getSetting('ontapp_id_1'))
ontapp2=int(ADDON.getSetting('ontapp_id_2'))

USER='[COLOR yellow]'+ADDON.getSetting('user')+'[/COLOR]'

THESITE='offsidestreams.com'

UA='XBMC'

net=net.Net()

STVBINI = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'oss.ini')

try:
   filename = 'stvb.ini' 
   import xbmcvfs
   ottv = xbmcaddon.Addon('script.tvguidedixie')
   path = ottv.getAddonInfo('profile')
   file = os.path.join(path, 'ini', filename)
   if not xbmcvfs.exists(file):
       stvb = xbmcaddon.Addon('plugin.video.offside')
       src = os.path.join(stvb.getAddonInfo('path'), 'resources', filename)
       xbmcvfs.copy(src, file)
except:
   pass
                

def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link

def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    
    
if ADDON.getSetting('user')=='':
    ADDON.setSetting('resetpass','false')
    dialog = xbmcgui.Dialog()
    if dialog.yesno(THESITE.upper(), "If You Dont Have An Account", "Please Sign Up At",THESITE.upper(),"Exit","Carry On"):
        
        dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('user',search_entered)
        
        dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('pass',search_entered)
        ADDON.setSetting('login_time','2000-01-01 00:00:00')
    else:
        EXIT()

   
                   

        

def TryAgain():
     dialog = xbmcgui.Dialog()       
     dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
     search_entered = ''
     keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
     keyboard.doModal()
     if keyboard.isConfirmed():
         search_entered = keyboard.getText() 
     ADDON.setSetting('user',search_entered)
     
     dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
     search_entered = ''
     keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
     keyboard.doModal()
     if keyboard.isConfirmed():
         search_entered = keyboard.getText() 
     ADDON.setSetting('pass',search_entered)
     ADDON.setSetting('login_time','2000-01-01 00:00:00')
     try:
        Login()
        return server()
     except: 
        CATEGORIES()        
    
site='http://'+THESITE+'/site/live-tv/'


datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, THESITE+"_new_.lwp")
cookie_amember = os.path.join(cookie_path, THESITE+"_amember_.lwp")
channeljs=os.path.join(cookie_path, "channels.js")
paki=os.path.join(datapath, "paki")



#if  ADDON.getSetting('first_run')=='false':
    #os.remove(cookie_jar)
    #ADDON.setSetting('first_run','true')


def checksub():
   print '########################## checking ########################'
   username = ADDON.getSetting('user')
   password = ADDON.getSetting('pass')
   try:os.remove(cookie_jar)
   except:pass
   headers={'Host': THESITE,
            'Connection': 'keep-alive',
            'Origin': 'http://'+THESITE,
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'XBMC',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://'+THESITE+'/payments/login',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8'}

   TIME = time.time()- 3600
   
   data={'amember_login':username, 'amember_pass':password , 'login_attempt_id': str(TIME)}
   html = net.http_POST('http://offsidestreams.com/payments/login',data,headers).content

   if 'true' in html:
      ADDON.setSetting('resetpass','false')
      net.save_cookies(cookie_amember)
      net.set_cookies(cookie_amember)

      html = net.http_GET('http://offsidestreams.com/payments/member').content

      try:
         
          match=re.compile('<h2 id="member-main-subscriptions-head">(.+?)</h2><div class="am-block" id="member-main-subscriptions">    <h3>(.+?)</h3>').findall(html)
     
          line1 = match[0][0].strip()
          line2 = match[0][1].strip()
          line3 = ''
          addDir('No Active Subscriptions','',2006,'','','','')
          addDir('Please Login And Pay For Subscription','',2006,'','','','')
          addDir('@','',2006,'','','','')
          addDir('WWW.offsidestreams.com','',2006,'','','','')
          addDir('','',2006,'','','','')
          addDir('[COLOR red]Automatic Recurring Payments Has Now Finished[/COLOR]','',2006,'','','','')
    
      except:
            
          try:os.remove(cookie_jar)
          except:pass         
          addDir('My Active Subscriptions','',2006,'','','','')
          link=html.split('>Active Subscriptions<')[1]
          link=link.split('</ul>')[0]
          match=re.compile('<li>(.+?)-(.+?)</li>',re.DOTALL).findall(link)
          for sub , expiry in match:
             sub=sub.strip().replace('  ','').replace('<strong>','').replace('</strong>','')
             expiry=expiry.replace('\n',' ').replace('  ','')
             if 'expires' in expiry:
                expiry='[COLOR red]%s[/COLOR]' % expiry
             else:
                expiry='[COLOR green]%s[/COLOR]' % expiry                
             addDir('[COLOR white]%s - %s[/COLOR]' % (sub,expiry),'',2006,'','','','')
          
   else:     
       dialog = xbmcgui.Dialog()
       dialog.ok("Please Check Your Details", "Username : "+ADDON.getSetting('user'), "Password : "+ ADDON.getSetting('pass'), "[COLOR red]is Wrong ...[/COLOR]")
       addDir("Doesn't Seem You Have an Account OR Details",'',2006,'','','','')
       addDir('Are Incorrect','',2006,'','','','')
       addDir('','',2006,'','','','')
       addDir('------>>>>>> [COLOR red]RESET PASSWORD [/COLOR]<<<<<<-----','url',2007,'','','','')
       addDir('OR','',2006,'','','','')
       addDir('------>>>>>>   [COLOR green]Try AGAIN    [/COLOR]<<<<<<-----','url',2008,'','','','')



      
def KICKOUT():
        try:
            checksub()
            
            try:os.remove(cookie_jar)
            except:pass
        except:
            pass   




def WAIT():
        dialog = xbmcgui.Dialog()
        dialog.ok(THESITE.upper(),"If You Have Just Signed Up Please", "Allow Up To 24Hrs Before Your Active", "Come Back Soon")
        try:
            os.remove(cookie_jar)
        except:
            pass
        EXIT()        

def LOGOUT():
    net.set_cookies(cookie_jar)
    html = net.http_GET(site).content
    match=re.compile('  href="(.+?)">Log Out</a>').findall(html)[0]
    net.set_cookies(cookie_jar)
    logout = net.http_GET(match.replace('#038;','')).content
    if 'You are now logged out' in logout:
        print '===============LOGGED OUT !!==============='
        dialog = xbmcgui.Dialog()
        dialog.ok(THESITE.upper(),'', "You Are Now Logged Out", "")
        EXIT()
        
    
    

def Login():
    print '###############    LOGIN TO OSS   #####################'
    loginurl = 'http://'+THESITE+'/site/wp-login.php'
    username = ADDON.getSetting('user')
    password = ADDON.getSetting('pass')

    data     = {'pwd': password,
                                            'log': username,
                                            'wp-submit': 'Log In','redirect_to':'http://'+THESITE+'/site','testcookie':'1','rememberme':'forever'}




    headers  = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                'Host':'offsidestreams.com',
                'Origin':'http://'+THESITE,
                'Pragma':'no-cache',
                'Referer':'http://'+THESITE+'/site/wp-login.php',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}


    html = net.http_POST(loginurl, data, headers).content
  
    print html
    if os.path.exists(cookie_path) == False:
            os.makedirs(cookie_path)
    add_ontapp = ontapp1 + 1        
    ADDON.setSetting('ontapp_id_1',str(add_ontapp))       
    net.save_cookies(cookie_jar)
    net.set_cookies(cookie_jar)
    a=net.http_GET('http://'+THESITE+'/site/api/matrix/channels',headers={'User-Agent' :UA}).content
    f = open(channeljs, mode='w')
    f.write(a)
    f.close()





    

def downloadchannel():
    if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
    if sessionExpired():
        Login()
    net.set_cookies(cookie_jar)
    a=net.http_GET('http://'+THESITE+'/site/MatrixUp/site/api/matrix/channels',headers={'User-Agent' :UA}).content
    f = open(channeljs, mode='w')
    f.write(a)
    f.close()


def parse_date(dateString):
    import time
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))


def sessionExpired():
    try:
        a=open(cookie_jar).read()
        expiry=re.compile('expires="(.+?)"').findall(a)[0]
        expiry=expiry [0:len(expiry)-1]
    except:
        expiry='2000-01-01 00:00:00'


    now        = datetime.datetime.today()
 
    
    prev = parse_date(expiry)


    return (now > prev)



def server():
    net.set_cookies(cookie_jar)
    a=net.http_GET('http://'+THESITE+'/site/api/matrix/channels',headers={'User-Agent' :UA}).content
  
    print 'WEB READ'
    return a



def CheckChannels():
    update=OPEN_URL('http://xty.me/xunitytalk/addons/plugin.video.offside/update.txt')
    ADDON.setSetting('pakauth',re.compile('<pakauth>(.+?)</pakauth>').findall(update)[0]) 
    ADDON.setSetting('pakurl',re.compile('<pakurl>(.+?)</pakurl>').findall(update)[0])

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))


#

def CreatIniNow(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        a=name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' GB','').replace(' (G)','').replace(' HD','').replace(' EU','')+'='+u
        f = open(STVBINI, mode='a')
        f.write(a+'\n')
        f.close()           

def CATEGORIES():
    #CheckChannels()
    if sessionExpired():
        Login()

    try:
        link = json.loads(server())
    except:
        return checksub()

    if ontapp1 > ontapp2:
        a='[%s]\n'% PLUGIN
        f = open(STVBINI, mode='w')
        f.write(a)
        f.close()
      
    if ADDON.getSetting('genre')=='true':
        uniques=[]
        uniquesurl=[]
        data=link['categories']
        ret = ''
        for j in data:
            url = j
            name = data[j].encode("utf-8")
            
            if name not in uniques:
                uniques.append(name)
                uniquesurl.append(url)
                iconimage=image+'cat'+url+'.png'
                addDir(name,url,4,iconimage,'','','')
                
        if ontapp1 > ontapp2:                
            print '################# CREATING INI ########################'        
            data=link['channels']
            for field in data:
                id= str(field['id'])
                name= field['title'].encode("utf-8")            
                iconimage=image+id+'.png'
                CreatIniNow(name,id,2,iconimage,'False','','')
   
    else:
        data=link['channels']
        for field in data:
            id= str(field['id'])
            name= field['title'].encode("utf-8")            
            iconimage=image+id+'.png'
            addDir(name,id,2,iconimage,'False','','')
            if ontapp1 > ontapp2:
              CreatIniNow(name,id,2,iconimage,'False','','')
    
    
    if os.path.exists(cookie_jar) == True:
        try:
            import random
            text=''
            twit = 'http://twitrss.me/twitter_user_to_rss/?user=@offsidesupport'
            link = OPEN_URL(twit)
            link=link.split('<item>')[1]
            match=re.compile("<title>(.+?)</title>",re.DOTALL).findall(link)
            status = cleanHex(match[0])
            addDir('.[COLOR blue]*** [/COLOR] [COLOR orange]'+status.strip()+'[/COLOR]','url',image+'twitter.png','','','','')
        except:pass

        addDir('[COLOR cyan].Upcoming Matches[/COLOR]','url',1999,image+'upcoming.png','','','')
        addDir('[COLOR plum].Premier League Pass[/COLOR]','http://sportsmania.eu/apis/plp.php',2005,'','','','') 
        addDir('[COLOR green].On Demand Movies[/COLOR]','https://raw.githubusercontent.com/Mercutio1/MercutioPlaylist/master/OSS%20Main',5,image+'ondemand.png','','','')
        addDir('[COLOR red].Full Match Replays HD[/COLOR]','url',3,image+'fullmatch.png','','','')                
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    ADDON.setSetting('ontapp_id_2',str(ontapp1))     
    setView('movies', 'channels')
    
def GetMikey(url):
    ADDME=[]
    try:
        aa=open(paki).read()
        match=re.compile('<programCategory>(.+?)</programCategory.+?<categoryImage>(.+?)</categoryImage>').findall(aa)
        UNIQUES =[]

        for name , iconimage in match:
            if name not in UNIQUES:
                UNIQUES.append(name)        
                ADDME.append([name,paki,iconimage])
    except:pass    
          
    for NAME , URL , ICONIMAGE in ADDME:                
        addDir(NAME,URL,501,iconimage,'','','')         
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)             


def getme():
   return '|User-Agent=Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'



def SportsOnDemand(url):

       ADDME=[]
       data ={'sportsmania':'1'}
       a=net.http_POST(url,data,headers={'User-Agent':'XBMC'}).content
       import json
       link=json.loads(a)
       data=link['vod_channels']
       for field in data:
           id= str(field['channel_url'])
           name= field['channel_title'].encode("utf-8")
           if '(' in name:
              date='('+name.split('(')[1]
              name=name.split('(')[0]
              NAME='[COLOR white]%s[/COLOR] - [COLOR yellow]%s[/COLOR]' % (name,date)
           else:
              NAME='[COLOR white]%s[/COLOR]' % (name)
           addDir(NAME,id,2004,'','','','')   



def Oo0Oool(url):
 iI111iI = urllib2 . Request (url )
 IiII = urllib2 . urlopen ( iI111iI )
 iI1Ii11111iIi = IiII . read ( )
 IiII . close ( )
 return iI1Ii11111iIi   


def auth():
 import base64
 import time
 TIME = time.time()
 second= str(TIME).split('.')[0]
 first =int(second)+69296929
 token=base64.b64encode('%s@2nd2@%s' % (str(first),second))    
 DATA_URL='https://app.dynns.com/keys/activate.php?token='+token
 request = urllib2.Request(DATA_URL)
 base64string = 'ZGlsZGlsZGlsOlBAa2lzdEBu'
 request.add_header("Authorization", "Basic %s" % base64string)   
 return urllib2.urlopen(request).read()
    

           

def worldlinks(name,url):
    NAME=name
    genre=name.split('[COLOR')[0].replace('.','')
    addDir('[COLOR gold]Dont Blame Mikey1234 If They Dont Work[/COLOR]','url',2004,'','','','')
          
  
    AUTH=auth()
    aa=open(url).read()
    link=aa.split('<items>')
    for p in link:
        try:
            name=re.compile('<programTitle>(.+?)</programTitle>').findall(p)[0]
            URL=re.compile('<programURL>(.+?)</programURL>').findall(p)[0]
            iconimage=re.compile('<programImage>(.+?)</programImage>').findall(p)[0]
            if '<programCategory>'+genre+'<' in p:
                addDir(name,URL+AUTH,2004,iconimage,'','','')
        except:pass
              
    


                 
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

        
def PlayMikey(name,url,iconimage):
    if url =='none':
        dialog = xbmcgui.Dialog()
        return dialog.ok(THESITE.upper(), '',"Streams Not Active Until match Time", "")
    else:  
       if 'CHANGEME' in url:
          URL=['1600','3000','4500']
          NAME=['480P','720P','1080P']
          RES = URL[xbmcgui.Dialog().select('Please Select Resolution', NAME)]
          url=url.replace('CHANGEME',RES)+getme()
       liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
       liz.setInfo(type='Video', infoLabels={'Title':name})
       liz.setProperty("IsPlayable","true")
       liz.setPath(url)
       xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
       
def GENRES(name,url):
    if sessionExpired():
        Login()
    link = json.loads(server())
    data=link['channels']
    for field in data:
        id= field['id']
        title= field['title'].encode("utf-8")
        genre= field['cat_id']
        iconimage=image+id+'.png'
        if url == genre:
            addDir(title,id,2,iconimage,'False','','')
                
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)             
    setView('movies', 'channels')        


def OnDemand(url):    
    link = OPEN_URL(url)
    if '<message>' in link:
        message=re.compile('<message>(.+?)</message>').findall (link)
        for name in message:
            addLink(name,'url','','')

    DIRS=re.compile('<title>(.+?)</title.+?<dir>(.+?)</dir.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall (link)

    for name , url , iconimage  in DIRS:      
        addDir(name,url,6,iconimage,'','','','')        



def OnDemandLinks(url):
    link = OPEN_URL(url)
    if '<message>' in link:
       message=re.compile('<message>(.+?)</message>').findall (link)
       for name in message:
           addLink(name,'url','','')   

    LINKS=re.compile('<title>(.+?)</title.+?<link>(.+?)</link.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall (link)
    
   
    for name , url , iconimage in LINKS:
        addDir(name,url,7,iconimage,'','','','')


def GrabVK(url):
    html=OPEN_URL(url)
    r      ='"url(\d+)":"(.+?)"'
    name=[]
    url=[]
    match = re.compile(r,re.DOTALL).findall(html)
    for quality,stream in match:
        name.append(quality.replace('\\','')+'p')
        url.append(stream.replace('\/','/'))
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
    
def afdah(url):
    url= 'https://m.afdah.org/watch?v='+url

    loginurl = 'https://m.afdah.org/video_info/html5'

    v=url.split('v=')[1]
    data={'v': v}
    headers = {'host': 'm.afdah.org','origin':'https://m.afdah.org', 'referer': url,
               'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}

    first= net.http_POST(loginurl,data,headers).content

    link= json.loads(first)
    name=[]
    url=[]
    for j in link:
        name.append(j.upper())
   
        url.append(urllib.unquote(link[j][3]))

    THEURL= url[xbmcgui.Dialog().select('Please Select Resolution', name)]
    import requests
    print THEURL
    r=requests.get(THEURL,allow_redirects=False, verify=False )   

    r = requests.get(str(r.headers['Location']),allow_redirects=False, verify=False )
    return r.headers['location']


def PlayOnDemand(url):
    if 'googlevideo' in url:
        url=url
    if not 'http' in url:
        url=afdah(url)
    if 'http://vk' in url:
        url=GrabVK(url)

    if 'movreel' in url:
        import movreel
        url=movreel.solve(url)
    else:
        import urlresolver
        url=urlresolver.resolve(url)
            
         
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


    


 
def EVENTS():
    link = OPEN_URL('http://channelstatus.weebly.com/upcoming-events.html')
    link=link.split('<div class="paragraph" style="text-align:left;"')[1]
    link=link.split('>***')
    for p in link:
        try:
            DATE=re.compile('(.+?)\*').findall(p)[0]
            addDir('[COLOR cyan]'+DATE+'[/COLOR]','',2000,'','False','','')  
            match=re.compile('\[(.+?)\].+?/strong>(.+?) - (.+?)<br',re.DOTALL).findall (p)
            for TIME ,VS , CHANNEL in match:

                CHANNEL=CHANNEL.replace('beIN','beIN Sports ').replace('Sports  Sports','Sports').replace('__','')
                name= '[COLOR white][%s][/COLOR][COLOR yellow]- %s -[/COLOR][COLOR green]%s[/COLOR]' %(TIME.replace('__',''),VS.replace('__',''),CHANNEL.replace('__',''))
                addDir(name,'url',2,'','GET_EVENT','','')       
        except:pass       

 
def Show_Dialog():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), '',"All Done Try Now", "")
        
def REPLAY():
       
        xbmc.executebuiltin('ActivateWindow(videos,plugin://plugin.video.footballreplays)')

 
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
        
        
def timeout():
    quality = ADDON.getSetting('timeout')
    if quality == '0':
        return ' timeout=5 '
    elif quality == '1':
        return ' timeout=10'
    elif quality == '2':
        return ' timeout=15'
    elif quality == '3':
        return ' timeout=20'
    elif quality == '4':
        return ' timeout=25'
    elif quality == '5':
        return ' timeout=30'
    elif quality == '6':
        return ' timeout=35'
    elif quality == '7':
        return ' timeout=40'
    elif quality == '8':
        return ' timeout=45'
    elif quality == '9':
        return ' timeout=50'
        


def Show_Down():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), 'Sorry Channel is Down',"Will Be Back Up Soon", "Try Another Channel")  
    
def Show_Cover():
    dialog = xbmcgui.Dialog()
    dialog.ok(THESITE.upper(), '',"Sorry We Dont Cover This Channel", "")    

   
        
def PLAY_STREAM(name, url, iconimage, play, description):

    
    if play =='GET_EVENT':
        url=PLAY_FROM_EVENTS(name, url, iconimage, play, description)
        if not url:
            return Show_Cover()
    if sessionExpired():
        Login()
    net.set_cookies(cookie_jar)
    stream_url= net.http_GET('http://'+THESITE+'/site/api/matrix/channel/%s'%url,headers={'User-Agent' :UA}).content
    if stream_url=='':
        return Show_Down()
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url+timeout())
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 



def PLAY_FROM_EVENTS(name, url, iconimage, play, description):
    name=name.split('[COLOR green]')[1].replace('[/COLOR]','')
    nameFINAL=[]
    urlFINAL=[]
    
    if ',' in name:
        nameSelect=[]
        urlSelect=[]
        name=name.split(',')
        for p in name:
            urlSelect.append(p.strip().lower())
            nameSelect.append(p.strip())
        TITLE = urlSelect[xbmcgui.Dialog().select('Please Select Channel', nameSelect)]      
        TITLE=TITLE.replace(' ','').lower().strip()
        link = server().split('{')
        for YOYO in link:
            if TITLE in YOYO.replace(' ','').lower():
                print YOYO
                id = re.compile('"id":"(.+?)"').findall(YOYO)[0]
                NAME = re.compile('"title":"(.+?)"').findall(YOYO)[0]
                #GENRE = re.compile('"mediaid":"(.+?)"').findall(YOYO)[0]
                urlFINAL.append(id)
                nameFINAL.append('[COLOR red]%s[/COLOR]'%(NAME))
        if urlFINAL:
            return urlFINAL[xbmcgui.Dialog().select('Multiple Channels Found', nameFINAL)] 
        else:
            return False

                       
    else:
    
        NAME=name.replace(' ','').lower().strip()
        link = server().split('{')
        for YOYO in link:
                match = re.compile('"id":"(.+?)".+?"title":"(.+?)"').findall(YOYO)
                for id,NAME_ in match :
                    print NAME
                    print NAME_.replace(' ','').lower().strip()
                    if NAME in NAME_.replace(' ','').lower().strip():
                        urlFINAL.append(id)
                        nameFINAL.append('[COLOR red]%s[/COLOR]'%(NAME_))
        if urlFINAL:
            return urlFINAL[xbmcgui.Dialog().select('Multiple Channels Found', nameFINAL)] 
        else:
            return False
         
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
                          
            
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        #print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+u
        uniques=[]
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        menu=[]
        #menu.append(('[COLOR green]Reset Password[/COLOR]','XBMC.RunPlugin(%s?mode=2007&url=None)'% (sys.argv[0])))
        menu.append(('[COLOR red]Delete Cookie[/COLOR]','XBMC.RunPlugin(%s?mode=203&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        menu.append(('[COLOR cyan]Log Out[/COLOR]','XBMC.RunPlugin(%s?mode=205&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        if mode == 2 or mode==7  or mode==2004:
            if not mode == 2000:           
                    liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
          
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addLink(name,url,iconimage, fanart):
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)


def addSUBLINK(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        #print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+u
        uniques=[]
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
date=None
description=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        play=urllib.unquote_plus(params["play"])
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()
               
elif mode==2:
        PLAY_STREAM(name,url,iconimage,play,description)
        
elif mode==3:
        REPLAY()
        
elif mode==4:
        GENRES(name,url)

elif mode==5:
        OnDemand(url)


elif mode==6:
        OnDemandLinks(url)

elif mode==7:
        PlayOnDemand(url)         
        
elif mode==200:
        schedule(name,url,iconimage)
        
elif mode==201:
        fullguide(name,url,iconimage,description)
        
elif mode==202:
        Login()
        Show_Dialog()
        
elif mode==203:
        os.remove(cookie_jar)
        Show_Dialog()

elif mode==204:
        downloadchannel()      
        
elif mode==205:
        LOGOUT()


elif mode==501:
        worldlinks(name,url)  
        

elif mode==1999:
        EVENTS()        
        
elif mode==2001:
        ADDON.openSettings()

elif mode==2003:
        GetMikey(url)     
        
elif mode==2004:
        PlayMikey(name,url,iconimage)

elif mode==2005:
        SportsOnDemand(url)             

elif mode==2006:
        checksub()

elif mode==2007:
     resetpass()        

elif mode==2008:
     TryAgain()
     
else:
        #just in case mode is invalid 
        CATEGORIES()

               
xbmcplugin.endOfDirectory(int(sys.argv[1]))

