
class Int():
	"""Methodes for Int managment"""
	def __init__(self, value=None):
		self.value = int( value )

	def __repr__(self):
		return repr(self.value)

	def setValue( self, value ):
		self.value = int( value )

	def getValue( self ):
		return self.value
