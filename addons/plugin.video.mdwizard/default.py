import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time
from addon.common.addon import Addon
from addon.common.net import Net
 

###THANK YOU TO THE PEOPLE THAT ORIGINALY WROTE SOME OF THIS CODE WITHOUT YOU I STILL PROBABLY WOULDNT HAVE A CLUE WHERE TO START###

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id = 'plugin.video.mdwizard'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonTitle="MD Wizard" 
net = Net()
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.1.4"
DBPATH = xbmc.translatePath('special://database')
TNPATH = xbmc.translatePath('special://thumbnails');
PATH = "Mucky Ducks Wizard"            
BASEURL = "http://kodimediaportal.ml"
H = 'http://'



exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("NDQgMTY5KCk6CgkzMSgnN2UgMTYxJywnMWQnLDEsMmUrJzdlLjMwJyxlLCcnKQoJMzEoJzEzMiAxNGEnLDFjOSsnLzE5Yi8xNTcuMWEyPzE2Zj0zLjAnLDE5LDJlKydjZi4zMCcsZSwnJykKCTMxKCdlOCAxNmMnLDFjOSwyLDJlKydlOC4zMCcsZSwnJykKCTMxKCcyNScsMWM5LDMsMmUrJzI1LjMwJyxlLCcnKQoJMzEoJzU2IDc4IDJmJywxYzksNCwyZSsnMmYuMzAnLGUsJycpCiMJMzEoJzEyZSBmMyBkOCcsJ2U4JywxNSwyZSsnYTguMzAnLGUsJycpCgk1MignNjAnLCAnOWQnKQoKNDQgMjUoKToKCTFjNygnMzYgOGMnLCcxZCcsMTQsMmUrJzI1LjMwJyxlLCcnKQoJMWM3KCczNiA2YicsJzFkJyw2LDJlKycyNS4zMCcsZSwnJykKCTFjNygnMTY3IGIxJywnMWQnLDEwLDJlKycyNS4zMCcsZSwnMTViIDEyMiAxOWQgMTU5JykKIwkzMSgnMTgwIDE0MiBmMCAxNjAgYTcnLCcxZCcsOSwyZSsnMS4xOWEnLGUsJzFhZSAxMWMgZmQnKQoJMWM3KCdhYiAxYjYgMWMwJywnMWQnLDEyLDJlKycyNS4zMCcsZSwnJykKCTFjNygnYjQgZjYgMzYgZWUuMTc2JmViIDEyYycsJzFkJywxMywyZSsnMjUuMzAnLGUsJzE3YSAxNzEgMTgyIDEyNSAxODIgMTIwIDFjMSAxMWUgMTBhIGVjIDE0NyAxOTYgMTg2IDFhNyAxYzggMTM3IDhhLmRiJykKCTUyKCc2MCcsICc5ZCcpCgoKNDQgZDYoKToKCTFjNygnYWIgNTYgMmYnLDFjOSw4LDJlKycyZi4zMCcsZSwnJykKCTFjNygnYzggMmYnLDFjOSsnLzQxL2M5LjViJyw3LDJlKycyZi4zMCcsZSwnJykKCTFjNygnYmQgMmYnLDFjOSsnLzQxLzE0Ni41YicsNywyZSsnMmYuMzAnLGUsJycpCgkxYzcoJzkzIDJmJywxYzkrJy80MS9lNi41YicsNywyZSsnMmYuMzAnLGUsJycpCgkxYzcoJ2NiIDJmJywxYzkrJy80MS8xNTMuNWInLDcsMmUrJzJmLjMwJyxlLCcnKQoJMWM3KCdkMCA1MCAxODcnLDFjOSsnLzQxLzEwYy41YicsNywyZSsnMmYuMzAnLGUsJycpCgkxYzcoJ2QwIDUwIDE4OCcsMWM5KycvNDEvMTBiLjViJyw3LDJlKycyZi4zMCcsZSwnJykKCTFjNygnMzYgMmYnLDFjOSwxMSwyZSsnMmYuMzAnLGUsJycpCgk1MignNjAnLCAnOWQnKQoKNDQgZjIoKToKCTMxKCcxMWIgZjMgZDggMWFiIDE2NCA4ZSBmNScsMWM5KycvNDEvOTIvMTAzLTk3LjEzYScsNSwyZSsnYTguMzAnLGUsJycpCgkxYzcoJzk1IDE1YSAxOTkgNzgnLDFjOSsnLzQxLzkyLzEwNy41YicsMTcsMmUrJ2E4LjMwJyxlLCcnKQoJMWM3KCc5NSAxMTguMTlmIDE0MyAxNTgnLCcxNzg6Ly9lZi4xMjQuMWEzLzEyMy4xOWMnLDE2LDJlKydhOC4zMCcsZSwnJykKCTFjNygnMTY2IGYzIGZlJywnMWQnLDE4LDJlKydhOC4zMCcsZSwnJykKCQoKCjQ0IDE0YigpOgoJNDYgPSA2YSgxYzkrMWIwKzFhOSkuNjUoJ1wxYmInLCcnKS42NSgnXDFiNScsJycpCgk1NSA9IGY5LjcxKCcxYT0iKC4rPykiLis/MTc1PSIoLis/KSIuKz8xN2I9IiguKz8pIi4rP2U1PSIoLis/KSIuKz84Nj0iKC4rPykiJykuNzQoNDYpCgljIDFhLDFkLDQyLDQ3LDFjIDE5NCA1NToKCQkJMzEoMWEsMWQsNSw0Miw0NywxYykKCTUyKCc2MCcsICc5ZCcpCgkKCjQ0IDdlKCk6Cgk1YToKCQk0NiA9IDZhKDFkMCsxYmQrMWJhKzFhOSkuNjUoJ1wxYmInLCcnKS42NSgnXDFiNScsJycpCgkJNTUgPSBmOS43MSgnMWE9IiguKz8pIi4rPzE3NT0iKC4rPykiLis/MTdiPSIoLis/KSIuKz9lNT0iKC4rPykiLis/ODY9IiguKz8pIicpLjc0KDQ2KQoJCWMgMWEsMWQsNDIsNDcsMWMgMTk0IDU1OgoJCQkzMSgxYSwxZCw1LDQyLDQ3LDFjKQoJMmM6IDIzCgk1MignNjAnLCAnZmYnKQoKCjQ0IDEyZigxYSwxZCwxYyk6CgkxYjQgPSAxYi4xZDEoMWNjLjFiNC4xODEoJzZjOi8vNTgvOTcnLCdhMicpKQoJZGMgPSAxMzEuYmEoKQoJZGMuMTNkKCIxNjMgMTY1IDM4IiwiZDcgIiwnJywgJzY0IGY3JykKCWNlPTFjYy4xYjQuMTgxKDFiNCwgMWErJy4xM2EnKQoJNWE6CgkgICAxY2MuNmUoY2UpCgkyYzoKCSAgIDIzCgk4OS4xMTEoMWQsIGNlLCBkYykKCTY4ID0gMWIuMWQxKDFjYy4xYjQuMTgxKCc2YzovLycsJzU4JykpCgkxODkuMTZlKDIpCglkYy4xMzkoMCwiIiwgImUyIDE5NSA2NCBmNyIpCgkyOSAnPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09JwoJMjkgNjgKCTI5ICc9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0nCgkxMTcuMTQ4KGNlLDY4LGRjKQoJMWI5ID0gMTMxLjFjZCgpCgkxYjkuNmYoIjcwIDRmIiwgIjY0IGUzIDEzNyAxNmIgYjUgMTBlIDE1MSIsIlsyYiA5MV04MSBiNSBkMSAxNDAgNzAgNGZbLzJiXSIpCgoKCjQ0IDE3ZSgxZCk6Cgk0NiA9IDZhKDFkKQoJNTU9ZjkuNzEoJzwxMTIgMWJlPSIuKz8iPjxhIGEwPSIoLis/KSI+KC4rPyk8L2E+PC8xMTI+JykuNzQoNDYpCgljIDFkLDFhIDE5NCA1NToKCQkxMDYgPSAnMTY4PTExLjAnCgkJMWEgPSAxYS42NSgnJjFhODsnLCcmJykKCQkxY2EgMTA2IDE5ZSAxOTQgMWQ6CgkJCTMxKCdbMmIgMTcyXSUxY2VbLzJiXScgJTFhLDFkLDIwLDJlKydjZi4zMCcsZSwnJykKCTU5Ljc1KCBjMD0xMzYoIDEzOC4xMDlbIDEgXSApLCA4ND01OS40YiApCgo0NCAxNWYoMWQpOgoJNDYgPSA2YSgxZCkKCTVhOgoJCTU1PWY5LjcxKCcmODM7MWEmODI7KC4rPykmODM7MWEmODI7PDEwOCAvPiY4MzsxZCY4Mjs8YSBhMD0iKC4rPykiIGFhPSI3OSIgOTY9IjhmIj4uKz88L2E+JjgzOzFkJjgyOzwxMDggLz4mODM7MTA0JjgyOzxhIGEwPSIoLis/KSIgYWE9Ijc5IiA5Nj0iOGYiPi4rPzwvYT4mODM7MTA0JjgyOzwxMDggLz4mODM7NDcmODI7PGEgYTA9IiguKz8pIiBhYT0iNzkiIDk2PSI4ZiI+Lis/PC9hPiY4Mzs0NyY4Mjs8MTA4IC8+JjgzOzFjJjgyOyguKz8pJjgzOzFjJjgyOycpLjc0KDQ2KQoJCWMgMWEsMWQsNDIsNDcsMWMgMTk0IDU1OgoJCQkzMSgxYSwxZCw1LDQyLDQ3LDFjKQoJMmM6IDIzCgk1MignNjAnLCAnZmYnKQoJNTkuNzUoIGMwPTEzNiggMTM4LjEwOVsgMSBdICksIDg0PTU5LjRiICkKCgojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwojIyMJZjAgYTcmOGUJICAjIyMKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCjQ0IGM1KCk6CgkxYi43MyggJzlhJyApCgkxYi43MyggJzlmJyApCgkxYjkgPSAxMzEuMWNkKCkKCTFiOS42ZigiODcgMzgiLCAnJywnCQkJCQkJCQkgYjEgZTEgOiknLCAiCQkJCQkJICBbMmIgYzddODEgYjUgZDEgMTQwIDg3IDM4Wy8yYl0iKQoJNTMKCQojNDQgYjYoMWQpOgojCTI5ICcjIyMnKzE3NysnIC0gNDggZmMuMTc2ICMjIycKIwkxYjQgPSAxYi4xZDEoMWNjLjFiNC4xODEoJzZjOi8vMTBkJywnJykpCiMJNjY9MWNjLjFiNC4xODEoMWI0LCAnMTBmLmRiJykKIwk1YToKIwkJMWNjLjZlKDY2KQojCQkxYjkgPSAxMzEuMWNkKCkKIwkJMjkgJz09PSA4NyAzOCAtIDQ4CScrMzkoNjYpKycJPT09JwojCQkxYjkuNmYoMTc3LCAiCSAgIDc3IDEwMi5kYiA4OCA2NCBkMyBiNSAxMGUgMTUwIikKIwkyYzoKIwkJMWI5ID0gMTMxLjFjZCgpCiMJCTFiOS42ZigxNzcsICIJICAgMTU2IDE5MyBiNSA3NyIpCiMJNTMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiMjIwlmNCBmMCBhNyY4ZSAgIyMjCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCgojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwojIyMJIDM2IGQyCQkjIyMKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCjQ0IGM2KCk6Cgk1YToKCQkxY2EgMWNjLjFiNC4yNChjMik9PTNmOgoJCQkxYjkgPSAxMzEuMWNkKCkKCQkJMWNhIDFiOS4yMigiMWM4IDhkIiwgIlsyYiBjN11bYl0jIyMjIyMjIyMjMTIxIGI0IGY2IyMjIyMjIyMjI1svYl1bLzJiXSIsICIxMDUgMTE0IDEyOCAxNzMgOTAgMTRjIDRlIGRmLmRiIiwgIjE5NyAzZCAxOTAgM2QgMzIgMWIxIDFiNyAxMjY/IDEwNSAxYTYgMWE1IGJlIDEzMyIpOgoJCQkJYyAxY2YsIDFjMiwgMThkIDE5NCAxY2MuMzQoYzIpOgoJCQkJCTVlID0gMAoJCQkJCTVlICs9IDQ1KDE4ZCkKCQkJCQkxY2EgNWUgPiAwOgkJCQkKCQkJCQkJYyBmIDE5NCAxOGQ6CgkJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCQkJICAgCgkJY2EgPSAxY2MuMWI0LjE4MSgxNDUsIjhhLmRiIikJCQkgICAKCQkxY2MuMWM1KGNhKQoJCTFiOS42ZigiMTE2IDcwIiwgIjY0IDExZiA3MCAxYjEgMTFkIDkwIDExYSIpCgkyYzogCgkJMWI5ID0gMTMxLjFjZCgpCgkJMWI5LjZmKDE3NywgImU3IDY5IDhkIDFiYyBkZCA3MCA0ZiAxOGYgYTYiKQoJNTMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiMjIwkgMTNiIDM2IGQyCSMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKIyMjCSAgIDM2IDhjCSAgICMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKNDQgZDUoMWQpOgoJMjkgJyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwkgICA0OCAxMTMgOGMJCQkgIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjJwoJNGMgPSAxY2MuMWI0LjE4MSgxYi4xZDEoJzZjOi8vNTgnKSwgJzFjNicpCgkxY2EgMWNjLjFiNC4yNCg0Yyk9PTNmOgkKCQljIDFjZiwgMWMyLCAxOGQgMTk0IDFjYy4zNCg0Yyk6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CgkKCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJMWNhIDFiOS4yMigiMWM4IDcwIDI3IDI2IiwgMzkoNWUpICsgIiAxOGQgMmEiLCAiNjcgM2QgMzIgMWIxIDdmIDNhPyIpOgoJCQkJCgkJCQkJYyBmIDE5NCAxOGQ6CgkJCQkJCTVhOgoJCQkJCQkJMWNjLjFjNSgxY2MuMWI0LjE4MSgxY2YsIGYpKQoJCQkJCQkyYzoKCQkJCQkJCTIzCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTVhOgoJCQkJCQkJMWYuMWUoMWNjLjFiNC4xODEoMWNmLCBkKSkKCQkJCQkJMmM6CgkJCQkJCQkyMwoJCQkJCQkKCQkJMzU6CgkJCQkyMwoJMWNhIDFiLjk5KCcxMmQuMTEwLmJmJyk6CgkJN2QgPSAxY2MuMWI0LjE4MSgnL2FkLzE1NS9jMy9iMy9jZC9hZS9lMC8nLCAnZDknKQoJCQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDdkKToKCQkJNWUgPSAwCgkJCTVlICs9IDQ1KDE4ZCkKCQkKCQkJMWNhIDVlID4gMDoKCgkJCQkxYjkgPSAxMzEuMWNkKCkKCQkJCTFjYSAxYjkuMjIoIjFjOCBiZiAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIDE5NCAnZDknIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgkJN2MgPSAxY2MuMWI0LjE4MSgnL2FkLzE1NS9jMy9iMy9jZC9hZS9lMC8nLCAnNzInKQoJCQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDdjKToKCQkJNWUgPSAwCgkJCTVlICs9IDQ1KDE4ZCkKCQkKCQkJMWNhIDVlID4gMDoKCgkJCQkxYjkgPSAxMzEuMWNkKCkKCQkJCTFjYSAxYjkuMjIoIjFjOCBiZiAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIDE5NCAnNzInIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgkJCSAgIyA1MSAxYjQgMWIxIDE1ZSBmOCAxYzYgMThkCgkJCQkJCQkgCgoJIyA1MSAxYjQgMWIxIDE4NCAxYmYgMTdjIDFjNiAxOGQKCTU0ID0gMWNjLjFiNC4xODEoMWIuMWQxKCc2YzovLzJkLzFjMy8zNy40MC5kNC8xYzYnKSwgJycpCgkxY2EgMWNjLjFiNC4yNCg1NCk9PTNmOgkKCQljIDFjZiwgMWMyLCAxOGQgMTk0IDFjYy4zNCg1NCk6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CgkKCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJMWNhIDFiOS4yMigiMWM4IDFhMSAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgkJCQkKCQkJCSMgNTEgMWI0IDFiMSAxNTQgMWM2IDE4ZAoJM2M9IDFjYy4xYjQuMTgxKDFiLjFkMSgnNmM6Ly8yZC8xYzMvMzcuNDAuMWFjLzFjNicpLCAnJykKCTFjYSAxY2MuMWI0LjI0KDNjKT09M2Y6CQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDNjKToKCQkJNWUgPSAwCgkJCTVlICs9IDQ1KDE4ZCkKCQkKCQkjIDMzIDE4ZCA0ZSAzZSAyOCAxYjEgN2YKCQkJMWNhIDVlID4gMDoKCQoJCQkJMWI5ID0gMTMxLjFjZCgpCgkJCQkxY2EgMWI5LjIyKCIxYzggMTU0IDI3IDI2IiwgMzkoNWUpICsgIiAxOGQgMmEiLCAiNjcgM2QgMzIgMWIxIDdmIDNhPyIpOgoJCQkJCgkJCQkJYyBmIDE5NCAxOGQ6CgkJCQkJCTFjYy4xYzUoMWNjLjFiNC4xODEoMWNmLCBmKSkKCQkJCQljIGQgMTk0IDFjMjoKCQkJCQkJMWYuMWUoMWNjLjFiNC4xODEoMWNmLCBkKSkKCQkJCQkJCgkJCTM1OgoJCQkJMjMKCQkJCQoJCQkJIyA1MSAxYjQgMWIxIDEzYyBiOSAxYzYgMThkCgk0Mz0gMWNjLjFiNC4xODEoMWIuMWQxKCc2YzovLzJkLzFjMy8zNy40MC4xMmIvOTQnKSwgJycpCgkxY2EgMWNjLjFiNC4yNCg0Myk9PTNmOgkKCQljIDFjZiwgMWMyLCAxOGQgMTk0IDFjYy4zNCg0Myk6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CgkKCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJMWNhIDFiOS4yMigiMWM4IDEzYyBiOSAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgkJCQkKCQkJCQoJCQkJIyA1MSAxYjQgMWIxIDE5MiA4YiAxYzYgMThkCgkzYiA9IDFjYy4xYjQuMTgxKDFiLjFkMSgnNmM6Ly8yZC8xYzMvMTRkLjE0ZS4xMzQuODknKSwgJycpCgkxY2EgMWNjLjFiNC4yNCgzYik9PTNmOgkKCQljIDFjZiwgMWMyLCAxOGQgMTk0IDFjYy4zNCgzYik6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CgkKCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJMWNhIDFiOS4yMigiMWM4IDE5MiA4YiAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgkJCQkKCQkJCSMgNTEgMWI0IDFiMSAxNDEgMWM2IDE4ZAoJMWM0ID0gMWNjLjFiNC4xODEoMWIuMWQxKCc2YzovLzJkLzFjMy8zNy40MC4xYWQvMTQ5JyksICcnKQoJMWNhIDFjYy4xYjQuMjQoMWM0KT09M2Y6CQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDFjNCk6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CgkKCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJMWNhIDFiOS4yMigiMWM4IDE0MSAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgoJCQkJIyA1MSAxYjQgMWIxIDk4IDFjNiAxOGQKCTZkID0gMWNjLjFiNC4xODEoMWIuMWQxKCc2YzovLzJkLzFjMy8zNy40MC45OC8xYzYnKSwgJycpCgkxY2EgMWNjLjFiNC4yNCgxYzQpPT0zZjoJCgkJYyAxY2YsIDFjMiwgMThkIDE5NCAxY2MuMzQoNmQpOgoJCQk1ZSA9IDAKCQkJNWUgKz0gNDUoMThkKQoJCQoJCSMgMzMgMThkIDRlIDNlIDI4IDFiMSA3ZgoJCQkxY2EgNWUgPiAwOgoJCgkJCQkxYjkgPSAxMzEuMWNkKCkKCQkJCTFjYSAxYjkuMjIoIjFjOCBlYSAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgoJCQkJCSMgNTEgMWI0IDFiMSAxMTUgMWM2IDE4ZAoJNjMgPSAxY2MuMWI0LjE4MSgxYi4xZDEoJzZjOi8vMmQvMWMzLzM3LjQwLmU5LzI3JyksICcnKQoJMWNhIDFjYy4xYjQuMjQoMWM0KT09M2Y6CQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDYzKToKCQkJNWUgPSAwCgkJCTVlICs9IDQ1KDE4ZCkKCQkKCQkjIDMzIDE4ZCA0ZSAzZSAyOCAxYjEgN2YKCQkJMWNhIDVlID4gMDoKCQoJCQkJMWI5ID0gMTMxLjFjZCgpCgkJCQkxY2EgMWI5LjIyKCIxYzggMTI3IDI3IDI2IiwgMzkoNWUpICsgIiAxOGQgMmEiLCAiNjcgM2QgMzIgMWIxIDdmIDNhPyIpOgoJCQkJCgkJCQkJYyBmIDE5NCAxOGQ6CgkJCQkJCTFjYy4xYzUoMWNjLjFiNC4xODEoMWNmLCBmKSkKCQkJCQljIGQgMTk0IDFjMjoKCQkJCQkJMWYuMWUoMWNjLjFiNC4xODEoMWNmLCBkKSkKCQkJCQkJCgkJCTM1OgoJCQkJMjMKCgkJCQkJIyA1MSAxYjQgMWIxIDgwIDE2MiAxYzYgMThkCgk2MiA9IDFjYy4xYjQuMTgxKDFiLjFkMSgnNmM6Ly8yZC8xYzMvMzcuNDAuZjEvMWM2JyksICcnKQoJMWNhIDFjYy4xYjQuMjQoMWM0KT09M2Y6CQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDYyKToKCQkJNWUgPSAwCgkJCTVlICs9IDQ1KDE4ZCkKCQkKCQkjIDMzIDE4ZCA0ZSAzZSAyOCAxYjEgN2YKCQkJMWNhIDVlID4gMDoKCQoJCQkJMWI5ID0gMTMxLjFjZCgpCgkJCQkxY2EgMWI5LjIyKCIxYzggYjIgMTcwIDI3IDI2IiwgMzkoNWUpICsgIiAxOGQgMmEiLCAiNjcgM2QgMzIgMWIxIDdmIDNhPyIpOgoJCQkJCgkJCQkJYyBmIDE5NCAxOGQ6CgkJCQkJCTFjYy4xYzUoMWNjLjFiNC4xODEoMWNmLCBmKSkKCQkJCQljIGQgMTk0IDFjMjoKCQkJCQkJMWYuMWUoMWNjLjFiNC4xODEoMWNmLCBkKSkKCQkJCQkJCgkJCTM1OgoJCQkJMjMKCgkJCQkJIyA1MSAxYjQgMWIxIDc2IDFjNiAxOGQKCTRhID0gMWNjLjFiNC4xODEoMWIuMWQxKCc2YzovLzJkLzFjMy8zNy40MC43Ni8xYzYnKSwgJycpCgkxY2EgMWNjLjFiNC4yNCgxYzQpPT0zZjoJCgkJYyAxY2YsIDFjMiwgMThkIDE5NCAxY2MuMzQoNGEpOgoJCQk1ZSA9IDAKCQkJNWUgKz0gNDUoMThkKQoJCQoJCSMgMzMgMThkIDRlIDNlIDI4IDFiMSA3ZgoJCQkxY2EgNWUgPiAwOgoJCgkJCQkxYjkgPSAxMzEuMWNkKCkKCQkJCTFjYSAxYjkuMjIoIjFjOCBiYyAyNyAyNiIsIDM5KDVlKSArICIgMThkIDJhIiwgIjY3IDNkIDMyIDFiMSA3ZiAzYT8iKToKCQkJCQoJCQkJCWMgZiAxOTQgMThkOgoJCQkJCQkxY2MuMWM1KDFjYy4xYjQuMTgxKDFjZiwgZikpCgkJCQkJYyBkIDE5NCAxYzI6CgkJCQkJCTFmLjFlKDFjYy4xYjQuMTgxKDFjZiwgZCkpCgkJCQkJCQoJCQkzNToKCQkJCTIzCgoJCQkJCSMgNTEgMWI0IDFiMSBhNS5jYyAxYzYgMThkCgk1ZCA9IDFjYy4xYjQuMTgxKDFiLjFkMSgnNmM6Ly8yZC8xYzMvMzcuNDAuYTUuY2MvMWM2JyksICcnKQoJMWNhIDFjYy4xYjQuMjQoMWM0KT09M2Y6CQoJCWMgMWNmLCAxYzIsIDE4ZCAxOTQgMWNjLjM0KDVkKToKCQkJNWUgPSAwCgkJCTVlICs9IDQ1KDE4ZCkKCQkKCQkjIDMzIDE4ZCA0ZSAzZSAyOCAxYjEgN2YKCQkJMWNhIDVlID4gMDoKCQoJCQkJMWI5ID0gMTMxLjFjZCgpCgkJCQkxY2EgMWI5LjIyKCIxYzggZmIgMjcgMjYiLCAzOSg1ZSkgKyAiIDE4ZCAyYSIsICI2NyAzZCAzMiAxYjEgN2YgM2E/Iik6CgkJCQkKCQkJCQljIGYgMTk0IDE4ZDoKCQkJCQkJMWNjLjFjNSgxY2MuMWI0LjE4MSgxY2YsIGYpKQoJCQkJCWMgZCAxOTQgMWMyOgoJCQkJCQkxZi4xZSgxY2MuMWI0LjE4MSgxY2YsIGQpKQoJCQkJCQkKCQkJMzU6CgkJCQkyMwoKCQkJCQkjIDUxIDFiNCAxYjEgODAgMWM2IDE4ZAoJNjEgPSAxY2MuMWI0LjE4MSgxYi4xZDEoJzZjOi8vMmQvMWMzLzM3LjQwLjgwLzEzNScpLCAnJykKCTFjYSAxY2MuMWI0LjI0KDFjNCk9PTNmOgkKCQljIDFjZiwgMWMyLCAxOGQgMTk0IDFjYy4zNCg2MSk6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CgkKCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJMWNhIDFiOS4yMigiMWM4IGIyIDI3IDI2IiwgMzkoNWUpICsgIiAxOGQgMmEiLCAiNjcgM2QgMzIgMWIxIDdmIDNhPyIpOgoJCQkJCgkJCQkJYyBmIDE5NCAxOGQ6CgkJCQkJCTFjYy4xYzUoMWNjLjFiNC4xODEoMWNmLCBmKSkKCQkJCQljIGQgMTk0IDFjMjoKCQkJCQkJMWYuMWUoMWNjLjFiNC4xODEoMWNmLCBkKSkKCQkJCQkJCgkJCTM1OgoJCQkJMjMKCgkJCSAgICMgNTEgMWI0IDFiMSAxMDAgMWM2IDE4ZAoJNGQgPSAxY2MuMWI0LjE4MSgxYi4xZDEoJzZjOi8vNTgvMTAwJyksICcnKQoJMWNhIDFjYy4xYjQuMjQoNGQpPT0zZjoJCgkJYyAxY2YsIDFjMiwgMThkIDE5NCAxY2MuMzQoNGQpOgoJCQk1ZSA9IDAKCQkJNWUgKz0gNDUoMThkKQoJICAgCgkJIyAzMyAxOGQgNGUgM2UgMjggMWIxIDdmCgkJCTFjYSA1ZSA+IDA6CiAgIAoJCQkJMWI5ID0gMTMxLjFjZCgpCgkJCQkxY2EgMWI5LjIyKCIxYzggMTdkIDI2IiwgMzkoNWUpICsgIiAxOGQgMmEiLCAiNjcgM2QgMzIgMWIxIDdmIDNhPyIpOgoJCQkgICAKCQkJCQljIGYgMTk0IDE4ZDoKCQkJCQkJMWNjLjFjNSgxY2MuMWI0LjE4MSgxY2YsIGYpKQoJCQkJCWMgZCAxOTQgMWMyOgoJCQkJCQkxZi4xZSgxY2MuMWI0LjE4MSgxY2YsIGQpKQoKCQkJCQkjIDUxIDFiNCAxYjEgYjAgMWM2IDE4ZAoJCgk1ZiA9IDFiLjFkMSgnNmM6Ly9iYi8xYzMvMzcuNDAuYjAnKQoJMWI5ID0gMTMxLjFjZCgpCgk1YToKCQkxY2EgMWI5LjIyKCIxYzggMTI5IDI3IDI2IiwgIjY3IDNkIDMyIDFiMSA3ZiAxYzYiKToKCQkJN2IgPSAxY2MuMWI0LjE4MSg1ZiwiMWM2LmRiIikKCQkJMWNjLjFjNSg3YikKCgkyYzoKCQkyMwoJCgkxYjkgPSAxMzEuMWNkKCkKCTFiOS42ZigiODcgMzgiLCAiCQkJCQlmYSA2OSA2NCBkMyAgIiwgIgkJCQkgICBbMmIgYzddODEgYjUgZDEgMTQwIDg3IDM4Wy8yYl0iKQoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKIyMjCSAxM2IgMzYgOGMJICMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKIyMjCSAzNiA2YgkgICMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoJCjQ0IGFjKDFkKToKCTI5ICcjIyMnKzE3NysnIC0gNDggNmIjIyMnCgk1YyA9IDFiLjFkMSgxY2MuMWI0LjE4MSgnNmM6Ly81OC85Ny9hMicsICcnKSkKCTVhOgkKCQljIDFjZiwgMWMyLCAxOGQgMTk0IDFjYy4zNCg1Yyk6CgkJCTVlID0gMAoJCQk1ZSArPSA0NSgxOGQpCgkJCQoJCSMgMzMgMThkIDRlIDNlIDI4IDFiMSA3ZgoJCQkxY2EgNWUgPiAwOgoJCgkJCQkxYjkgPSAxMzEuMWNkKCkKCQkJCTFjYSAxYjkuMjIoIjFjOCAxMTkgMjcgMjYiLCAzOSg1ZSkgKyAiIDE4ZCAyYSIsICI2NyAzZCAzMiAxYjEgN2YgM2E/Iik6CgkJCQkJCQkKCQkJCQljIGYgMTk0IDE4ZDoKCQkJCQkJMWNjLjFjNSgxY2MuMWI0LjE4MSgxY2YsIGYpKQoJCQkJCWMgZCAxOTQgMWMyOgoJCQkJCQkxZi4xZSgxY2MuMWI0LjE4MSgxY2YsIGQpKQoJCQkJCTFiOSA9IDEzMS4xY2QoKQoJCQkJCTFiOS42ZigxNzcsICIJICAgNjkgN2EgMTQ4IDE4NSIpCgkJCQkzNToKCQkJCQkJMjMKCQkJMzU6CgkJCQkxYjkgPSAxMzEuMWNkKCkKCQkJCTFiOS42ZigxNzcsICIJICAgMTU2IDdhIDFiMSAzNiIpCgkyYzogCgkJMWI5ID0gMTMxLjFjZCgpCgkJMWI5LjZmKDE3NywgImU3IDY5IDdhIDFiYyBkZCA3MCA0ZiAxOGYgYTYiKQoJNTMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiMjIwlmNCAzNiA2YiAgICMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKIyMjCSAgIDQ5IDJmCSAgICMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyAKCQo0NCAxOTEoMWQsMWEpOgoJMWI0ID0gMWIuMWQxKDFjYy4xYjQuMTgxKCc2YzovLzU4LzU3JywnJykpCgk2Nj0xY2MuMWI0LjE4MSgxYjQsICcyMS41YicpCgkxYjkgPSAxMzEuMWNkKCkKCWVkPTFjYy4xYjQuMTgxKDFiNCwgJzIxLjViLmVkJykKCTFjYSAxY2MuMWI0LjI0KGVkKT09MTVjOiAKCQkxY2EgMWI5LjIyKCIxOGMgMTdmIDllIiwgJzE4YSBkMSAxNDQgMTdmIDEwYSA5ZT8nLCcnLCAiW2JdWzJiIDFhMF0JIDFhZiAxNGYgMTMwIDFiMiAxNzQgISEhWy9iXVsvMmJdIik6CgkJCTI5ICcjIyMnKzE3NysnIC0gNTYgMmYjIyMnCgkJCTFiNCA9IDFiLjFkMSgxY2MuMWI0LjE4MSgnNmM6Ly81OC81NycsJycpKQoJCQk2Nj0xY2MuMWI0LjE4MSgxYjQsICcyMS41YicpCgkJCTVhOgoJCQkJMWNjLjZlKDY2KQoJCQkJMjkgJz09PSA4NyAzOCAtIDljCScrMzkoNjYpKycJPT09JwoJCQkyYzoKCQkJCTIzCgkJCTQ2PTEzZS5hMygxZCkuYWYKCQkJYSA9IGMxKDY2LCIxYjMiKSAKCQkJYS5lNCg0NikKCQkJYS5kZSgpCgkJCTI5ICc9PT0gODcgMzggLSBiNyAxNTIJJyszOSg2NikrJwk9PT0nCgkJCTFiOSA9IDEzMS4xY2QoKQoJCQkxYjkuNmYoMTc3LCAiCSAgIDEwMSBjNCAxM2YgNDkgMmYiKQoJMzU6IAoJCTI5ICcjIyMnKzE3NysnIC0gNTYgMmYjIyMnCgkJMWI0ID0gMWIuMWQxKDFjYy4xYjQuMTgxKCc2YzovLzU4LzU3JywnJykpCgkJNjY9MWNjLjFiNC4xODEoMWI0LCAnMjEuNWInKQoJCTVhOgoJCQkxY2MuNmUoNjYpCgkJCTI5ICc9PT0gODcgMzggLSA5YwknKzM5KDY2KSsnCT09PScKCQkyYzoKCQkJMjMKCQk0Nj0xM2UuYTMoMWQpLmFmCgkJYSA9IGMxKDY2LCIxYjMiKSAKCQlhLmU0KDQ2KQoJCWEuZGUoKQoJCTI5ICc9PT0gODcgMzggLSBiNyAxNTIJJyszOSg2NikrJwk9PT0nCgkJMWI5ID0gMTMxLjFjZCgpCgkJMWI5LjZmKDE3NywgIgkgICAxMDEgYzQgMTNmIDQ5IDJmIikJCgk1MwoKNDQgYTQoMWQsMWEpOgoJMjkgJyMjIycrMTc3KycgLSBhYiBiOCAyZiMjIycKCTFiNCA9IDFiLjFkMSgxY2MuMWI0LjE4MSgnNmM6Ly81OC81NycsJycpKQoJNjY9MWNjLjFiNC4xODEoMWI0LCAnMjEuNWInKQoJNWE6CgkJYT1jMSg2NikuMTc5KCkKCQkxY2EgJzE4ZScgMTk0IGE6CgkJCTFhPSdiZCcKCQk4NSAnMTZhJyAxOTQgYToKCQkJMWE9J2NiJwoJCTg1ICdjOScgMTk0IGE6CgkJCTFhPSdjOCcKCQk4NSAnMTBjJyAxOTQgYToKCQkJMWE9JzFhNCBkMCA1MCcKCQk4NSAnMTBiJyAxOTQgYToKCQkJMWE9JzFhYSBkMCA1MCcKCQk4NSAnZTYnIDE5NCBhOgoJCQkxYT0nOTMnCgkyYzoKCQkxYT0iMWNiIDU2IgoJMWI5ID0gMTMxLjFjZCgpCgkxYjkuNmYoMTc3LCJbMmIgOTFdMTRmIDE4M1svMmJdICIrIDFhKyJbMmIgOTFdIDJmIDc4IDE2ZFsvMmJdIikKCTUzCgo0NCA5YigxZCk6CgkyOSAnIyMjJysxNzcrJyAtIDQ4IGI4IDJmIyMjJwoJMWI0ID0gMWIuMWQxKDFjYy4xYjQuMTgxKCc2YzovLzU4LzU3JywnJykpCgk2Nj0xY2MuMWI0LjE4MSgxYjQsICcyMS41YicpCgk1YToKCQkxY2MuNmUoNjYpCgkJMWI5ID0gMTMxLjFjZCgpCgkJMjkgJz09PSA4NyAzOCAtIDQ4CScrMzkoNjYpKycJPT09JwoJCTFiOS42ZigxNzcsICIJICAgNzcgNDkgYTEgODgiKQoJMmM6CgkJMWI5ID0gMTMxLjFjZCgpCgkJMWI5LjZmKDE3NywgIgkgICAxNTYgNDkgYTEgYjUgNzciKQoJNTMKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiMjIwkgZjQgNDkgMmYJICMjIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwoxYmEgPSAnLmE5LjFiOCcKMWE5ID0gJy80MS4xOTgnCjFiZCA9IDE1ZC5kYSgnMThiJykKMWIwID0gJy8xMmEn")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|2|3|4|5|6|7|8|9|a|B|for|d|FANART|f|10|11|12|13|14|15|16|17|18|19|name|xbmc|description|url|rmtree|shutil|20|advancedsettings|yesno|pass|exists|MAINTENANCE|Files|Cache|option|print|found|COLOR|except|profile|ART|XML|png|addDir|want|Count|walk|else|DELETE|plugin|Wizard|str|them|downloader_cache_path|channel4_cache_path|you|give|True|video|wizard|iconimage|iplayer_cache_path|def|len|link|fanart|DELETING|Advanced|supercartoons_cache_path|SORT_METHOD_VIDEO_TITLE|xbmc_cache_path|temp_cache_path|and|mediaportal|RECOMMENDED|Set|setView|return|wtf_cache_path|match|ADVANCED|userdata|home|xbmcplugin|try|xml|packages_cache_path|tvonline_cache_path|file_count|genesis_cache_path|movies|youtube_cache_path|ytmusic_cache_path|phoenix_cache_path|Please|replace|advance|Do|addonfolder|Deleting|OPEN_URL|PACKAGES|special|m4me_cache_path|remove|ok|KODI|compile|LocalAndRental|executebuiltin|findall|addSortMethod|supercartoons|Remove|SETTINGS|bbc_link|Packages|genesiscache|atv2_cache_b|atv2_cache_a|PREMIUM|delete|youtube|Brought|gt|lt|sortMethod|elif|escription|MD|Sucessfull|downloader|Textures13|Downloader|CACHE|Thumbnails|ADDONS|_blank|thumbnail|yellow|customftv|MIKEY1234|iplayer_http_cache|RENEGADES|target|addons|movies4me|getCondVisibility|UpdateLocalAddons|DELETEADVANCEDXML|REMOVING|MAIN|Original|UpdateAddonRepos|href|Settings|packages|http_GET|CHECKADVANCEDXML|tvonline|facebook|REPOS|ftv|kodimediaportal|class|CHECK|DELETEPACKAGES|private|AppleTV|content|genesis|REFRESH|YouTube|Library|ANDROID|To|FIXREPOSADDONS|WRITING|ADVANCE|iPlayer|DialogProgress|masterprofile|SuperCartoons|0CACHE|Be|ATV2|handle|open|TNPATH|mobile|Adding|UPDATEREPO|DELETETHUMBS|gold|MUCKYS|muckys|text13|TUXENS|cc|Caches|lib|shared|P2P|You|THUMBS|Reboot|whatthefurk|DELETECACHE|ADVANCEDXML|Downloading|GUIDE|Other|getSetting|db|dp|visit|close|textures13|Video|SUCCESSFUL|Extracting|Disconnect|write|anart|mikey|Error|URL|phstreams|Movies4me|THUBMNAIL|Thumnails|bak|TEXTURE13|renegades|FIX|spotitube|CUSTOMFTV|FTV|End|REQUIRED|ONLY|Wait|Archives|re|Finished|TVonline|ADDONS16|Database|DATABASE|INFO|temp|Done|Addona16|ftvguide|icon|This|nono|settings|br|argv|Your|p2p2|p2p1|database|Take|addons16|platform|download|span|STANDARD|feature|phoenix|Restart|extract|ADDONS2|Package|library|INSTALL|Corrupt|rebuild|Deletes|restart|Windows|WARNING|Refresh|addons2|x10host|Android|proceed|Phoenix|deletes|Genesis|freefix|iplayer|FOLDER|system|CUSTOM|WIZARD|CANNOT|xbmcgui|SHARED|Undone|simple|kodion|int|The|sys|update|zip|END|BBC|create|net|new|By|ITV|RESORT|UPDATE|Backed|DBPATH|0cache|Folder|all|Images|BUILDS|URLFIX|folder|script|module|YOU|Affect|Effect|NEW|tuxens|4oD|var|No|index|DAILY|Repos|FIRST|Force|False|ADDON|Cydia|USERL|EMPTY|BUILD|music|Mucky|OTHER|Ducks|RESET|FORCE|topic|INDEX|tuxen|Power|FIXES|SETUP|sleep|board|Music|Works|white|your|BACK|rl|DB|AddonTitle|http|read|Only|mg|Furk|Temp|USER|Up|LAST|join|On|HAVE|What|done|Does|XML1|XML2|time|Have|User|Back|files|zero|on|sure|AXML|Simple|File|in|Zip|But|Are|txt|RUN|jpg|smf|ini|All|not|INI|red|WTF|php|com|1st|NOT|Can|Not|amp|T|2nd|AND|4od|itv|Fix|AS|F|to|GO|w|path|r|MY|do|ml|dialog|N|n|please|U|id|th|IP|It|dirs|addon_data|itv_cache_path|unlink|cache|addDir2|Delete|BASEURL|if|NO|os|Dialog|s|root|H|translatePath".split("|")))


