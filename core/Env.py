
class Env():
	"""Methodes for Env managment"""

	def __init__( self ):

		self.root = 'f:/'

		# temp
		self.tmp = '%stmp/' %( self.root )

		# data
		self.data = '%sdata/' %( self.root )

		# commercial software
		self.maya = 'c:/Program Files/Autodesk/Maya2015/bin/maya.exe'
		self.nuke = 'c:/Program Files/Nuke8.0v3/Nuke8.0.exe'
		self.renderdl = 'C:/Program Files/3Delight/bin/renderdl.exe'
		self.localqueue = 'c:/Program Files/Pixar/RenderManStudio-20.0-maya2015/bin/LocalQueue.exe'
		self.python = 'c:/Python27/python.exe'


		# global software
		self.software = '%ssoftware/' %( self.root )

		# library
		self.forgeLib = '%sForge_0.0.0.1dev/' %( self.software )
		self.anvilLib = '%sAnvil_0.0.0.1dev/' %( self.software )
		self.hammerLib = '%sHammer_0.0.0.1dev/' %( self.software )
		self.coalLib = '%scoal_0.0.0.1dev/' %( self.software )
		self.bcconverterLib = '%sBCconverter_0.0.0.1dev/' %( self.software )

		# apps
		self.coal = '%s/Coal/bin/launchCoal.py' %( self.coalLib )
		self.bcconverter = '%s/BCconverter/bin/launchBCconverter.py' %( self.bcconverterLib )
