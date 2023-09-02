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

ANUBIS = "(55, 80, 81, 83, 103, 104, 105)"
permissions = list()

sql = "select * "
sql = sql + "from detected_standard_permissions "
sql = sql + "where id in " + ANUBIS
sql = sql + "order by id"

sql_query = pd.read_sql_query(sql, conn)
df_alpha = pd.DataFrame(sql_query)
df_beta = pd.DataFrame()

df_beta['ID'] = df_alpha['ID']
df_alpha = df_alpha.drop(columns=['ID'])

for column in df_alpha:
  for cell in df_alpha[column]:
    if cell is not None:
      df_beta[column] = df_alpha[column]
      permissions.append(column)
      break
    # if
  # for
# for

sql = "select * from android_permissions"
sql = sql + " where Name in ("

index = 0
for p in permissions:
  if index is (len(permissions)-1):
    sql = sql + "'" + p + "'"
  else:
    sql = sql + "'" + p + "'" + ", "
  # for
  index = index + 1
# for

sql = sql + ") order by Protection_level, Name"

#print("\n# permissions: " +str(len(permissions)))
#print("\n" + sql + "\n") # DEBUGGING

sql_query = pd.read_sql_query(sql, conn)
df = pd.DataFrame(sql_query)
df.to_excel('Results.xlsx')