import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android"
)
cursor = conn.cursor()

EXCEL_WORKBOOK_NAME = 'Excel_Input.xlsx'

df = pd.read_excel(EXCEL_WORKBOOK_NAME, sheet_name = 'Main')

# get last record id
sql = "select max(id) from malware_samples"
cursor.execute(sql)
result = cursor.fetchall()
if result[0][0] == None:
    print("No Records Found.")
    exit
else:
    id = result[0][0] + 1 # increment by 1
    print(type(id))
# if

sql = "INSERT INTO malware_samples"
sql = sql + " (ID, Name, MD5)"
sql = sql + " VALUES (%s, %s, %s)"

for index, row in df.iterrows():
    name = row[0]
    md5 = row[1]
    
    val = (str(id), name, md5)
    cursor.execute(sql, val)
    id = id + 1
# for

conn.commit()
