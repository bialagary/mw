# Config Wizard By: Blazetamer 2013-2014
# Editted by TecFront
# Thanks to Blazetamer and the rest of the crew at TVADDONS.ag (XBMCHUB.com).
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,downloader,extract,time,shutil,socket
from resources.modules import main
addon_id        ='plugin.program.milowizard';
selfAddon       = xbmcaddon.Addon(id=addon_id);
datapath        = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
AddonTitle      ='Milo Wizard'; 
wizardUrl       ='http://milo.tecfront.ca/';
SiteDomain      ='TECFRONT.CA'; 
TeamName        ='TecFront';
user            = selfAddon.getSetting('username');
passw           = selfAddon.getSetting('password');
cookie_file     = os.path.join(os.path.join(datapath,''), 'ds.lwp');
try:        from addon.common.addon import Addon
except:
    try:    from t0mm0.common.addon import Addon
    except: from t0mm0_common_addon import Addon
try:        from addon.common.net   import Net
except:
    try:    from t0mm0.common.net   import Net
    except: from t0mm0_common_net   import Net
addon=main.addon; net=Net(); settings=xbmcaddon.Addon(id=addon_id); net.set_user_agent('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'); 

# Get login credentials if add-ons configurations aren't set
socket.setdefaulttimeout(60)
if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('Milo Wizard', 'Please enter your login credentials.','Do not have your login information?','Contact sales@tecfront.ca','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter username:')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            username=search
            keyb = xbmc.Keyboard('', 'Enter password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                search = keyb.getText()
                password=search
                selfAddon.setSetting('username',username)
                selfAddon.setSetting('password',password)
user = selfAddon.getSetting('username')
passw = selfAddon.getSetting('password')

#==========================Help WIZARD=====================================================================================================
def HELPCATEGORIES():
    if ((XBMCversion['Ver'] in ['','']) or (int(XBMCversion['two']) < 12)) and (settings.getSetting('bypass-xbmcversion')=='false'):
        eod(); addon.show_ok_dialog(["Compatibility Issue: Outdated Kodi Setup","Please upgrade to a newer version of XBMC first!","Visit %s for Support!"%SiteDomain],title="XBMC "+XBMCversion['Ver'],is_error=False); DoA('Back'); 
    else:
        setCookie('http://milo.tecfront.ca/member/login')
        response = net.http_GET('http://milo.tecfront.ca/member/login')
        if not 'Logged in as' in response.content:
            dialog = xbmcgui.Dialog()
            dialog.ok('Milo Wizard', 'An error has ocurred logging in','Please check your details in addon settings','')
            quit()
        link = OPEN_URL('http://milo.tecfront.ca/member/content/f/id/1/').replace('\n','').replace('\r','')
        print link
        match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description,filetype in match:
            #if 'status' in filetype:
                #main.addHELPDir(name,url,'wizardstatus',iconimage,fanart,description,filetype)
            #else:    
                main.addHELPDir(name,url,'helpwizard',iconimage,fanart,description,filetype)
                #print [name,url]
        main.AUTO_VIEW('movies')
        #main.addHELPDir('Testing','http://www.firedrive.com/file/################','helpwizard',iconimage,fanart,description,filetype) ## For Testing to test a url with a FileHost.
        ## ### ## \/ OS Check and Button Suggestions \/ ## ### ## 
        #if   sOS.lower() in ['win32']: SuggestButton('Windows')    ## Windows.
        #elif sOS.lower() in ['linux']: SuggestButton('Linux')     ## May include android stuff as well.
        #elif sOS.lower() in ['mac','osx']: SuggestButton('MAC')   ## 
        #elif sOS.lower() in ['android']: SuggestButton('Android') ## 
        ## ### ## 
def setCookie(srDomain):
    html = net.http_GET(srDomain).content
    r = re.findall(r'<input type="hidden" name="(.+?)" value="(.+?)" />', html, re.I)
    post_data = {}
    post_data['amember_login'] = user
    post_data['amember_pass'] = passw
    for name, value in r:
        post_data[name] = value
    net.http_GET('http://milo.tecfront.ca/member/login')
    net.http_POST('http://milo.tecfront.ca/member/login',post_data)
    net.save_cookies(cookie_file)
    net.set_cookies(cookie_file)
def SuggestButton(msg): addon.show_ok_dialog(["By the looks of your operating system","we suggest clicking: ",""+msg],title="OS: "+sOS,is_error=False); 
def OPEN_URL(url): req=urllib2.Request(url); req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'); response=urllib2.urlopen(req); link=response.read(); response.close(); return link
def FireDrive(url):
    if ('http://m.firedrive.com/file/' not in url) and ('https://m.firedrive.com/file/' not in url) and ('http://www.firedrive.com/file/' not in url) and ('http://firedrive.com/file/' not in url) and ('https://www.firedrive.com/file/' not in url) and ('https://firedrive.com/file/' not in url): return url ## contain with current url if not a filedrive url.
    #else:
    try:
        if 'https://' in url: url=url.replace('https://','http://')
        html=net.http_GET(url).content
        if ">This file doesn't exist, or has been removed.<" in html: return "[error]  This file doesn't exist, or has been removed."
        elif ">File Does Not Exist | Firedrive<" in html: return "[error]  File Does Not Exist."
        elif "404: This file might have been moved, replaced or deleted.<" in html: return "[error]  404: This file might have been moved, replaced or deleted."
        #print html; 
        data={}; r=re.findall(r'<input\s+type="\D+"\s+name="(.+?)"\s+value="(.+?)"\s*/>',html);
        for name,value in r: data[name]=value
        #print data; 
        if len(data)==0: return '[error]  input data not found.'
        html=net.http_POST(url,data,headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0','Referer': url,'Host': 'www.firedrive.com'}).content
        #print html
        r=re.search('<a\s+href="(.+?)"\s+target="_blank"\s+id=\'top_external_download\'\s+title=\'Download This File\'\s*>',html)
        if r: 
            print urllib.unquote_plus(r.group(1)); 
            return urllib.unquote_plus(r.group(1))
        else: return url+'#[error]'
    except: return url+'#[error]'
def HELPWIZARD(name,url,description,filetype):
    path=xbmc.translatePath(os.path.join('special://home','addons','packages'))
    confirm=xbmcgui.Dialog()
    if confirm.yesno(TeamName,"Would you like %s to "%SiteDomain,"customize your add-on selection? "," "):
        dp=xbmcgui.DialogProgress(); dp.create(AddonTitle,"Downloading ",'','Please Wait')
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        ### ## File Host Handling ## \/
        url=FireDrive(url)
        #url=SockShare(url)
        if '[error]' in url: print url; dialog=xbmcgui.Dialog(); dialog.ok("Error!",url); return
        else: print url
        ### ## File Host Handling ## /\
        downloader.download(url,lib,dp)
        #return ## For Testing 2 Black Overwrite of stuff. ##
    #if filetype == 'addon':
        #addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
    #elif filetype == 'media':
        #addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
#attempt Shortcuts
    #elif filetype == 'main':
        addonfolder=xbmc.translatePath(os.path.join('special://','home'))
        time.sleep(2)
        dp.update(0,"","Extracting Zip Please Wait")
        print '======================================='; print addonfolder; print '======================================='
        extract.all(lib,addonfolder,dp)

        proname=xbmc.getInfoLabel("System.ProfileName")

        xbmc.executebuiltin('UnloadSkin()');
        xbmc.executebuiltin('ReloadSkin()');

        # xxx
        if filetype == "xxx":
            link = OPEN_URL(wizardUrl+'xxxsettings.txt')
            strings = re.compile('string={(.+?)}').findall(link)
            for string in strings: xbmc.executebuiltin("Skin.SetString(%s)" % string)
        else:
        # skinsettings.txt
            link = OPEN_URL(wizardUrl+'skinsettings.txt')
            strings = re.compile('string={(.+?)}').findall(link)
            for string in strings: xbmc.executebuiltin("Skin.SetString(%s)" % string)

        xbmc.executebuiltin('UnloadSkin()');
        xbmc.executebuiltin('ReloadSkin()');
        xbmc.executebuiltin("LoadProfile(%s)" % proname)
        xbmc.sleep(1000)
        dialog = xbmcgui.Dialog()
        dialog.ok("Success!","Installation complete!","[COLOR gold]Brought to you by %s[/COLOR]"%SiteDomain)
            
        ##
def WIZARDSTATUS(url):
    link=OPEN_URL(url).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,filetype in match: header="[B][COLOR gold]"+name+"[/B][/COLOR]"; msg=(description); TextBoxes(header,msg)
def TextBoxes(heading,anounce):
        class TextBox():
            WINDOW=10147; CONTROL_LABEL=1; CONTROL_TEXTBOX=5
            def __init__(self,*args,**kwargs):
                xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
                self.win=xbmcgui.Window(self.WINDOW) # get window
                xbmc.sleep(500) # give window time to initialize
                self.setControls()
            def setControls(self):
                self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
                try: f=open(anounce); text=f.read()
                except: text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText (str(text))
                return
        TextBox()
#==========
def DoA(a): xbmc.executebuiltin("Action(%s)" % a) #DoA('Back'); # to move to previous screen.
def eod(): addon.end_of_directory()
#==========OS Type & XBMC Version===========================================================================================
def get_xbmc_os():
    try: xbmc_os = str(os.environ.get('OS'))
    except:
        try: xbmc_os = str(sys.platform)
        except: xbmc_os = "unknown"
    return xbmc_os
XBMCversion={}; XBMCversion['All']=xbmc.getInfoLabel("System.BuildVersion"); XBMCversion['Ver']=XBMCversion['All']; XBMCversion['Release']=''; XBMCversion['Date']=''; 
if ('Git:' in XBMCversion['All']) and ('-' in XBMCversion['All']): XBMCversion['Date']=XBMCversion['All'].split('Git:')[1].split('-')[0]
if ' ' in XBMCversion['Ver']: XBMCversion['Ver']=XBMCversion['Ver'].split(' ')[0]
if '-' in XBMCversion['Ver']: XBMCversion['Release']=XBMCversion['Ver'].split('-')[1]; XBMCversion['Ver']=XBMCversion['Ver'].split('-')[0]
if len(XBMCversion['Ver']) > 1: XBMCversion['two']=str(XBMCversion['Ver'][0])+str(XBMCversion['Ver'][1])
else: XBMCversion['two']='00'
if len(XBMCversion['Ver']) > 3: XBMCversion['three']=str(XBMCversion['Ver'][0])+str(XBMCversion['Ver'][1])+str(XBMCversion['Ver'][3])
else: XBMCversion['three']='000'
sOS=str(get_xbmc_os()); 
print [['Version All',XBMCversion['All']],['Version Number',XBMCversion['Ver']],['Version Release Name',XBMCversion['Release']],['Version Date',XBMCversion['Date']],['OS',sOS]]
#==========END HELP WIZARD==================================================================================================
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]; cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&'); param={}
                for i in range(len(pairsofparams)):
                        splitparams={}; splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param
params=get_params(); url=None; name=None; mode=None; year=None; imdb_id=None
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    filetype=urllib.unquote_plus(params["filetype"])
except: pass
try:        url=urllib.unquote_plus(params["url"])
except: pass
try:        name=urllib.unquote_plus(params["name"])
except: pass
try:        mode=urllib.unquote_plus(params["mode"])
except: pass
try:        year=urllib.unquote_plus(params["year"])
except: pass
print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "Year: "+str(year)
if mode==None or url==None or len(url)<1: HELPCATEGORIES()
elif mode=="wizardstatus": print""+url; items = WIZARDSTATUS(url)
elif mode=='helpwizard': HELPWIZARD(name,url,description,filetype)
xbmcplugin.endOfDirectory(int(sys.argv[1]))        
