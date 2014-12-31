
class Database(object):
	"""Methodes for Database managment"""
	def __init__( self ):
		self.foo = ''
	
	def verbose( self ):
		print self.foo
		return self.foo

	@staticmethod
	def conection( addr=None, username=None, password=None, dbname=None ):
		""" Method for conection to Mysql database """
		'@parameter string addr Address of the Mysql server.'
		'@parameter string username Username of the database.'
		'@parameter string password Password of the user.'
		'@parameter string dbname Name of the database.'

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




