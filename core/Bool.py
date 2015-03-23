
class Bool():
	"""Methodes for boolean managment"""
	def __init__(self, value=None):
		self.value = bool( int(value) )

	def __repr__(self):
		return repr(self.value)

	def setValue( self, value ):
		self.value = bool( int(value) )

	def getValue( self ):
		return self.value