################################
###        CHECK IP          ###
################################
#Thanks to metalkettle for his work on the original IP checker addon        

def IPCHECK(url='http://www.iplocation.net/',inc=1):
    match=re.compile("<td width='80'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?</td><td>(.+?)</td>").findall(net.http_GET(url).content)
    for ip, region, country, isp in match:
        if inc <2: dialog=xbmcgui.Dialog(); dialog.ok('Check My IP',"[B][COLOR gold]Your IP Address is: [/COLOR][/B] %s" % ip, '[B][COLOR gold]Your IP is based in: [/COLOR][/B] %s' % country, '[B][COLOR gold]Your Service Provider is:[/COLOR][/B] %s' % isp)
        inc=inc+1

#################################
###      END CHECK IP         ###
#################################

#################################
###       CUSTOM FTV          ###
#################################

def CUSTOMINI(url,name):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("MD Wizard", '                                    Install Latest .ini File'):
        print '###'+AddonTitle+' - CUSTOM FTV INI###'
        path = xbmc.translatePath(os.path.join('special://masterprofile/addon_data/script.ftvguide',''))
        advance=os.path.join(path, 'addons2.ini')
        link=net.http_GET(url).content
        a = open(advance,"w") 
        a.write(link)
        a.close()
        print '=== MD Wizard - WRITING NEW    '+str(advance)+'    ==='
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "                               Done Adding New .ini File")  
    return

