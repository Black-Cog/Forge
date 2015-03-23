
class Compound():
	"""Methodes for compound managment"""
	def __init__(self, value={}):
		self.value = value
		if not isinstance( value, dict ):
			self.value = {}

	def __repr__(self):
		return repr(self.value)

	def __getitem__(self, key):
		return self.getItem(key)

	def __setitem__(self, key, item):
		self.setItem(key, item)

	def getValue( self ):
		return self.value

	def setValue( self, value ):
		self.value = value
		if not isinstance( value, dict ):
			self.value = {}

	def getItem( self, index ):
		return self.value[index]

	def setItem( self, index, item ):
		self.value[index] = item

	def removeIndex( self, index ):
		del self.value[index]

	def length( self ):
		return len( self.value )
