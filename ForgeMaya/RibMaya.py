import maya.cmds

class RibMaya(object):
	"""Methodes for Rib managment in Maya"""
	def __init__( self ):
		self.output = 'E:/141031_defaultProject/maya/3delight/rib_scene_001/rib/obj/ribObject_python.rib'

	def verbose( self ):
		print 'pouet'
		# print self.ribObject( name='obj1', face='1 1', vtxPerFace='4 4', vtxIndex='0 1 2 3', vtxP='0 0 0 0', n='0 0 0 0', stP='0 0 0 0' )
		return
		print self.help()

	@staticmethod
	def meshInfo( shapeNode ):
		"""Return dict meshInfo for Rib"""
		'@parameter string shapeNode Name of the shape.'

		# init var
		face       = ' '
		vtxPerFace = ' '
		vtxIndex   = ' '
		vtxP       = ' '
		vtxN       = ' '
		stP        = ' '

		for i in maya.cmds.polyInfo( shapeNode, fv=True ):
			# face
			face += '1 '
			
			# vertex index and vertex per face
			countVtx = 0
			for j in i.split( ' ' ) :
				if j.isdigit():
					countVtx += 1
					vtxIndex += '%s ' % ( j )
			vtxPerFace += '%i ' % ( countVtx )

		# vertex position
		for i in maya.cmds.getAttr( '%s.vrts' % ( shapeNode ), mi=True ):
			tmpP = maya.cmds.xform( '%s.pnts[%i]' % ( shapeNode, i ), q=True, t=True, ws=True )
			tmpN = maya.cmds.polyNormalPerVertex('%s.pnts[%i]' % ( shapeNode, i ), q=True, xyz=True )
			vtxP += '%s %s %s ' % ( str(tmpP[0]), str(tmpP[1]), str(tmpP[2]) )
			vtxN += '%s %s %s ' % ( str(tmpN[0]), str(tmpN[1]), str(tmpN[2]) )

		# st position
		for i in range( maya.cmds.polyEvaluate( shapeNode, uvcoord=True ) ) :
			tmpST = maya.cmds.polyEditUV( '%s.map[%i]' % ( shapeNode, i ), q=True )
			stP += '%s %s ' % ( str(tmpST[0]), str(tmpST[1]) )

		# Output in mesh info dict
		meshInfo = { 'face':face, 'vtxPerFace':vtxPerFace, 'vtxIndex':vtxIndex, 'vtxP':vtxP, 'vtxN':vtxN, 'stP':stP }

		return meshInfo

	@staticmethod
	def help():
		"""Return string the help of the class RibMaya"""
		helpString  = '\n ######## class Rib ########'
		helpString += '\n - ribWrite() : Write the rib file.'
		helpString += '\n     - string ribPath Path of the rib file.'
		helpString += '\n     - string content Content of the rib file.'
		helpString += '\n     - bool force Force the write of the rib for override.'

		return helpString




''''''''''''''''''''' tmp work '''''''''''''''''