def CUSTOMSET(url,name):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("MD Wizard", '                               Install Custom Settings'):
        print '###'+AddonTitle+' - CUSTOM FTV SETTINGS###'
        path = xbmc.translatePath(os.path.join('special://masterprofile/addon_data/script.ftvguide',''))
        advance=os.path.join(path, 'settings.xml')
        link=net.http_GET(url).content
        a = open(advance,"w") 
        a.write(link)
        a.close()
        print '=== MD Wizard - WRITING NEW    '+str(advance)+'    ==='
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "                               Done Adding New Settings")  
    return


def DELETEFTVDB():
    try:
        ftvpath = xbmc.translatePath(os.path.join('special://masterprofile/addon_data/script.ftvguide',''))
        if os.path.exists(ftvpath)==True:
            dialog = xbmcgui.Dialog()
            if dialog.yesno("MD WIzard", "                               Delete FTV Guide Database"):
                ftvsource = os.path.join(ftvpath,"source.db")               
                os.unlink(ftvsource)               
        dialog.ok("MD Wizard", "                                     FTV Database Reset")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "               Error Deleting Database No Database To Delete")
    return

#################################
###      END CUSTOM FTV       ###
#################################
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
          
        
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


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==5 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    #if addon.get_setting('auto-view') == 'true':

    #    print addon.get_setting(viewType)
    #    if addon.get_setting(viewType) == 'Info':
    #        VT = '515'
    #    elif addon.get_setting(viewType) == 'Wall':
    #        VT = '501'
    #    elif viewType == 'default-view':
    #        VT = addon.get_setting(viewType)

    #    print viewType
    #    print VT
        
    #    xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==1:
        PREMIUM()

elif mode==2:
        URLFIX()

elif mode==3:
        MAINTENANCE()

elif mode==4:
        ADVANCEDXML()

elif mode==5:
        WIZARD(name,url,description)

elif mode==6:
        DELETEPACKAGES(url)

elif mode==7:
        AXML(url,name)

elif mode==8:
        CHECKADVANCEDXML(url,name)

elif mode==9:
        FIXREPOSADDONS(url)

elif mode==10:
        UPDATEREPO()

elif mode==11:
        DELETEADVANCEDXML(url)

elif mode==12:
        IPCHECK()

elif mode==13:
        DELETETHUMBS()

elif mode==14:
        DELETECACHE(url)

elif mode==15:
        CUSTOMFTV()

elif mode==16:
        CUSTOMINI(url,name)

elif mode==17:
        CUSTOMSET(url,name)

elif mode==18:
        DELETEFTVDB()

elif mode==19:
        USER(url)

elif mode==20:
        USERL(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
