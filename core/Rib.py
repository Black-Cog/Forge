import os

class Rib(object):
	"""Methodes for Rib managment"""
	def __init__( self ):
		self.output = 'E:/141031_defaultProject/maya/3delight/rib_scene_001/rib/rib_python.rib'
		self.light = 'E:/141031_defaultProject/maya/3delight/rib_scene_001/shaders/OBJ/light.sdl'
		self.name = 'light_fill'
		# self.mesh = 'obj/boudha.rib'
		self.mesh = 'obj/test_python.rib'
		self.shader = 'BCmonolithic1'
		self.shaderP = 'E:/140817_tools/_framework/BCshading/sdl/BCmonolithic'
		# self.list = { 'type':['light, mesh'], 'path':['1', '2'], 'name':['light_fill', 'BCmonolithic1'] }
		self.list = { 'type':'', 'path':'', 'name':'' }
	
	def verbose( self ):

		# print self.ribObject( name='obj1', face='1 1', vtxPerFace='4 4', vtxIndex='0 1 2 3', vtxP='0 0 0 0', n='0 0 0 0', stP='0 0 0 0' )
		# print self.ribObjectSubdiv( name='obj1', vtxPerFace='4 4', vtxIndex='0 1 2 3', vtxP='0 0 0 0', stP='0 0 0 0' )
		# print self.list['name']
		# return
		test =   ''
		test +=  self.ribAttribute( attrType='light', name=self.name, path=self.light )
		test +=  self.ribArchive( name=self.shader, path=self.shaderP )
		test +=  self.ribAttribute( attrType='object', name=self.shader, path=self.mesh )
		test = self.ribWorld( test )
		test =  self.ribGlobal() + test
		self.ribWrite( ribPath=self.output, content=test, force=True )
		return
		print self.help()

	@staticmethod
	def ribObject( name, face, vtxPerFace, vtxIndex, vtxP, n, stP ):
		"""Return string Object"""

		objectString  =  '\nObjectBegin "%s"' % ( name )
		objectString  += '\n    PointsGeneralPolygons'
		objectString  += '\n        [%s]' % ( face )
		objectString  += '\n        [%s]' % ( vtxPerFace )
		objectString  += '\n        [%s]' % ( vtxIndex )
		objectString  += '\n        "vertex point P" [%s]' % ( vtxP )
		objectString  += '\n        "facevarying normal N" [%s]' % ( n )
		objectString  += '\n        "facevarying float[2] st" [%s]' % ( stP )
		objectString  += '\nObjectEnd\n'
		objectString  += '\nAttributeBegin'
		objectString  += '\n    ObjectInstance "%s"' % ( name )
		objectString  += '\nAttributeEnd'
		objectString  += '\n'
		return objectString

	@staticmethod
	def ribObjectSubdiv( name, vtxPerFace, vtxIndex, vtxP, stP ):
		"""Return string Object subdivide"""

		objectSubdivString  =  '\nObjectBegin "%s"' % ( name )
		objectSubdivString  += '\n    SubdivisionMesh "catmull-clark" [%s]' % ( vtxPerFace )
		objectSubdivString  += '\n    [%s]' % ( vtxIndex )
		objectSubdivString  += '\n        [ "interpolateboundary" "facevaryinginterpolateboundary" ] [ 1 0 1 0 ] [ 2 1 ] [ ]'
		objectSubdivString  += '\n        "vertex point P" [%s]' % ( vtxP )
		objectSubdivString  += '\n        "facevarying float[2] st" [%s]' % ( stP )
		objectSubdivString  += '\nObjectEnd\n'
		objectSubdivString  += '\nAttributeBegin'
		objectSubdivString  += '\n    ObjectInstance "%s"' % ( name )
		objectSubdivString  += '\nAttributeEnd'
		objectSubdivString  += '\n'
		return objectSubdivString

	@staticmethod
	def ribGlobal():
		"""Return string global"""

		globalString  =  '\n#Black Cog Rib\n\n'
		globalString  += '\nFormat 960 540 1'
		globalString  += '\nPixelSamples 6 6'

		globalString  += '\nProjection "perspective" "fov" [ 60 ]'
		globalString  += '\nScale 1 1 -1'
		globalString  += '\nTranslate 0 0 -10'
		globalString  += '\nRotate 0 0 1 0'

		globalString  += '\nHider "raytrace"'
		globalString  += '\nOrientation "rh"'
		globalString  += '\nOption "trace" "integer diffuseraycache" [ 1 ]'

		globalString  += '\nOption "limits" "integer[2] bucketsize" [ 16 16 ]'
		globalString  += '\nOption "limits" "integer texturememory" [ 1024000 ]'		
		globalString  += '\nOption "limits" "color othreshold" [ 0.996 0.996 0.996 ] "color zthreshold" [ 0.996 0.996 0.996 ]'

		globalString  += '\nDisplay "+E:/141031_defaultProject/maya/3delight/rib_scene_001/image/rib_scene_001_renderPass_rgba_0001.exr" "exr" "rgba"'
		globalString  += '\n    "float[4] quantize" [ 0 0 0 0 ]'
		globalString  += '\n    "string filter" [ "mitchell" ]'
		globalString  += '\n    "float[2] filterwidth" [ 4 4 ]'
		globalString  += '\n    "string exrpixeltype" [ "float" ]'
		globalString  += '\nOption "statistics" "integer endofframe" [ 3 ] "string filename" [ "E:/141031_defaultProject/maya/3delight/rib_scene_001/renderPass_0001.txt" ]'

		globalString  += '\n'
		return globalString


	@staticmethod
	def ribWorld( content ):
		"""Return string world"""
		'@parameter string content All of the element in the rib.'

		worldString  =  '\nFrameBegin 1'
		worldString  += '\n    WorldBegin'
		worldString  += content
		worldString  += '\n    WorldEnd'
		worldString  += '\nFrameEnd'
		worldString  += '\n'
		return worldString

	@staticmethod
	def ribArchive( name, path ):
		"""Return string archive"""
		'@parameter string name Name of the shader.'
		'@parameter string path Path of the shader.'

		archiveString  =  '\n        ArchiveBegin "%s surface"' % ( name )
		archiveString  += '\n            Surface "%s"' % ( path )
		archiveString  += '\n        ArchiveEnd'
		archiveString  += '\n'
		return archiveString

	@staticmethod
	def ribAttribute( attrType, name, path ):
		"""Return string attribut"""
		'@parameter string attrType "light" or "object" for choose with attribut'
		'@parameter string name Name of the light and Name of the shader (object case).'
		'@parameter string path Path of the rib object or le lightShader.'

		attrString  =  '\n        AttributeBegin'
		attrString  += '\n            Translate 0 0 0'
		attrString  += '\n            Rotate 0 0 1 0'
		attrString  += '\n            Scale 1 1 1'

		if attrType == 'light':
			attrString  += '\n            Translate 10 10 0'
			attrString  += '\n            LightSource "%s" "%s"' % ( path, name )

		if attrType == 'object':
			attrString  += '\n            Attribute "visibility" "integer transmission" [ 1 ] '
			attrString  += '\n            Attribute "shade" "string transmissionhitmode" [ "shader" ]'
			attrString  += '\n            Attribute "visibility" "integer specular" [ 1 ] '
			attrString  += '\n            Attribute "shade" "string specularhitmode" [ "shader" ]'
			attrString  += '\n            Sides 2'
			attrString  += '\n            ReadArchive "%s surface"' % ( name )
			attrString  += '\n            ReadArchive "%s"' % ( path )

		attrString  += '\n        AttributeEnd'

		if attrType == 'light' : attrString  += '\n            Illuminate "%s" 1' % ( name )
		attrString  += '\n'
		return attrString

	@staticmethod
	def ribWrite( ribPath, content, force=False ):
		"""Write the rib file"""
		'@parameter string ribPath Path of the rib file.'
		'@parameter string content Content of the rib file.'
		'@parameter bool force Force the write of the rib for override.'
		if os.path.exists( ribPath ) == False or force == True:
			rib = open( ribPath, 'w' )
			rib.write( content )
			rib.close()
			print 'Rib write.'
		else:
			print 'This rib file already exist'

	@staticmethod
	def help():
		"""Return string the help of the class Rib"""
		helpString  = '\n ######## class Rib ########'
		helpString += '\n - ribWrite() : Write the rib file.'
		helpString += '\n     - string ribPath Path of the rib file.'
		helpString += '\n     - string content Content of the rib file.'
		helpString += '\n     - bool force Force the write of the rib for override.'
		helpString += '\n - ribAttribute() : Return string attribut.'
		helpString += '\n     - string attrType "light" or "object" for choose with attribut'
		helpString += '\n     - string name Name of the light and Name of the shader (object case).'
		helpString += '\n     - string path Path of the rib object or le lightShader.'
		helpString += '\n - ribArchive() : Return string archive.'
		helpString += '\n     - string name Name of the shader.'
		helpString += '\n     - string path Path of the shader.'
		helpString += '\n - ribWorld() : Return string world.'
		helpString += '\n     - string content All of the element in the rib.'
		helpString += '\n - ribGlobal() : Return string global.'
		helpString += '\n - ribObject() : Return string Objects.'
		helpString += '\n - ribObjectSubdiv() : Return string Object subdivides.'

		return helpString
