
import subprocess

class Process():
	"""Methodes for Process managment"""

	@staticmethod
	def execShell( command=None ):
		"""Return the python interpreter."""
		'@parameter string command Command shell.'

		subprocess.call( command )

	@staticmethod
	def launchSoftware( softwarePath, arg=None ):
		if arg:
			if not isinstance( arg, list):
				arg = [arg]
			subprocess.Popen( [softwarePath] + arg, creationflags=subprocess.CREATE_NEW_CONSOLE )

		else:
			subprocess.Popen( softwarePath, creationflags=subprocess.CREATE_NEW_CONSOLE )

	@staticmethod
	def partial( func, *args, **keywords ):
		import functools
		return functools.partial( func, *args, **keywords )

	def launchMayaPython( self, cmd, arg='' ):

		actions = '%s(%s)' %( cmd, arg ) 
		cmdExec = 'exec(\'import sys\\\\nsys.path.append(\\\\\'F:/software/Forge_0.0.0.1dev/\\\\\')\\\\nsys.path.append(\\\\\'F:/software/Anvil_0.0.0.1dev/\\\\\')\\\\nsys.path.append(\\\\\'F:/software/hammer_0.0.0.1dev/\\\\\')\\\\nimport Hammer\\\\n' + actions + '\')'

		self.launchSoftware( 'c:/Program Files/Autodesk/Maya2015/bin/maya.exe', arg=['-command', "python \"%s\";" %( cmdExec )] )

	def launchNukePython( self, cmd, arg='' ):
		path = 'f:/tmp/nukeStartupTmp.py'

		actions = '%s(%s)' %( cmd, arg ) 
		cmdExec = 'exec(\'import sys\\nsys.path.append(\\\'F:/software/Forge_0.0.0.1dev/\\\')\\nsys.path.append(\\\'F:/software/Anvil_0.0.0.1dev/\\\')\\nsys.path.append(\\\'F:/software/hammer_0.0.0.1dev/\\\')\\nimport Hammer\\n%s\\nimport Forge.core.System\\nForge.core.System.removeFile(\\\'%s\\\')\')' %( actions, path )

		import Forge.core.System
		Forge.core.System.setFile( path=path, content=cmdExec )

		self.launchSoftware( 'c:/Program Files/Nuke8.0v3/Nuke8.0.exe', arg=path )
