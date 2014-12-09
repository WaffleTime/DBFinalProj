from __future__ import print_function
import pymysql
import logging

from Product import Product

class Controller(object):
    """
    The middleman inbetween the database connection engine and the GUI.
    """
    
    cnx = 0
    cursor = 0
    pendingProducts = []
    
    @classmethod
    def Setup(cls):
        cls.cnx = pymysql.connect(user='CS', host='isoptera.lcsc.edu', password = "cs445", database='cs445')
        print("Databse Connected")
        cls.cursor = cls.cnx.cursor()
        
    @classmethod
    def TearDown(cls):
        cls.cursor.close()
        cls.cnx.commit()
        cls.cnx.close()
        print("DONE")

    @classmethod
    def GetPossibleProducts(cls):
        """
        Fetches a list of the Products that this company is able to sell.
        @return
            A list of primary keys for the products and a list of names for the products. 
            (Maybe a dictionary would have been better to use... whatever.)
        """
        cls.cursor.execute("SELECT * FROM Product_T")
        
        productIds      = []
        productNames    = []
        
        for row in cls.cursor:
            if (row[0] != None and row[2] != None and row[3] != None):
                if (len(productIds) == 0):
                    productIds.append(row[0])
                    productNames.append("%s-%s"%(row[2], row[3]))
                else:
                    for i in range(len(productIds)):
                        productName = "%s-%s"%(row[2], row[3])
                        if (productName < productNames[i]):
                            productIds.insert(i, row[0])
                            productNames.insert(i, productName)
                            break
                        elif (i == len(productIds)):
                            productIds.append(row[0])
                            productNames.append(productName)
                            break
            
        return productIds, productNames
        
    @classmethod
    def GetProduct(cls, productPK):
        product = None
        for i in range(len(cls.pendingProducts)):
            if (str(cls.pendingProducts[i].PK) == str(productPK)):
                product = cls.pendingProducts[i]
                break
                
        return product
        
    @classmethod
    def RemoveProduct(cls, productPK, amountToRemove):
        """
        This subtracts from a product's quantity until the quantity is zero. Then
        the product is removed entirely.
        """
        for i in range(len(cls.pendingProducts)):
            if (cls.pendingProducts[i].PK == int(productPK)):
                if (cls.pendingProducts[i].quantity - amountToRemove <= 0):
                    del cls.pendingProducts[i]
                    break
                else:
                    cls.pendingProducts[i].quantity -= amountToRemove
                    break
        
    @classmethod
    def AddProduct(cls, productPK, quantity):
        """
        This adds to the self.pendingProducts list with Product objects that
        have been built using data from the database.
        @param productPK    The primary key of the product that is to be add.
        @param quantity     The amount of products that is being added.
        
        @return Returns the Product object that was just created or added to.
        """
        cls.cursor.execute("SELECT * FROM Product_T WHERE ProductID='%s'"%(productPK))
        
        product = cls.GetProduct(productPK)
        
        if (product == None):
            product = Product(quantity)
            
            columnNames = []
            
            for column in cls.cursor.description:
                columnNames.append(column[0])
                
            #Add those columns to the Product object!
            if (not product.AddColumns(columnNames, list(cls.cursor)[0])):
                print("AddColumns failed within Controller.AddProduct!")
            
            #Query vendors and materials and add that info to the product.
            #...
            #...
            #...
            #...
            #...
            
            cls.pendingProducts.append(product)
        else:
            product.quantity += quantity
        
        return product