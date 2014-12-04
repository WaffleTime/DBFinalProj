#https://github.com/PyMySQL/PyMySQL
from __future__ import print_function
import pymysql
import logging

cnx = 0
cursor = 0
COUNTER = 0


def setup():
	global cnx
	global cursor

	cnx = pymysql.connect(user='CS', host='isoptera.lcsc.edu', password = "cs445", database='cs445')
	print("Databse Connected")
	cursor = cnx.cursor()
	
def tearDown():
	global cnx
	global cursor	
	cursor.close()
	cnx.commit()
	cnx.close()
	print("DONE")
	
	
setup()


cursor.execute("SELECT * FROM Product_T")

#prints the filed descriptions
print(cursor.description)

#Prints the data from the tables in tuples
for row in cursor:
   print(row)

tearDown()