
class Float():
	"""Methodes for Float managment"""
	def __init__(self, value=None):
		self.value = float( value )

	def __repr__(self):
		return repr(self.value)

	def setValue( self, value ):
		self.value = float( value )

	def getValue( self ):
		return self.value
