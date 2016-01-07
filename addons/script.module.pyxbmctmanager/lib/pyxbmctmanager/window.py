import sys
import xbmcgui, xbmcaddon
import pyxbmct.addonwindow as pyxbmct
ACTION_ENTER = 13 # What is this code?
ACTION_SELECT_ITEM = 7

class Window(pyxbmct.AddonDialogWindow):
	def __init__(self, title='', width=None, height=None, columns=None, rows=None):
		super(Window,self).__init__(title)
		self.__index = None
		self.__draw = False
		self.overide_strings = {}
		self.overide_actions = {}
		self._width = width
		self._height = height
		self._columns = columns
		self._rows = rows
		self.__objects = {}
		if None not in [width, height, rows, columns]:
			self.setGeometry(width, height, rows, columns)

	def setAnimation(self, control): control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),('WindowClose', 'effect=fade start=100 end=0 time=250',)])
	
	def get_index(self): return self.__index

	def set_index(self, index): self.__index=index

	def draw(self):
		''' Function draw
			initialize built-in functions
			this automatically called.
		'''
		self.set_info_controls()
		self.set_active_controls()
		self.set_navigation()
		self.connect(pyxbmct.ACTION_NAV_BACK, self._cancel)
		self.__draw=True		
	
	def show(self):
		if self.__draw is False:
			self.draw()
		self.doModal()
	
	def hide(self): self.close()
		
	def set_info_controls(self):
		''' Function set_info_controls
			used to define static window controls
			this should be overwritten or the window will be blank.
		'''
		pass	

	def set_active_controls(self):
		''' Function set_active_controls
			used to define dynamic window controls
			this will be executed after set_info_controls
			this should be overwritten or the window will be blank.
		'''
		pass
	
	def set_navigation(self):
		''' Function set_navigation
			used to define navigation events
			this will be executed after set_info_controls
			this should be overwritten or there will be no navigation events
		'''
		pass
	
	def _cancel(self):
		dialog = xbmcgui.Dialog()
		if dialog.yesno("Exit Setup", "Are you sure?", "") : self.close()	
	
	def set_focus(self, target):
		''' Function set_focus
			used to set the inital focus on a specific object by target name
			
			Example:
				self.set_focus('button_name')
		'''
		self.setFocus(self.__get_object(target))
		
	def set_object_event(self, event, obj, target=None):
		if event == 'focus':
			self.set_focus(obj)
		elif event == 'left':
			self.__get_object(obj).controlLeft(self.__get_object(target))
		elif event == 'right':
			self.__get_object(obj).controlRight(self.__get_object(target))
		elif event == 'down':
			self.__get_object(obj).controlDown(self.__get_object(target))
		elif event == 'up':
			self.__get_object(obj).controlUp(self.__get_object(target))
		elif event == 'action':
			self.connect(self.__get_object(obj), target)

	def __put_object(self, name, obj):
		self.__objects[name] = obj
	
	def __get_object(self, key):
		return self.__objects[key]
	
	def put_object(self, name, obj):
		self.__objects[name] = obj
	
	def get_object(self, key):
		return self.__objects[key]
	
	def create_label(self, text, **kwargs):
		''' Function create_label
			used to create a text label
			the label needs to be added to the window via self.add_label
			
			Parameters:
		    text: string or unicode - text string.
		    font: string - font used for label text. (e.g. 'font13')
		    textColor: hexstring - color of enabled label's label. (e.g. '0xFFFFFFFF')
		    disabledColor: hexstring - color of disabled label's label. (e.g. '0xFFFF3300')
		    alignment: integer - alignment of label - *Note, see xbfont.h
		    hasPath: bool - True=stores a path / False=no path.
		    angle: integer - angle of control. (+ rotates CCW, - rotates CW)
			
			Example:
				label = self.create_label('The text is blah blah blah', font='font14')
		'''
		return pyxbmct.Label(text, **kwargs)
		
	def add_label(self, label, row, column, **kwargs):
		''' Function add_label
			Place a label within the window grid layout.
			
			Paramaters:
			label: label object created with self.create_label
			row: x coordinate
			column: y coordinate
	        rowspan: expand by n rows
	        columnspan: expand by n columns
	        pad_x: horizontal padding
	        pad_y: vertical padding
	        size and aspect adjustments. Negative values can be used
	        to make a control overlap with grid cells next to it, if necessary.
	        Raises AddonWindowError if a grid has not yet been set.
			Example:
				self.add_label(label_object, 1,1, rowspan=2)
		'''
		self.placeControl(label, row, column, **kwargs)
	
	def create_textbox(self, name, **kwargs):
		self.__put_object(name, pyxbmct.TextBox(**kwargs))
		self.__get_object(name)._type = 'textbox'
	
	def create_input(self, name, **kwargs):
		self.__put_object(name, pyxbmct.Edit('', **kwargs))
		self.__get_object(name)._type = 'input'

	def create_button(self, name, text, **kwargs):
		self.__put_object(name, pyxbmct.Button(text, **kwargs))
		self.__get_object(name)._type = 'button'
	
	def create_checkbox(self, name, text, **kwargs):
		self.__put_object(name, pyxbmct.RadioButton(text, **kwargs))
		self.__get_object(name)._type = 'checkbox'
	
	def create_image(self, name, path, **kwargs):
		self.__put_object(name, pyxbmct.Image(path, **kwargs))
		self.__get_object(name)._type = 'image'
		
	def create_list(self, name, **kwargs):
		self.__put_object(name, pyxbmct.List())
		self.__get_object(name)._type = 'list'
	
	def add_list_items(self, name, items, default=None):
		self.__get_object(name).addItems(items)
		if default is not None:
			self.set_selected(name, default)
		self.connectEventList(
            [pyxbmct.ACTION_MOUSE_LEFT_CLICK, ACTION_ENTER, ACTION_SELECT_ITEM],
            self.__list_update)
				
		
	def __list_update(self):
		try:
			obj = self.getFocus()
			for index in range(0,obj.size()):
				text = obj.getListItem(index).getProperty('original_label')
				if text:
					obj.getListItem(index).setLabel(text)
					obj.getListItem(index).setProperty('original_label', '')
				
			text = obj.getListItem(obj.getSelectedPosition()).getLabel()
			obj.getListItem(obj.getSelectedPosition()).setLabel('[B][COLOR yellow]%s[/COLOR][/B]' % text)
			obj.getListItem(obj.getSelectedPosition()).setProperty('original_label', text)
		except: pass
	
	
	def add_object(self, name, row, column, height=None, width=None, **kwargs):
		if None in [height, width]:
			self.placeControl(self.__get_object(name), row, column, **kwargs)
		else:
			self.placeControl(self.__get_object(name), row, column, height, width, **kwargs)
			
	def get_values(self):
		values = {}
		for key in self.__objects.keys():
			values[key] = self.get_value(key)
		return values
	
	def get_value(self, key):
		if self.__get_object(key)._type in ['input', 'textbox']:
			return self.__get_object(key).getText()
		elif self.__get_object(key)._type == 'checkbox':
			return self.__get_object(key).isSelected()==1
		elif self.__get_object(key)._type == 'list':
			return self.__get_object(key).getListItem(self.__get_object(key).getSelectedPosition()).getProperty('original_label')
	
	def set_value(self, key, value):
		if self.__get_object(key)._type in ['input', 'textbox']:
			self.__get_object(key).setText(value)
		elif self.__get_object(key)._type == 'checkbox':
			self.__get_object(key).setSelected(value)
		elif self.__get_object(key)._type == 'list':
			pass
		
	def set_selected(self, key, index):
		if self.__get_object(key)._type == 'list':
			self.__get_object(key).getListItem(index).select(True)
			text = self.__get_object(key).getListItem(index).getLabel()
			self.__get_object(key).getListItem(index).setLabel('[B][COLOR yellow]%s[/COLOR][/B]' % text)
			self.__get_object(key).getListItem(index).setProperty('original_label', text)
		else:
			pass
			