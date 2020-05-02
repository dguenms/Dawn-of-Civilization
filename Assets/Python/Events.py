from BugEventManager import g_eventManager as events
import inspect


def handler(event):
	def handler_decorator(func):
		arg_names = inspect.getargspec(func)[0]
		
		def handler_func(args):
			print "%s -> %s" % (event, func)
			return func(*args[:len(arg_names)])
				
		events.addEventHandler(event, handler_func)
		return handler_func
		
	return handler_decorator