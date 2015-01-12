import os
import sys

class Python(object):
	"""Methodes for Python managment"""

	@staticmethod
	def interpreter():
		"""Return the python interpreter."""
		executable = sys.argv[0].replace( '\\', '/' ).split( '/' )[-1]
		software   = executable.split( '.' )[0]

		return software

	@staticmethod
	def help():
		"""Return string the help of the class Python"""
		helpString  = '\n ######## class Python ########'
		helpString += '\n - interpreter() : Return the python interpreter.'

		return helpString
