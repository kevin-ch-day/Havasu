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

sql = "SELECT * FROM malware_samples"
sql = sql + " WHERE id in (4, 11, 20, 21, 54, 55, 122, 125)"
sql = sql + " order by id"

sql_query = pd.read_sql_query(sql, conn)
df = pd.DataFrame(sql_query)
df.to_excel('output.xlsx')