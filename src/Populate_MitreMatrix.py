import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="cyberops_capstone_android")

cursor = conn.cursor()

def getMitreColumns():
  print("getMitreColumns()")
  columns = set() # empty set

  sql = "select DISTINCT Tactic, ATTACK_ID"
  sql = sql + " from mitre_detection"
  sql = sql + " order by Tactic, ATTACK_ID, Description"

  results = pd.read_sql_query(sql, conn)
  records = pd.DataFrame(results)

  for index, row in records.iterrows():
      col = row[0] + " " + row[1]
      columns.add(col)
  # for

  return sorted(columns)
# function

def getMitreDict():
  print("getMitreDict()")

  dict_mitre = dict()  
  for i in getMitreColumns():
    dict_mitre[i] = list()
  # for

  sql = "SELECT Tactic, ATTACK_ID, trojan_id"
  sql = sql + " FROM mitre_detection"
  sql = sql + " order by trojan_id, Tactic, ATTACK_ID"

  results = pd.read_sql_query(sql, conn)
  df_samples = pd.DataFrame(results)

  for index, row in df_samples.iterrows():
    key = row[0] + " " + row[1]
    items = dict_mitre[key]
    items.append(row[2])
    items.sort()
    dict_mitre[key] = items
  # for

  return dict_mitre
# function

def getMitreMatrixColumns():
  print("getMitreMatrixColumns()")

  sql = "SHOW COLUMNS FROM mitre_matrix"
  results = pd.read_sql_query(sql, conn)
  
  cols = results.loc[:, 'Field']  
  cols = cols.drop(cols.index[0])

  return cols.tolist()
# function

def getSampleIds():
  print("getSampleIds()")

  sql = "select DISTINCT trojan_id from mitre_detection"
  results = pd.read_sql_query(sql, conn)
  records = pd.DataFrame(results)
  
  temp = list()
  for i in records.loc[:, 'trojan_id']:
      temp.append(i)
  # for

  temp.sort()

  return temp
# function

def addIdsMitreMatrix():
  print("addIdsMitreMatrix()")

  samples = getSampleIds()

  for index in samples:
    sql = "select * from mitre_matrix where trojan_id = " + str(index)
    results = pd.read_sql_query(sql, conn)
      
    if results.empty:
      sql = "insert into mitre_matrix (trojan_id) value (%s)"
      cursor.execute(sql, (str(index),))
      conn.commit()

      print("Added sample id: " + str(index))
    # if
  # for

  print() # newline
# function


def main_driver():
  addIdsMitreMatrix()

  columns = getMitreMatrixColumns()
  dict_mitreMatrix = getMitreDict()
  
  # iterator to find any missing columns 
  for index in dict_mitreMatrix:
    
    # check if column does not exist in the table
    if index not in columns:
      print(index + " Does not exist")
      sql = "ALTER TABLE `mitre_matrix` ADD `"+ index +"` varchar(1) null"
      cursor.execute(sql)
      conn.commit()
    # if
  # for
  print() # newline

  for key in dict_mitreMatrix:
    print(key)
    values = dict_mitreMatrix[key]
    
    for i in values:
      sql = "UPDATE mitre_matrix SET `" + key + "` = 'X' WHERE trojan_id = " + str(i)
      cursor.execute(sql)
      conn.commit()
    # for
  # for
# function

main_driver()