import xbmc , xbmcaddon , xbmcgui , base64 , xbmcplugin , os , shutil , urllib2 , urllib , re , extract , downloader , time , socket
from t0mm0 . common . net import Net as net
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.wizard2'
Oo0Ooo = xbmcaddon . Addon ( id = OO0o )
O0O0OO0O0O0 = xbmcaddon . Addon ( id = OO0o )
iiiii = xbmc . translatePath ( O0O0OO0O0O0 . getAddonInfo ( 'profile' ) )
ooo0OO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'icon.png' ) )
II1 = O0O0OO0O0O0 . getSetting ( 'dsusername' )
O00ooooo00 = O0O0OO0O0O0 . getSetting ( 'dspassword' )
I1IiiI = os . path . join ( os . path . join ( iiiii , '' ) , 'ds.lwp' )
socket . setdefaulttimeout ( 60 )
if II1 == '' or O00ooooo00 == '' :
 if os . path . exists ( I1IiiI ) :
  try : os . remove ( I1IiiI )
  except : pass
 IIi1IiiiI1Ii = xbmcgui . Dialog ( )
 I11i11Ii = IIi1IiiiI1Ii . yesno ( 'Update Wizard 2.0' , 'Please enter your username and password' , 'If you dont have these check your emails' , 'Or contact support for further instructions' , 'Cancel' , 'Login' )
 if I11i11Ii == 1 :
  oO00oOo = xbmc . Keyboard ( '' , 'Enter Username' )
  oO00oOo . doModal ( )
  if ( oO00oOo . isConfirmed ( ) ) :
   OOOo0 = oO00oOo . getText ( )
   Oooo000o = OOOo0
   oO00oOo = xbmc . Keyboard ( '' , 'Enter Password:' )
   oO00oOo . doModal ( )
   if ( oO00oOo . isConfirmed ( ) ) :
    OOOo0 = oO00oOo . getText ( )
    IiIi11iIIi1Ii = OOOo0
    O0O0OO0O0O0 . setSetting ( 'dsusername' , Oooo000o )
    O0O0OO0O0O0 . setSetting ( 'dspassword' , IiIi11iIIi1Ii )
II1 = O0O0OO0O0O0 . getSetting ( 'dsusername' )
O00ooooo00 = O0O0OO0O0O0 . getSetting ( 'dspassword' )
def Oo0O ( ) :
 IiI ( base64 . b64decode ( ooOo ) )
 Oo = net ( ) . http_GET ( base64 . b64decode ( ooOo ) )
 if not 'Logged in as' in Oo . content :
  IIi1IiiiI1Ii = xbmcgui . Dialog ( )
  IIi1IiiiI1Ii . ok ( 'Update Wizard 2.0' , 'An error has ocurred logging in' , 'Please check your details in addon settings' , '' )
  quit ( )
 o0O = IiiIII111iI ( base64 . b64decode ( IiII ) ) . replace ( '\n' , '' ) . replace ( '\r' , '' )
 print o0O
 iI1Ii11111iIi = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"' ) . findall ( o0O )
 for i1i1II , O0oo0OO0 , I1i1iiI1 , iiIIIII1i1iI , o0oO0 in iI1Ii11111iIi :
  oo00 ( i1i1II , O0oo0OO0 , 1 , I1i1iiI1 , iiIIIII1i1iI , o0oO0 )
 o00 ( 'movies' , 'MAIN' )
def IiiIII111iI ( url ) :
 Oo0oO0ooo = urllib2 . Request ( url )
 Oo0oO0ooo . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 Oo = urllib2 . urlopen ( Oo0oO0ooo )
 o0O = Oo . read ( )
 Oo . close ( )
 return o0O
def o0oOoO00o ( name , url , description ) :
 i1 = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
 oOOoo00O0O = xbmcgui . DialogProgress ( )
 oOOoo00O0O . create ( "Update Wizard 2.0" , "Downloading configuration files" , '' , 'Please Wait' )
 i1111 = os . path . join ( i1 , name + '.zip' )
 try :
  os . remove ( i1111 )
 except :
  pass
 downloader . download ( url , i1111 , oOOoo00O0O )
 i11 = xbmc . translatePath ( os . path . join ( 'special://' , 'home' ) )
 time . sleep ( 2 )
 oOOoo00O0O . update ( 0 , "" , "Just a little while longer :)" )
 extract . all ( i1111 , i11 , oOOoo00O0O )
 IIi1IiiiI1Ii = xbmcgui . Dialog ( )
 IIi1IiiiI1Ii . ok ( "Update Wizard 2.0" , "Configuration files prepared" , "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]" )
