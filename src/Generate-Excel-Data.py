import mysql.connector
import pandas as pd
import random

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android"
)

EXCEL_FILE = "OUTPUT\\Output-Excel.xlsx"

cursor = conn.cursor()

sql = "SELECT * FROM malware_samples WHERE family = 'ERMAC'"

#sql = "SELECT * FROM mobfs_analysis WHERE id in (66, 67, 68, 69)"

df = pd.read_sql_query(sql, conn)
df.to_excel(EXCEL_FILE)
