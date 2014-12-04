class Material(object):
    def __init__(self):
        self.quantity = 0
        
        self.optimalVendor = None
        
        #The cost of these materials in total equals
        #   self.quantity*self.costPerMaterial
        self.costPerMaterial = 0.0