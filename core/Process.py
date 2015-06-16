
import subprocess

class Process(object):
	"""Methodes for Process managment"""

	@staticmethod
	def execShell( command=None ):
		"""Return the python interpreter."""
		'@parameter string command Command shell.'

		subprocess.call( command )

	@staticmethod
	def launchSoftware( softwarePath, arg=None ):
		if arg:
			subprocess.Popen( [softwarePath, arg], creationflags=subprocess.CREATE_NEW_CONSOLE )
		else:
			subprocess.Popen( softwarePath, creationflags=subprocess.CREATE_NEW_CONSOLE )

	@staticmethod
	def partial( func, *args, **keywords ):
		import functools
		return functools.partial( func, *args, **keywords )
