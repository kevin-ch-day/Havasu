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
sql = sql + " where id in (63, 73, 74, 78, 79, 84, 85, 88, 89, 90)"
sql = sql + " order by id"

sql_query = pd.read_sql_query(sql, conn)
df_alpha = pd.DataFrame(sql_query)
df_beta = pd.DataFrame()

#df_alpha = df_alpha.drop(columns=['scan_id'])
df_beta['ID'] = df_alpha['ID']
df_alpha = df_alpha.drop(columns=['ID'])

for column in df_alpha:
  for cell in df_alpha[column]:
    if cell is not None:
      df_beta[column] = df_alpha[column]
      break
    # if
  # for
# for

df_beta.to_excel('OUTPUT\\RecordedPermissions.xlsx')