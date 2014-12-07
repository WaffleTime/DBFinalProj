from Material import Material
import random

class Product(object):
    def __init__(self, quantity):
        self.quantity   = quantity
        
        self.columnInfo = {}
        
        self.PK = ""
        
        #A list of material objects.
        #These are the materials for a single product
        self.materials  = []
        
    def AddColumns(self, columnNames, columnValues):
        """
        This takes in a list of column names and column values. Then it maps those
        two lists together and saves the results to self.columnInfo
        @param columnNames A list of columnNames for the Product_T table.
        @param columnValues A list of columnValues for this specific product in Product_T.
        @return A boolean telling whether this was a success or not.
        """
        success = False
        
        if (len(columnNames) == len(columnValues)):
            success = True
            self.PK = columnValues[0]
            for i in range(len(columnNames)):
                self.columnInfo[columnNames[i]] = columnValues[i]
                
        self.AddMaterial(str(random.randint(0,100)), "test", "5", "Albertsons", "500000")
                
        return success
        
    def AddMaterial(self, PK, name, quantity, vendor, unitCost):
        self.materials.append(Material(PK, name, quantity, vendor, unitCost))