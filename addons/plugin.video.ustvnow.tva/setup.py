import os
import sys
import xbmc
import xbmcaddon
import xbmcgui

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonid   = addon.getAddonInfo('id')
root = addon.getAddonInfo('path')

settings = os.path.join(xbmc.translatePath( root ), 'resources/settings.xml')
def Setup():
	sys.path.append(os.path.join(xbmc.translatePath( "special://home/addons/script.module.beautifulsoup/" ), 'lib'))
	sys.path.append(os.path.join(xbmc.translatePath( "special://home/addons/script.module.pyxbmct/" ), 'lib'))
	sys.path.append(os.path.join(xbmc.translatePath( "special://home/addons/script.module.pyxbmctmanager/" ), 'lib'))
	from resources.lib import ustvnow
	from pyxbmctmanager.window import Window
	from pyxbmctmanager.manager import Manager
	from BeautifulSoup import BeautifulSoup
	class FirstPage(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title)
		
		def set_info_controls(self):
			content = """Please visit the following link to Sign Up for a free account with USTVNOW:\n[COLOR blue]http://www.ustvnow.com/newuser_usa.php[/COLOR]\nYou'll need to Sign Up by email, not through Facebook. Make sure that you have \nconfirmed your email address before continuing."""
			self.add_label(self.create_label(content), 0, 0, columnspan=4, rowspan=5, pad_x=15, pad_y=10)

	class SecondPage(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title)
		def set_info_controls(self):
			def next_action():
				valid = ustvnow.Ustvnow(self.get_value('email'), self.get_value('password'))._login()
				if not valid:
					xbmcgui.Dialog().ok('Login Error', 'Incorrect login.', 'Please check your email and password.', 'Sign up at http://www.ustvnow.com/newuser_usa.php')
					return False
				WM.next_page()
			content = "Please input your USTVNOW login details below:"
			self.add_label(self.create_label(content), 0, 0, columnspan=4, pad_x=15, pad_y=10)
			
			self.add_label(self.create_label('Email:'), 2, 0, pad_x=15, pad_y=10)
			self.add_label(self.create_label('Password:'), 3, 0, pad_x=15, pad_y=10)

			
			self.create_input('email')
			self.add_object('email', 2, 1, columnspan=2)
			self.set_value('email', addon.getSetting('email'))
			
			self.create_input('password', isPassword=True)
			self.add_object('password', 3, 1, columnspan=2)
			self.set_value('password', addon.getSetting('password'))

			self.overide_actions = {"next_button": next_action}

	class ThirdPage(Window):
		def __init__(self, title):
			super(self.__class__,self).__init__(title)
		def set_info_controls(self):
			content = "Please select your account type:"
			self.add_label(self.create_label(content), 0, 0, columnspan=4, pad_x=15, pad_y=10)
			
			self.create_list('speed', selectedColor=1, columnspan=4)
			self.add_object('speed', 1, 0, 4, 3)
			items = ["Free - (Limited to 400 kbps)", "Paid (HD)"]
			self.add_list_items('speed', items, 0)
			self.create_button('finish', "Finish")
			self.add_object('finish', 5, 3)
	
	class ConfirmationPage(Window):	
		def set_info_controls(self):
			content = """Thank you for choosing USTVnow Live for Kodi.\n\nPlease feel free to visit\n[COLOR lightblue]http://forums.tvaddons.ag[/COLOR]\nshould you have any questions or comments, enjoy!"""
			self.add_label(self.create_label(content, alignment=2, font="font14"), 0, 0, columnspan=3, rowspan=5, pad_x=15, pad_y=15)

	TitleText = "USTVnow Live for Kodi"
	
	WM = Manager(width=800, height=320, columns=4, rows=6)
	WM.add_page(FirstPage(TitleText))
	WM.add_page(SecondPage(TitleText))
	WM.add_page(ThirdPage(TitleText))
	WM.add_confirmation(ConfirmationPage(TitleText))
	WM.build()
	WM.set_object_event(0, 'focus', 'next_button')
	WM.set_object_event(1, 'focus', 'email')
	WM.set_object_event(1, 'down', 'email', 'password')
	WM.set_object_event(1, 'down', 'password', 'next_button')
	WM.set_object_event(1, 'up', 'previous_button', 'password')
	WM.set_object_event(1, 'up', 'next_button', 'password')
	WM.set_object_event(1, 'up', 'password', 'email')
	WM.set_object_event(1, 'left', 'next_button', 'previous_button')
	WM.set_object_event(1, 'right', 'previous_button', 'next_button')
	WM.set_object_event(2, 'focus', 'finish')
	WM.set_object_event(2, 'left', 'finish', 'previous_button')
	WM.set_object_event(2, 'right', 'previous_button', 'finish')
	WM.set_object_event(2, 'down', 'speed', 'finish')
	WM.set_object_event(2, 'up', 'finish', 'speed')
	WM.set_object_event(2, 'up', 'previous_button', 'speed')
	def complete_setup():
		new = BeautifulSoup
		xml = BeautifulSoup(open(settings, "r").read())
		ent = xml.findAll('setting')
		for i in ent:
			try:
				id = i['id']
				try:
					default = id['default']
				except:
					default = ""
				addon.setSetting(id, str(default))	
			except: pass
		email = WM.get_value(1, "email")
		password = WM.get_value(1, "password")
		speed = WM.get_value(2, "speed")
		addon.setSetting('email', email)
		addon.setSetting('password', password)
		if speed == 'Paid (HD)':
			addon.setSetting('quality', "3")
		else:
			addon.setSetting('quality', "0")
		addon.setSetting('stream_type', "0")
		addon.setSetting('setup', "true")
		
		WM.show_confirmation()
		
	WM.set_object_event(2, "action", "finish", complete_setup)
	WM.show()


if __name__ == '__main__':
	Setup()
	win = xbmcgui.Window(10000)
	win.setProperty(addonname+'.setup', "false")
