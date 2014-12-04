class Controller(object):
	"""
	The middleman inbetween the database connection engine and the GUI.
	"""
	def __init__(self):
		#A list of the products that the user has selected to order so far.
		self.pendingProducts = []
		
		#SQLConnectionEngine instance
		
	def AddProduct(self, productPK, quantity):
		"""
		This adds to the self.pendingProducts list with Product objects that
		have been built using data from the database.
		@param productPK 	The primary key of the product that is to be add.
		@param quantity 	The amount of products that is being added.
		"""
		pass