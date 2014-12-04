from Material import Material

class Product(object):
    def __init__(self, quantity):
        self.quantity   = quantity
        
        self.columnInfo = {}
        
        #A list of material objects.
        #These are the materials for a single product
        self.materials  = []
        
    def GetPrimaryKey(self):
        """
        This returns the primarykey of the product.
        """
        pass