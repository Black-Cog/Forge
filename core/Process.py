
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
		import Forge.core

		env = Forge.core.Env()

		actions = '%s(%s)' %( cmd, arg ) 
		cmdExec = 'exec(\'import sys\\\\nsys.path.append(\\\\\'%s\\\\\')\\\\nsys.path.append(\\\\\'%s\\\\\')\\\\nsys.path.append(\\\\\'%s\\\\\')\\\\nimport Hammer\\\\n%s\')' %( env.forgeLib, env.anvilLib, env.hammerLib, actions )

		self.launchSoftware( env.maya, arg=['-command', "python \"%s\";" %( cmdExec )] )

	def launchNukePython( self, cmd, arg='' ):
		import Forge.core

		env = Forge.core.Env()
		path = '%snukeStartupTmp.py' %( env.tmp )

		actions = '%s(%s)' %( cmd, arg ) 
		cmdExec = 'exec(\'import sys\\nsys.path.append(\\\'%s\\\')\\nsys.path.append(\\\'%s\\\')\\nsys.path.append(\\\'%s\\\')\\nimport Hammer\\n%s\\nimport Forge.core.System\\nForge.core.System.removeFile(\\\'%s\\\')\')' %(  env.forgeLib, env.anvilLib, env.hammerLib, actions, path )

		Forge.core.System.setFile( path=path, content=cmdExec )

		self.launchSoftware( env.nuke, arg=path )
