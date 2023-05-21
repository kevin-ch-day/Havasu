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

sql = "SHOW COLUMNS FROM detect_stand_perms LIKE 'CAPTURE_SECURE_VIDEO_OUTPUT'"
cursor.execute(sql)
results = cursor.fetchall()
if results:
  pass
# if