# TODO fix normal problem and st problem
def writeObjectRib( shapeNode ):
	"""Return dict meshInfo for Rib"""
	'@parameter string shapeNode Name of the shape.'

	path = 'E:/141031_defaultProject/maya/3delight/rib_scene_001/rib/obj/test_python.rib'
	# init var
	face       = ' '
	vtxPerFace = ' '
	vtxIndex   = ' '
	vtxP       = ' '
	vtxN       = ' '
	stP        = ' '

	# init file
	rib = open( path, 'w' )
	rib.write( '\nObjectBegin "%s"' % ( shapeNode ) )
	rib.write( '\n  PointsGeneralPolygons' )
	rib.close()


	# face
	rib = open( path, 'a' )
	rib.write( ' [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.polyInfo( shapeNode, fv=True ) :
		rib.write( '1 ' )
		countLine += 1
		if countLine == 18 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n        ' )
		if countOp > 10 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# vtxPerFace
	rib = open( path, 'a' )
	rib.write( '\n  [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.polyInfo( shapeNode, fv=True ):
		# vertex index and vertex per face
		countVtx = 0
		for j in i.split( ' ' ) :
			if j.isdigit():
				countVtx += 1
		rib.write( '%i ' % ( countVtx ) )
		countLine += 1
		if countLine == 18 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 10 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# vtxIndex
	rib = open( path, 'a' )
	rib.write( '\n  [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.polyInfo( shapeNode, fv=True ):
		for j in i.split( ' ' ) :
			if j.isdigit():
				rib.write( '%s ' % ( j ) )
				countLine += 1
				if countLine == 18 :
					countLine = 0
					countOp += 0.001
					rib.write( '\n    ' )
				if countOp > 10 :
					countOp = 0
					rib.close()
					rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# vtxP
	rib = open( path, 'a' )
	rib.write( '\n  "vertex point P" [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.getAttr( '%s.vrts' % ( shapeNode ), mi=True ):
		tmpP = maya.cmds.xform( '%s.pnts[%i]' % ( shapeNode, i ), q=True, t=True, ws=True )
		rib.write( '%s %s %s ' % ( str(round(tmpP[0], 7)), str(round(tmpP[1], 7)), str(round(tmpP[2], 7)) ) )
		countLine += 1
		if countLine == 4 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 10 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# vtxN
	rib = open( path, 'a' )
	rib.write( '\n  "facevarying normal N" [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.getAttr( '%s.vrts' % ( shapeNode ), mi=True ):
		tmpN = maya.cmds.polyNormalPerVertex('%s.pnts[%i]' % ( shapeNode, i ), q=True, xyz=True )
		rib.write( '%s %s %s ' % ( str(round(tmpN[0], 7)), str(round(tmpN[1], 7)), str(round(tmpN[2], 7)) ) )
		countLine += 1
		if countLine == 4 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 10 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# stP
	rib = open( path, 'a' )
	rib.write( '\n  "facevarying float[2] st" [ ' )
	countLine = 0
	countOp   = 0
	for i in range( maya.cmds.polyEvaluate( shapeNode, uvcoord=True ) ):
		tmpST = maya.cmds.polyEditUV( '%s.map[%i]' % ( shapeNode, i ), q=True )
		rib.write( '%s %s ' % ( str(round(tmpST[0], 7)), str(round(tmpST[1], 7)) ) )
		countLine += 1
		if countLine == 6 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 10 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# close file
	rib = open( path, 'a' )
	rib.write( '\nObjectEnd\n' )
	rib.write( '\nAttributeBegin' )
	rib.write( '\n  ObjectInstance "%s"' % ( shapeNode ) )
	rib.write( '\nAttributeEnd' )
	rib.write( '\n' )
	rib.close()

writeObjectRib( 'pSphereShape1' )

# TODO fix st problem
def writeObjectSubdivRib( shapeNode ):
	"""Return dict meshInfo for Rib"""
	'@parameter string shapeNode Name of the shape.'

	path = 'E:/141031_defaultProject/maya/3delight/rib_scene_001/rib/obj/test_python.rib'
	# init var
	face       = ' '
	vtxPerFace = ' '
	vtxIndex   = ' '
	vtxP       = ' '
	vtxN       = ' '
	stP        = ' '

	# init file
	rib = open( path, 'w' )
	rib.write( '\nObjectBegin "%s"' % ( shapeNode ) )
	rib.write( '\n  SubdivisionMesh "catmull-clark"' )
	rib.close()

	# vtxPerFace
	rib = open( path, 'a' )
	rib.write( ' [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.polyInfo( shapeNode, fv=True ):
		countVtx = 0
		item = i.split( ' ' )
		item.reverse()
		for j in item :
			if j.isdigit():
				countVtx += 1
		rib.write( '%i ' % ( countVtx ) )
		countLine += 1
		if countLine == 18 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 10 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()


	# vtxIndex
	rib = open( path, 'a' )
	rib.write( '\n  [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.polyInfo( shapeNode, fv=True ):
		item = i.split( ' ' )
		item.reverse()
		for j in item :
			if j.isdigit():
				rib.write( '%s ' % ( j ) )
				countLine += 1
				if countLine == 18 :
					countLine = 0
					countOp += 0.001
					rib.write( '\n    ' )
				if countOp > 10 :
					countOp = 0
					rib.close()
					rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()



	# interp
	rib = open( path, 'a' )
	rib.write( '\n[ "interpolateboundary" "facevaryinginterpolateboundary" ] [ 1 0 1 0 ] [ 2 1 ] [ ]\n' )
	rib.close()

	# vtxP
	rib = open( path, 'a' )
	rib.write( '\n  "vertex point P" [ ' )
	countLine = 0
	countOp   = 0
	for i in maya.cmds.getAttr( '%s.vrts' % ( shapeNode ), mi=True ):
		tmpP = maya.cmds.xform( '%s.pnts[%i]' % ( shapeNode, i ), q=True, t=True, ws=True )
		rib.write( '%s %s %s ' % ( str(round(tmpP[0], 7)), str(round(tmpP[1], 7)), str(round(tmpP[2], 7)) ) )
		countLine += 1
		if countLine == 4 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 20 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# stP
	rib = open( path, 'a' )
	rib.write( '\n  "facevarying float[2] st" [ ' )
	countLine = 0
	countOp   = 0
	for i in range( maya.cmds.polyEvaluate( shapeNode, uvcoord=True ) ):
		tmpST = maya.cmds.polyEditUV( '%s.map[%i]' % ( shapeNode, i ), q=True )
		rib.write( '%s %s ' % ( str(round(tmpST[0], 7)), str(round(tmpST[1], 7)) ) )
		countLine += 1
		if countLine == 6 :
			countLine = 0
			countOp += 0.001
			rib.write( '\n    ' )
		if countOp > 20 :
			countOp = 0
			rib.close()
			rib = open( path, 'a' )
	rib.write( ']\n' )
	rib.close()

	# close file
	rib = open( path, 'a' )
	rib.write( '\nObjectEnd\n' )
	rib.write( '\nAttributeBegin' )
	rib.write( '\n  ObjectInstance "%s"' % ( shapeNode ) )
	rib.write( '\nAttributeEnd' )
	rib.write( '\n' )
	rib.close()

writeObjectSubdivRib( 'pSphereShape1' )



'''
shapeNode = 'pCubeShape1'
for i in maya.cmds.polyInfo( fv=True ):
	item = i.split( ' ' )
	item.reverse()
	for j in item :
		if j.isdigit():
			bool = False
			for k in maya.cmds.polyEditUV( '%s.map[%s]' % ( shapeNode, j ), q=True ):
				if bool == True : print round(1-k, 8)
				else : print round(k, 8)
				bool = True