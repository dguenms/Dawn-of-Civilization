from CvPythonExtensions import *
from Core import *

from CvPopupInterface import register

import inspect


class PopupLauncherBuilderFactory(object):

	def text(self, text):
		return PopupLauncherBuilderBuilder(text=text)
	
	def option(self, func, label='', button=event_bullet):
		return PopupLauncherBuilderBuilder(options={func.__name__: (func, label, button)})
	
	def selection(self, func, label='', button=event_bullet):
		return PopupLauncherBuilderBuilder(selections={func.__name__: (func, label, button)})
		
	def cancel(self, label='', button=event_cancel):
		return PopupLauncherBuilderBuilder(cancel=(label, button))


class PopupLauncherBuilderBuilder(object):

	def __init__(self, text='', options={}, selections={}, cancel=None):
		self._text = text
		self._option_types = options
		self._selection_types = selections
		self._cancel_type = cancel
		
	def text(self, text):
		return PopupLauncherBuilderBuilder(text, self._option_types, self._selection_types, self._cancel_type)	
		
	def option(self, func, label='', button=event_bullet):
		option_types = self._option_types.copy()
		option_types[func.__name__] = (func, label, button)
		return PopupLauncherBuilderBuilder(self._text, option_types, self._selection_types, self._cancel_type)
		
	def selection(self, func, label='', button=event_bullet):
		selection_types = self._selection_types.copy()
		selection_types[func.__name__] = (func, label, button)
		return PopupLauncherBuilderBuilder(self._text, self._option_types, selection_types, self._cancel_type)
		
	def cancel(self, label='', button=event_cancel):
		return PopupLauncherBuilderBuilder(self._text, self._option_types, self._selection_types, (label, button))
	
	def build(self):
		return PopupLauncherBuilder(self._text, self._option_types, self._selection_types, self._cancel_type)


class PopupLauncherBuilder(object):

	def __init__(self, text='', option_types={}, selection_types={}, cancel=None):
		self._text = text
		self._option_types = {}
		self._selection_types = {}
		self._cancel = cancel
		
		for func, label, button in option_types.values():
			self.option_type(func, label, button)
			
		for func, label, button in selection_types.values():
			self.selection_type(func, label, button)
	
	def option_type(self, func, label='', button=event_bullet):
		func_name = func.__name__
		
		self._option_types[func_name] = (func, label, button)
		self.register_option_func(func_name)
		
	def register_option_func(self, func_name):
		def func_option(*format):
			return self.option(func_name, *format)
		
		self.__dict__[func_name] = func_option
		
	def selection_type(self, func, label='', button=event_bullet):
		func_name = func.__name__
		
		self._selection_types[func_name] = (func, label, button)
		self.register_selection_func(func_name)
	
	def register_selection_func(self, func_name):
		def func_selection(*format):
			return self.selection(func_name, *format)
		
		self.__dict__[func_name] = func_selection

	def launcher(self):
		return PopupLauncher(self._text, self._option_types, self._selection_types, self._cancel)
	
	def text(self, *format):
		return self.launcher().text(*format)
	
	def option(self, func_name, *format, **optional):
		return self.launcher().option(func_name, *format, **optional)
	
	def selection(self, func_name, *format, **optional):
		return self.launcher().selection(func_name, *format, **optional)
		
	def cancel(self, *format, **optional):
		return self.launcher().cancel(*format, **optional)


class PopupLauncher(object):

	def __init__(self, input_text, option_types, selection_types, cancel_type):
		self._text = text(input_text)
		self._option_types = option_types
		self._selection_types = selection_types
		self._cancel_type = cancel_type
		
		self._choices = []
		
		for func_name in self._option_types:
			self.register_option(func_name)
		
		for func_name in self._selection_types:
			self.register_selection(func_name)
			
	def parse_button(self, button):
		try:
			return infos.art(button)
		except:
			return button
		
	def format_label(self, label, *format):
		if label:
			return text(label, *format)
		else:
			return ', '.join(format)
		
	def register_option(self, func_name):
		def func(*format, **optional):
			return self.option(func_name, *format, **optional)
			
		self.__dict__[func_name] = func
		
	def register_selection(self, func_name):
		def func(*format, **optional):
			return self.selection(func_name, *format, **optional)
		
		self.__dict__[func_name] = func
	
	def text(self, *format):
		if self._text:
			self._text = text(self._text, *format)
		elif format:
			self._text = text(*format)
		return self
		
	def option(self, func_name, *format, **optional):
		handle, label, button = self._option_types[func_name]
		label = optional.get('label', label)
		button = optional.get('button', button)
		self._choices.append(('option', handle, self.format_label(label, *format), button))
		return self
	
	def selection(self, func_name, *format, **optional):
		handle, label, button = self._selection_types[func_name]
		label = optional.get('label', label)
		button = optional.get('button', button)
		self._choices.append(('selection', handle, self.format_label(label, *format), button))
		return self
		
	def no_handle(self):
		return
	
	def cancel(self, *format, **optional):
		label, button = self._cancel_type
		label = optional.get('label', label)
		button = optional.get('button', button)
		self._choices.append(('option', self.no_handle, self.format_label(label, *format), button))
		return self
	
	def handle_choice(self, args):
		iChoice = args[0]
		data = args[1:5]
		text = args[5]
		options = args[6:8]
		
		type, handle, _, _ = self._choices[iChoice]
		arg_names = [arg_name for arg_name in inspect.getargspec(handle)[0] if arg_name != 'self']
		
		if not handle:
			return
		
		if type == 'selection':
			handle(iChoice, *data[:len(arg_names)-1])
		else:
			handle(*data[:len(arg_names)])
	
	def launch(self, *args):
		# create popup
		popup = CyPopupInfo()
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		
		# dynamically register handler func
		func_name = register(self.__class__.__name__, self.handle_choice)
		
		popup.setPythonModule("CvPopupInterface")
		popup.setOnClickedPythonCallback(func_name)
		
		# pass arguments
		setters = (popup.setData1, popup.setData2, popup.setData3)
		for setter, arg in zip(setters[:len(args)], args):
			setter(arg)
		
		# set up popup body and buttons
		popup.setText(self._text)
		
		for type, handle, label, button in self._choices:
			popup.addPythonButton(label, self.parse_button(button))
		
		# launch
		popup.addPopup(active())


popup = PopupLauncherBuilderFactory()