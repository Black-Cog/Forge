
class Database(object):
	"""Methodes for Database managment"""
	def __init__( self ):
		self.foo = ''
	
	def verbose( self ):
		print self.foo
		return self.foo

	@staticmethod
	def conection( addr=None, username=None, password=None, dbname=None ):
		""" Return methode doc """
		'@parameter string addr All of the element in the rib.'
		'@parameter string username All of the element in the rib.'
		'@parameter string password All of the element in the rib.'
		'@parameter string dbname All of the element in the rib.'

	@staticmethod
	def insert():
		"""  """

	@staticmethod
	def select():
		"""  """
		return

	@staticmethod
	def update():
		"""  """

	@staticmethod
	def delete():
		"""  """

	@staticmethod
	def close():
		"""  """

	@staticmethod
	def help():
		"""Return string the help of the class Database"""
		helpString  = '\n ######## class Database ########'
		helpString += '\n - conection() : Write the rib file.'
		helpString += '\n     - string addr All of the element in the rib.'
		helpString += '\n     - string username All of the element in the rib.'
		helpString += '\n     - string password All of the element in the rib.'
		helpString += '\n     - string dbname All of the element in the rib.'

		return helpString




