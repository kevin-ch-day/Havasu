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

sql = "select id, name, family, md5 from malware_samples order by id"

df = pd.read_sql_query(sql, conn)
df.to_excel('Excel_Output.xlsx')