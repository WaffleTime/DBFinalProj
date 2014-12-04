from __future__ import print_function
import pymysql
import logging

class Controller(object):
	"""
	The middleman inbetween the database connection engine and the GUI.
	"""
	
	cnx = 0
	cursor = 0
	pendingProducts = []
	
	def setup(cls):
		cls.cnx = pymysql.connect(user='CS', host='isoptera.lcsc.edu', password = "cs445", database='cs445')
		print("Databse Connected")
		cls.cursor = cnx.cursor()
		
    def tearDown(cls):
        cls.cursor.close()
        cls.cnx.commit()
        cls.cnx.close()
        print("DONE")

		
    def AddProduct(cls, productPK, quantity):
        """
        This adds to the self.pendingProducts list with Product objects that
        have been built using data from the database.
        @param productPK 	The primary key of the product that is to be add.
        @param quantity 	The amount of products that is being added.
        """
        cursor.execute("SELECT * FROM Product_T")
		
        for row in cursor:
            print(row)