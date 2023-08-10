import mysql.connector
import pandas as pd
import openpyxl as xl

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android"
)
cursor = conn.cursor()

EXCEL_FILE_NAME = "MITRE-INPUT.xlsx"
  
wb = xl.load_workbook(EXCEL_FILE_NAME)

for i in wb.sheetnames:
    print("Worksheet: ", i)
    values = list()
    df = pd.read_excel(EXCEL_FILE_NAME, sheet_name = i)

    sql = "INSERT INTO mitre_detection"
    sql = sql + " (Trojan_ID, ATTACK_ID, Tactic, Description, Malicious_Indicators, Suspicious_Indicators, Informative_Indicators)"
    sql = sql + " VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for index, row in df.iterrows():
      trojan_id = row[0]
      attack_id = row[1]
      technique = row[2]
      tactic = row[3]
      mali = row[4]
      susp = row[5]
      info = row[6]

      data = (trojan_id, attack_id, technique, tactic, mali, susp, info)
      print(data) # DEGUGGING
      values.append(data)

      cursor.execute(sql, data)

      #print(cursor.rowcount, "record inserted.")
    # for

    conn.commit()
    print() # newline
  # for