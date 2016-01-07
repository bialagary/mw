import urllib , urllib2 , sys , re , xbmcplugin , xbmcgui , xbmcaddon , xbmc , os
if 64 - 64: i11iIiiIii
import json
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
IiII1IiiIiI1 = xbmcaddon . Addon ( id = 'plugin.video.pakhind' )
if 40 - 40: oo * OoO0O00
if 2 - 2: ooOO00oOo % oOo0O0Ooo * Ooo00oOo00o . oOoO0oo0OOOo + iiiiIi11i
if 24 - 24: II11iiII / OoOO0ooOOoo0O + o0000oOoOoO0o * i1I1ii1II1iII % oooO0oo0oOOOO
O0oO = xbmc . translatePath ( IiII1IiiIiI1 . getAddonInfo ( 'profile' ) )
IIi1IiiiI1Ii = os . path . join ( O0oO , "world" )
o0oO0 = os . path . join ( O0oO , "pak" )
if 100 - 100: i11Ii11I1Ii1i
if 67 - 67: iiI1iIiI . i1I1ii1II1iII * ooOO00oOo . i11iIiiIii / iiiiIi11i % II111iiii
def Ooo00O0 ( ) :

 oo0 = open ( o0oO0 ) . read ( )
 Oooo00OOo000 = json . loads ( oo0 )
 O0I11i1i11i1I = [ ]
 for Iiii in Oooo00OOo000 :
  OOO0O = Iiii [ 'categoryName' ]
  oo0ooO0oOOOOo = Iiii [ 'categoryImageLink' ]
  if OOO0O not in O0I11i1i11i1I :
   O0I11i1i11i1I . append ( OOO0O )
   oO000OoOoo00o ( OOO0O , o0oO0 , 1 , oo0ooO0oOOOOo , '' )
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_VIDEO_TITLE )
 if 31 - 31: II111iiii + ooOO00oOo . i11Ii11I1Ii1i
 if 68 - 68: oo - i11iIiiIii - ooOO00oOo / II11iiII - ooOO00oOo + i1IIi
 if 48 - 48: OoooooooOO % Ooo00oOo00o . oo - o0000oOoOoO0o % i1IIi % OoooooooOO
 if 3 - 3: i1I1ii1II1iII + O0
def I1Ii ( name , url , iconimage ) :
 opoooII='?token='+Oo0Oool()      
 o0oOo0Ooo0O = name
 import json
 oo0 = open ( o0oO0 ) . read ( )
 Oooo00OOo000 = json . loads ( oo0 )
 for Iiii in Oooo00OOo000 :
  iconimage = Iiii [ 'channelImageLink' ]
  name = Iiii [ 'channelName' ]
  url = Iiii [ 'channelLink' ]+opoooII
  if o0oOo0Ooo0O in Iiii [ 'categoryName' ] :
   OO00O0O0O00Oo ( name , url , iconimage )
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_VIDEO_TITLE )
 if 25 - 25: Ooo00oOo00o % II111iiii - II111iiii . II111iiii
 if 32 - 32: i1IIi . OoOO0ooOOoo0O % ooOO00oOo . Ooo00oOo00o

def Oo0Oool():
 #import base64
 return 'ZmI0MzFiMTMwNzc5Y2RkNDM2NTZlODdkNzA0YThhMWY6MTQzNjY5NTk5Ng=='
def i1I111I ( ) :
 i11I1IIiiIi = [ ]
 IiIiIi = sys . argv [ 2 ]
 if len ( IiIiIi ) >= 2 :
  II = sys . argv [ 2 ]
  iI = II . replace ( '?' , '' )
  if ( II [ len ( II ) - 1 ] == '/' ) :
   II = II [ 0 : len ( II ) - 2 ]
  iI11iiiI1II = iI . split ( '&' )
  i11I1IIiiIi = { }
  for O0oooo0Oo00 in range ( len ( iI11iiiI1II ) ) :
   Ii11iii11I = { }
   Ii11iii11I = iI11iiiI1II [ O0oooo0Oo00 ] . split ( '=' )
   if ( len ( Ii11iii11I ) ) == 2 :
    i11I1IIiiIi [ Ii11iii11I [ 0 ] ] = Ii11iii11I [ 1 ]
    if 72 - 72: II11iiII
 return i11I1IIiiIi
 if 63 - 63: o0000oOoOoO0o
