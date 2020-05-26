from BugEventManager import g_eventManager as events
import inspect


def handler(event):
	def handler_decorator(func):
		arg_names = inspect.getargspec(func)[0]
		
		def handler_func(args):
			return func(*args[:len(arg_names)])
			
		handler_func.__name__ = func.__name__
		handler_func.__module__ = func.__module__
		handler_func.func_name = func.func_name
				
		events.addEventHandler(event, handler_func)
		return handler_func
		
	return handler_decorator