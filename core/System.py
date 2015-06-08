import os
import sys
import shutil

class System(object):
	"""Methodes for System managment"""

	@staticmethod
	def interpreter():
		"""Return the system interpreter."""
		executable = sys.executable.replace( '\\', '/' ).split( '/' )[-1]
		software   = executable.replace( '.exe', '' )

		return software

	@staticmethod
	def mkdir( path=None ):
		"""Create directory."""
		'@parameter string path Path of the new directory.'

		# converte to array
		folders = []
		if isinstance( path, list ):
			folders = path
		else:
			folders.append( path )

		# create folder
		for folder in folders:
			if not os.path.exists( folder ):
				os.makedirs( folder )

	@staticmethod
	def setFile( path=None, content=None, type='w' ):
		"""Create file."""
		'@parameter string path Path of the new file.'
		'@parameter string content Content of the new file.'
		'@parameter string type Type of the new file| w=override (default); a=append; r=read only.'

		file = open( path, type )
		file.write( content )
		file.close()

	@staticmethod
	def list( path=None, file=True, folder=True ):
		"""Create file."""
		'@parameter string path Path of the list.'
		'@parameter bool   file Bool for return file.'
		'@parameter bool   folder Bool for return folder.'

		fullList   = os.listdir( path )
		returnList =[]

		for i in fullList:
			if file and os.path.isfile( '%s/%s' %(path, i) ):
				returnList.append(i)
			if folder and not os.path.isfile( '%s/%s' %(path, i) ):
				returnList.append(i)

		return returnList

	@staticmethod
	def cleanFolder( path=None ):

		if os.path.exists( path ):
			for i in os.listdir( path ):

				tmpItem = '%s/%s' %( path, i )

				if os.path.isfile( tmpItem ) : os.remove( tmpItem )
				elif os.path.isdir( tmpItem ) : shutil.rmtree( tmpItem )

	@staticmethod
	def setEnv( path ):
		os.chdir( path )

	@staticmethod
	def getPath( file ):
		return os.path.dirname( os.path.realpath(file) )

	@staticmethod
	def exists( path ):
		return os.path.exists( path )

	@staticmethod
	def getExtension( path ):
		return path.split( '.' )[-1]

	@staticmethod
	def help():
		"""Return string the help of the class System"""
		helpString  = '\n ######## class System ########'
		helpString += '\n - interpreter() : Return the system interpreter.'
		helpString += '\n - mkdir()       : Create directory.'
		helpString += '\n     - string path Path of the new directory.'
		helpString += '\n - setFile()       : Create directory.'
		helpString += '\n     - path Path of the new file.'
		helpString += '\n     - content Content of the new file.'
		helpString += '\n     - type Type of the new file| w=override (default); a=append; r=read only.'

		return helpString
