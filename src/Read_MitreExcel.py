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

EXCEL_FILE_NAME = "TEST-EXCEL-BOOK.xlsx"
  
wb = xl.load_workbook(EXCEL_FILE_NAME)

for i in wb.sheetnames:
    print("Worksheet: ", i)
    values = list()
    df = pd.read_excel(EXCEL_FILE_NAME, sheet_name = i)

    sql = "INSERT INTO mitre_detection"
    sql = sql + " (Trojan_ID, Tactic, ATTACK_ID, Description, Malicious_Indicators, Suspicious_Indicators, Informative_Indicators)"
    sql = sql + " VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for index, row in df.iterrows():
      id = i[7:]
      tactic = row[0]
      attack = row[1]
      desc = row[2]
      mali = row[3]
      susp = row[4]
      info = row[5]

      data = (id, tactic, attack, desc, mali, susp, info)
      print(data) # BDEGUGGING
      values.append(data)
    # for

    print() # newline
  # for