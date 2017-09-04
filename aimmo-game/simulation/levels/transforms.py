import hashlib


class CellTransform():
	"""
		A transform is a function callable from objects.json. E.g.:
		  {
		    "code": "1",
		    "id" : "class:CellTransform.compute_id",
		    "x" : "class:CellTransform.get_x",
		    "y" : "class:CellTransform.get_y"
		  }

		A transform has to be registered to a parser.
	"""
	def __init__(self, x, y, width, height):
		centerX = int(width / 2)
		centerY = int(height / 2)

		self.x = +y - centerY
		self.y = -x + centerX

	def compute_id(self):
		return hash(str(self.x) + ":" + str(self.y))

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y
