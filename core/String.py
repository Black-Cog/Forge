
class String( str ):
	"""Methodes for string managment"""
	def __init__(self, value=None):
		self.value = value

	def __repr__(self):
		return repr(self.value)

	def setValue( self, value ):
		self.value = value

	def getValue( self ):
		return self.value
