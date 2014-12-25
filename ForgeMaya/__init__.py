
from RibMaya import RibMaya

def help():
	"""Return string the help of the module ForgeMaya"""
	helpString  = '\n ######## module ForgeMaya ########'
	helpString += '\n - RibMaya() : Methodes for Rib managment in Maya.'

	return helpString


foo = RibMaya()
foo.verbose()