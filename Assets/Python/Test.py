def function():
	print "you have called the function"

name = 'name'
othername = 'othername'

globals()[name] = function
globals()[othername] = function