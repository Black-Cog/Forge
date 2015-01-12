
import subprocess

class Process(object):
	"""Methodes for Process managment"""

	@staticmethod
	def launch( command=None ):
		"""Return the python interpreter."""
		'@parameter string command Command shell.'

		subprocess.call( command )
