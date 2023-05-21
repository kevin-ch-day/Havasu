import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android"
)
cursor = conn.cursor()

EXCEL_WORKBOOK_NAME = 'MitreExcelInput.xlsx'

def readExcelMitreSheets():
  sampleList = [61, 62]
  sampleList.sort()

  for i in sampleList:
    sheet = 'Brata ' + str(i)
    print(sheet)

    df = pd.read_excel(EXCEL_WORKBOOK_NAME, sheet_name = sheet)

    sql = "INSERT INTO mitre_detection_temp"
    sql = sql + " (trojan_id, technique_id, technique_description, tactic_description,"
    sql = sql + " malicious_indicators, suspicious_indicators, informative_indicators)"
    sql = sql + " VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for index, row in df.iterrows():
      id = row[0]
      attack = row[1]
      tech = row[2]
      tact = row[3]
      mali = row[4]
      susp = row[5]
      info = row[6]

      val = (id, attack, tech, tact, mali, susp, info)
      cursor.execute(sql, val)
    # for
  # for

  conn.commit()
# function

readExcelMitreSheets()