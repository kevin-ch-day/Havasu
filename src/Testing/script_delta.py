import mysql.connector
import pandas as pd
import random

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="havasu_dev"
)
cursor = conn.cursor()

SAMPLE_SET = "(55, 80, 81, 83, 103, 104, 105, 6, 7, 18, 19, 20, 117, 663, 73, 74, 79, 84, 85, 89, 90, 93, 98,"
SAMPLE_SET = SAMPLE_SET + " 17, 27, 28, 112, 1, 40, 41, 120, 121, 8, 29, 30, 31, 32, 33, 36, 37, 15, 16, 51, 109, 110,"
SAMPLE_SET = SAMPLE_SET + " 44, 45, 114, 115, 23, 24, 25, 26)"

sql = "select ID, MD5, Kaspersky_Label "
sql = sql + "from malware_samples "
sql = sql + "where id in " + SAMPLE_SET
sql = sql + " order by id"

#print(sql)

buffer = list()
results = pd.read_sql_query(sql, conn)
df = pd.DataFrame(results)

with open('results.txt', 'w') as f:
  for index, row in df.iterrows():
      temp = str(row['ID']) + " & " + row['Kaspersky_Label'] + " & " + row['MD5'] + " \\\\\n" 
      f.write(temp)

#df_alpha.to_excel('Results.xlsx')