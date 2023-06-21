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
sql = "SELECT * FROM malware_samples ORDER BY malware_samples.ID ASC"

df_alpha = pd.read_sql_query(sql, conn)
df_alpha.to_excel('OUTPUT\\ResultOutput.xlsx')