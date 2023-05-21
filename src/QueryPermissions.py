import mysql.connector
import pandas as pd
import random

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops-androidbanking"
)

cursor = conn.cursor()

sql = "select permission_name from standard_android_permissions where permission_status = 'Dangerous' order by permission_name"
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

sql = "select trojan_id, " + dangerousPermissionQuery
sql = sql + " from detected_trojan_standard_permissions"
sql = sql + " order by trojan_id"

sql_query = pd.read_sql_query(sql, conn)
df = pd.DataFrame(sql_query)

df.dropna(how='all', axis=1, inplace=True)

#df.to_excel('Permissions.xlsx')
s = df.count()
dict = s.to_dict()

#dict.pop("scan_id")
dict.pop("trojan_id")

f = open("permission_results.txt", "w")
for key, value in dict.items():
   f.write(str(value) + " " + key + "\n")
# for
f.close()
