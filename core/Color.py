
from ColorScience import ColorScience

class Color():
	"""Methodes for Color managment"""
	def __init__(self, color=None):
		self.color = color

	def __repr__(self):
		return repr(self.color)

	def __setitem__(self, key, item):
		if key == 0 or key == 'red' or key == 'r':
			self.color[0] = item

		if key == 1 or key == 'green' or key == 'g':
			self.color[1] = item

		if key == 2 or key == 'blue' or key == 'b':
			self.color[2] = item

		if key == 'hue' or key == 'h':
			hsv = self.getHsv()
			hsv[0] = item
			self.color = ColorScience().hsvToRgb( hsv )

		if key == 'saturation' or key == 's':
			hsv = self.getHsv()
			hsv[1] = item
			self.color = ColorScience().hsvToRgb( hsv )

		if key == 'value' or key == 'v':
			hsv = self.getHsv()
			hsv[2] = item
			self.color = ColorScience().hsvToRgb( hsv )

	def __getitem__(self, key):
		if key == 0 or key == 'red' or key == 'r':
			return self.getRed()

		if key == 1 or key == 'green' or key == 'g':
			return self.getGreen()

		if key == 2 or key == 'blue' or key == 'b':
			return self.getBlue()

		if key == 'hue' or key == 'h':
			return self.getHue()

		if key == 'saturation' or key == 's':
			return self.getSaturation()

		if key == 'value' or key == 'v':
			return self.getValue()

	def setRgb( self, rgb ):
		self.color = rgb

	def setHsv( self, hsv ):
		self.color = ColorScience().hsvToRgb( hsv )


	def getRgb( self ):
		return self.color

	def getRed( self ):
		return self.color[0]

	def getGreen( self ):
		return self.color[1]

	def getBlue( self ):
		return self.color[2]

	def getRgb255( self ):
		return self.color * 255

	def getR255( self ):
		return self.color[0] * 255

	def getG255( self ):
		return self.color[1] * 255

	def getB255( self ):
		return self.color[2] * 255

	def getHsv( self ):
		return ColorScience().rgbToHsv( self.color )

	def getHue( self ):
		return self.getHsv()[0]

	def getSaturation( self ):
		return self.getHsv()[1]

	def getValue( self ):
		return self.getHsv()[2]
