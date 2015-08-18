
import math

class ColorScience():
	"""Methodes relative at Color Science"""
	
	@staticmethod
	def linearToSrgb(color):
		colorOut = []

		for i in range(3):
			if color[i] <= 0.0031308:
				colorTmp = color[i] * 12.92
				colorOut.append( round(colorTmp, 6) )
			else:
				colorTmp = 1.055 * ( pow(color[i], 1 / 2.4) ) - 0.055
				colorOut.append( round(colorTmp, 6) )

		return colorOut

	@staticmethod
	def srgbToLinear(color):
		colorOut = []

		for i in range(3):
			if color[i] <= 0.04045:
				colorTmp = color[i] / 12.92
				colorOut.append( round(colorTmp, 6) )
			else:
				colorTmp = pow(  ( (color[i]+0.055) / 1.055 ), 2.4  )
				colorOut.append( round(colorTmp, 6) )

		return colorOut

	@staticmethod
	def floatToBits8(color):
		return [ int(i*255) for i in color ]

	@staticmethod
	def bits8ToFloat(color):
		return [ float(i/255) for i in color ]

	@staticmethod
	def applyLut(color, lut):
		return None

	@staticmethod
	def removeLut(color, lut):
		return None

	def rgbToHsv(self, color):
		# todo : fix forumla to don't have to make this ugly colorspace convertion
		# colorSrgb = self.linearToSrgb( color )
		colorSrgb = color

		r = colorSrgb[0]
		g = colorSrgb[1]
		b = colorSrgb[2]

		mini = min( r, g, b )
		maxi = max( r, g, b )
		v = maxi
		delta = maxi - mini

		if maxi:
			s = delta / maxi
		else:
			s = 0
			h = -1
			return [ h, s, v ]

		if delta:
			if r == maxi:
				h = ( g - b ) / delta
			elif g == maxi:
				h = 2 + ( b - r ) / delta
			else:
				h = 4 + ( r - g ) / delta

			h *= 60.0

			if h < 0 : h += 360
			h /= 360.0

		else:
			h = 0

		return [ h, s, v ]

	def hsvToRgb(self, color):
		h = color[0]
		s = color[1]
		v = color[2]

		step = h / (1.0 / 6.0)
		pos = step - math.floor( step )

		if math.floor(step) % 2 : m = ( 1.0 - pos ) * v
		else : m = pos * v

		maximum = 1.0 * v
		minimum = (1.0 - s) * v
		medium  = m + ( (1.0 - s)*(v - m) )

		switchValue = math.floor( step )
		if switchValue == 0:
			r = maximum
			g = medium
			b = minimum
		if switchValue == 1:
			r = medium
			g = maximum
			b = minimum
		if switchValue == 2:
			r = minimum
			g = maximum
			b = medium
		if switchValue == 3:
			r = minimum
			g = medium
			b = maximum
		if switchValue == 4:
			r = medium
			g = minimum
			b = maximum
		if switchValue == 5 or switchValue == 6 or switchValue == -6 :
			r = maximum
			g = minimum
			b = medium

		rgb = [r, g, b]

		# todo : fix forumla to don't have to make this ugly colorspace convertion
		# rgb = self.srgbToLinear( rgb )

		return rgb

	def hslToRgb(self, color):
		h = color[0]
		s = color[1]
		l = color[2]

		if s == 0:
			r = l
			g = l
			b = l
		else:
			def hueTorgb(p, q, t):
				if(t < 0.0) : t += 1.0
				if(t > 1.0) : t -= 1.0
				if(t < 1.0/6.0) : return p + (q - p) * 6.0 * t
				if(t < 1.0/2.0) : return q
				if(t < 2.0/3.0) : return p + (q - p) * (2.0/3.0 - t) * 6.0
				return p

			if l < 0.5 : q = l * (1.0 + s)
			else : q = l + s - l * s
			p = 2.0 * l - q

			r = hue2rgb( p, q, h + 1.0/3.0 )
			g = hue2rgb( p, q, h )
			b = hue2rgb( p, q, h - 1.0/3.0 )

		rgb = [r, g, b]

		# todo : fix forumla to don't have to make this ugly colorspace convertion
		rgb = self.srgbToLinear( rgb )

		return rgb
