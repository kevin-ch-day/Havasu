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

sql = "select * from mitre_matrix"
#sql = sql + " where trojan_id in (60, 61, 62, 101, 171, 172)"
sql = sql + " order by trojan_id"

df_alpha = pd.read_sql_query(sql, conn)
df_beta = pd.DataFrame()

df_beta['trojan_id'] = df_alpha['trojan_id']
df_alpha = df_alpha.drop(columns=['trojan_id'])

for column in df_alpha:
  for cell in df_alpha[column]:
    if cell is not None:
      df_beta[column] = df_alpha[column]
      break
    # if
  # for
# for

df_beta.to_excel('Mitre_Matrix.xlsx')