ooOo = 'aHR0cDovL3Rla25va2F0LmNvLnVrL2FtZW1iZXIvbWVtYmVy'
def IiI ( srDomain ) :
 I11 = net ( ) . http_GET ( srDomain ) . content
 Oo0o0000o0o0 = re . findall ( r'<input type="hidden" name="(.+?)" value="(.+?)" />' , I11 , re . I )
 oOo0oooo00o = { }
 oOo0oooo00o [ 'amember_login' ] = II1
 oOo0oooo00o [ 'amember_pass' ] = O00ooooo00
 for i1i1II , oO0o0o0ooO0oO in Oo0o0000o0o0 :
  oOo0oooo00o [ i1i1II ] = oO0o0o0ooO0oO
 net ( ) . http_GET ( base64 . b64decode ( ooOo ) )
 net ( ) . http_POST ( base64 . b64decode ( ooOo ) , oOo0oooo00o )
 net ( ) . save_cookies ( I1IiiI )
 net ( ) . set_cookies ( I1IiiI )
def oo00 ( name , url , mode , iconimage , fanart , description = '' ) :
 oo0o0O00 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description )
 oO = True
 i1iiIIiiI111 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 i1iiIIiiI111 . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 i1iiIIiiI111 . setProperty ( 'fanart_image' , fanart )
 oO = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oo0o0O00 , listitem = i1iiIIiiI111 , isFolder = False )
 return oO
def o00 ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if Oo0Ooo . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % Oo0Ooo . getSetting ( viewType ) )
IiII = 'aHR0cDovL3Rla25va2F0LmNvLnVrL2FtZW1iZXIvY29udGVudC9mL2lkLzkv'
def oooOOOOO ( ) :
 i1iiIII111ii = [ ]
 i1iIIi1 = sys . argv [ 2 ]
 if len ( i1iIIi1 ) >= 2 :
  ii11iIi1I = sys . argv [ 2 ]
  iI111I11I1I1 = ii11iIi1I . replace ( '?' , '' )
  if ( ii11iIi1I [ len ( ii11iIi1I ) - 1 ] == '/' ) :
   ii11iIi1I = ii11iIi1I [ 0 : len ( ii11iIi1I ) - 2 ]
  OOooO0OOoo = iI111I11I1I1 . split ( '&' )
  i1iiIII111ii = { }
  for iIii1 in range ( len ( OOooO0OOoo ) ) :
   oOOoO0 = { }
   oOOoO0 = OOooO0OOoo [ iIii1 ] . split ( '=' )
   if ( len ( oOOoO0 ) ) == 2 :
    i1iiIII111ii [ oOOoO0 [ 0 ] ] = oOOoO0 [ 1 ]
    if 59 - 59: oOOO0OOooOoO0Oo * II + IIi - iI11iiiI1II + O0oooo0Oo00
 return i1iiIII111ii
ii11iIi1I = oooOOOOO ( ) ; O0oo0OO0 = None ; i1i1II = None ; Ii11iii11I = None ; I1i1iiI1 = None ; o0oO0 = None
try : O0oo0OO0 = urllib . unquote_plus ( ii11iIi1I [ "url" ] )
except : pass
try : i1i1II = urllib . unquote_plus ( ii11iIi1I [ "name" ] )
except : pass
try : I1i1iiI1 = urllib . unquote_plus ( ii11iIi1I [ "iconimage" ] )
except : pass
try : Ii11iii11I = int ( ii11iIi1I [ "mode" ] )
except : pass
try : o0oO0 = urllib . unquote_plus ( ii11iIi1I [ "description" ] )
except : pass
if Ii11iii11I == None or O0oo0OO0 == None or len ( O0oo0OO0 ) < 1 : Oo0O ( )
elif Ii11iii11I == 1 : o0oOoO00o ( i1i1II , O0oo0OO0 , o0oO0 )
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 72 - 72: O00
if 61 - 61: OOOOO0
if 83 - 83: O0O00o0OOO0
if 27 - 27: IIII % o0O0 . ii1I11II1ii1i % I1i1iii - IiiI11Iiiii / ii1I1i1I
