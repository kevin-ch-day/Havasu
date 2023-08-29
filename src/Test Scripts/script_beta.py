import mysql.connector
import pandas as pd
import sys

import mysql.connector
import pandas as pd
import random

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android"
)
cursor = conn.cursor()

sql = "select id from malware_samples "
sql = sql + "where family = 'Brata' order by id"

cursor.execute(sql)
result = cursor.fetchall()

s = "("
for x in result:
  s = s + str(x[0]) + ", "
s = s + ")"

print(s)