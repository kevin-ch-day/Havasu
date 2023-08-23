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

sql = "select * from mitre_matrix "
sql = sql + " where trojan_id in (44, 45, 114, 115)"
sql = sql + " order by trojan_id"

df_raw = pd.read_sql_query(sql, conn)

cols = df_raw.columns.tolist()
cols.sort()
cols.remove('trojan_id')

df_beta = pd.DataFrame()
df_beta['trojan_id'] = df_raw['trojan_id']
df_alpha = df_raw.drop(columns=['trojan_id'])

for column in cols:
  for cell in df_alpha[column]:
    if cell is not None:
      df_beta[column] = df_alpha[column]
      break
    # if
  # for
# for

df_beta.to_excel('Mitre-Matrix.xlsx')