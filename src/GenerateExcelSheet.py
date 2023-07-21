import mysql.connector
import pandas as pd
import random

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android"
)


EXCEL_FILE_NAME = "SHARKBOT.xlsx"

cursor = conn.cursor()

sql = "select * from malware_samples where family = 'sharkbot' order by id"

df = pd.read_sql_query(sql, conn)
df.to_excel(EXCEL_FILE_NAME)