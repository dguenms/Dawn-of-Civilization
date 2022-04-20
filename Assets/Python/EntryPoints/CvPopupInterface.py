index = 0

def register(name, func):
	global index
	index += 1
	
	func_name = name + str(index)
	globals()[func_name] = func
	
	return func_name