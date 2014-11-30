#!/usr/bin/env python

from __future__ import print_function

import pymysql

conn = pymysql.connect(host='isoptera.lcsc.edu', port=3306, user='fcm', passwd='cs480fcm', db='FCM')

cur = conn.cursor()

cur.execute("SELECT Host,User FROM user")

print(cur.description)

print()

for row in cur:
   print(row)

cur.close()
conn.close()