def oO000OoOoo00o ( name , url , mode , iconimage , description ) :
 O00 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description )
 iII11i = True
 O0O00o0OOO0 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 O0O00o0OOO0 . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description } )
 xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O00 , listitem = O0O00o0OOO0 , isFolder = True )
 return iII11i
 if 27 - 27: O0 % i1IIi * iiiiIi11i + i11iIiiIii + OoooooooOO * i1IIi
 if 80 - 80: OoOO0ooOOoo0O * i11iIiiIii / i11Ii11I1Ii1i
def OO00O0O0O00Oo ( name , url , iconimage ) :
 O0O00o0OOO0 = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 O0O00o0OOO0 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 O0O00o0OOO0 . setProperty ( "IsPlayable" , "true" )
 iII11i = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = O0O00o0OOO0 , isFolder = False )
 if 9 - 9: o0000oOoOoO0o + iiiiIi11i % o0000oOoOoO0o + i1IIi . II11iiII
 if 31 - 31: Ooo00oOo00o + OoOO0ooOOoo0O + OoOO0ooOOoo0O / II111iiii
def iiI1 ( content , viewType ) :
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if IiII1IiiIiI1 . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % IiII1IiiIiI1 . getSetting ( viewType ) )
  if 19 - 19: OoOO0ooOOoo0O + iiI1iIiI
  if 53 - 53: OoooooooOO . i1IIi
II = i1I111I ( )
ii1I1i1I = None
OOO0O = None
OOoo0O0 = None
oo0ooO0oOOOOo = None
iiiIi1i1I = None
if 80 - 80: oOo0O0Ooo - ooOO00oOo
if 87 - 87: iiiiIi11i / OoOO0ooOOoo0O - i1IIi * II11iiII / OoooooooOO . O0
try :
 ii1I1i1I = urllib . unquote_plus ( II [ "url" ] )
except :
 pass
try :
 OOO0O = urllib . unquote_plus ( II [ "name" ] )
except :
 pass
try :
 oo0ooO0oOOOOo = urllib . unquote_plus ( II [ "iconimage" ] )
except :
 pass
try :
 OOoo0O0 = int ( II [ "mode" ] )
except :
 pass
try :
 iiiIi1i1I = urllib . unquote_plus ( II [ "description" ] )
except :
 pass
 if 1 - 1: II111iiii - OoOO0ooOOoo0O / OoOO0ooOOoo0O
print "Mode: " + str ( OOoo0O0 )
print "URL: " + str ( ii1I1i1I )
print "Name: " + str ( OOO0O )
print "IconImage: " + str ( oo0ooO0oOOOOo )
if 46 - 46: o0000oOoOoO0o * II11iiII - ooOO00oOo * iiiiIi11i - i11Ii11I1Ii1i
if 83 - 83: OoooooooOO
if 31 - 31: II111iiii - II11iiII . i11Ii11I1Ii1i % oOo0O0Ooo - O0
if OOoo0O0 == None or ii1I1i1I == None or len ( ii1I1i1I ) < 1 :
 print ""
 Ooo00O0 ( )
 if 4 - 4: II111iiii / iiI1iIiI . i1I1ii1II1iII
elif OOoo0O0 == 1 :
 print "" + ii1I1i1I
 I1Ii ( OOO0O , ii1I1i1I , oo0ooO0oOOOOo )
 if 58 - 58: II11iiII * i11iIiiIii / oOo0O0Ooo % i11Ii11I1Ii1i - oOoO0oo0OOOo / iiiiIi11i
 if 50 - 50: oo
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
