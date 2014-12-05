class Material(object):
    def __init__(self, PK, name, quantity, vendor, unitCost):
        self.PK = PK
        self.name = name
        self.quantity = quantity
        self.vendor = vendor
        #The cost of these materials in total equals
        #   self.quantity*self.unitCost
        self.unitCost = unitCost