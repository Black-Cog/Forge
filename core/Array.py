
class Array():
	"""Methodes for array managment"""
	def __init__(self, value=None):
		if not isinstance( value, list ):
			value = [ value ]
		self.value = value

	def __repr__(self):
		return repr(self.value)

	def __getitem__(self, key):
		return self.getItem(key)

	def __setitem__(self, key, item):
		if key >= self.length():
			self.addItem( key, item )
		else:
			self.setItem(key, item)

	def getValue( self ):
		return self.value

	def setValue( self, value ):
		if not isinstance( value, list ):
			value = [ value ]
		self.value = value

	def getItem( self, index ):
		return self.value[index]

	def setItem( self, index, item ):
		self.value[index] = item

	def removeIndex( self, index ):
		del self.value[index]

	def removeItem( self, item ):
		self.value.remove( item )

	def addItem( self, index, item ):
		if index == -1:
			self.value.append( item )
		else:
			if index < -1:
				index += 1
			self.value.insert( index, item )

	def extend( self , list ):
		self.value.extend( list )

	def sort( self ):
		self.value.sort()

	def reverse( self ):
		self.value.reverse()

	def length( self ):
		return len( self.value )

	def count( self, item ):
		return self.value.count( item )

	def index( self, item ):
		return self.value.index( item )
