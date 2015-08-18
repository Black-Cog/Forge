
from Rib import Rib
from System import System
from Process import Process
from Env import Env
# todo add Database for mySQL implementation
# from Database import Database
from ColorScience import ColorScience

# datas
from Bool import Bool
from Int import Int
from Float import Float
from Color import Color
from String import String
from Array import Array
from Compound import Compound

def help():
	"""Return string the help of the module ForgeCore"""
	helpString  = '\n ######## module ForgeCore ########'
	helpString += '\n - System()   : Methodes for System managment.'
	helpString += '\n - Process()  : Methodes for Process managment.'
	helpString += '\n - Rib()      : Methodes for Rib managment.'
	helpString += '\n - Database() : Methodes for Database managment.'

	return helpString
