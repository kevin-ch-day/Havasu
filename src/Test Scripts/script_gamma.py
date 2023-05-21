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

sql = "select *"
sql = sql + " from detected_standard_permissions "
sql = sql + " where trojan_id in (4, 11, 20, 21, 55, 122, 125)"
sql = sql + " order by trojan_id"

sql_query = pd.read_sql_query(sql, conn)
df_alpha = pd.DataFrame(sql_query)
df_beta = pd.DataFrame()

df_alpha = df_alpha.drop(columns=['scan_id'])

df_beta['trojan_id'] = df_alpha['trojan_id']

df_alpha = df_alpha.drop(columns=['trojan_id'])

columnNotEmpty = False
count = 0

# loop through columns
for column in df_alpha:

  # loop through each column row
  for i in df_alpha[column]:

    # if cell has data
    if i is not None:
      columnNotEmpty = True
      break
    # if
  # for

  if columnNotEmpty:
    df_beta[column] = df_alpha[column]
  # if

  columnNotEmpty = False
# for

df_beta.to_excel('Permission_Sheet.xlsx')