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

SAMPLE_SET = "(63, 73, 74, 79, 84, 85, 89, 90, 93, 98)"

sql = "select * from detected_standard_permissions "
sql = sql + " where id in " + str(SAMPLE_SET)
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

df_beta.to_excel('OUTPUT\\Detected-Standard-Permissions.xlsx')


sql = "select * from detected_unknown_permissions "
sql = sql + " where id in " + str(SAMPLE_SET)
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

df_beta.to_excel('OUTPUT\\Detected-Unknown-Permissions.xlsx')

sql = "select permission_name from android_permissions"
sql = sql + " where permission_status = 'Dangerous' order by permission_name"

cursor.execute(sql)
results = cursor.fetchall()
dangerousPermissionQuery = ""
dangerousPermissionsList = list()
cnt = 1

for x in results:
    if cnt == len(results):
      dangerousPermissionQuery = dangerousPermissionQuery + x[0]
    else:
      dangerousPermissionQuery = dangerousPermissionQuery + x[0] + ", "
    # if
    dangerousPermissionsList.append(x[0])
    cnt = cnt + 1
# for

sql = "select id as 'ID', " + dangerousPermissionQuery
sql = sql + " from detected_standard_permissions"
sql = sql + " where id in " + SAMPLE_SET
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
      print(column)
      df_beta[column] = df_alpha[column]
      break
    # if
  # for
# for

df_beta.to_excel('OUTPUT\\Dangerous-Permissions.xlsx')

sql = "select permission_name from android_permissions"
sql = sql + " where permission_status = 'Normal' order by permission_name"

cursor.execute(sql)
results = cursor.fetchall()
normalPermissionQuery = ""
normalPermissionsList = list()
cnt = 1

for x in results:
    if cnt == len(results):
      normalPermissionQuery = normalPermissionQuery + x[0]
    else:
      normalPermissionQuery = normalPermissionQuery + x[0] + ", "
    # if
    normalPermissionsList.append(x[0])
    cnt = cnt + 1
# for

sql = "select id as 'ID', " + normalPermissionQuery
sql = sql + " from detected_standard_permissions"
sql = sql + " where id in " + SAMPLE_SET
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
      print(column)
      df_beta[column] = df_alpha[column]
      break
    # if
  # for
# for

df_beta.to_excel('OUTPUT\\Normal-Permissions.xlsx')