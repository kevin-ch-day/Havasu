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

def main():
    hashes = list()

    f = open("newHashes.txt")
    for i in f:
        hashes.append(i.strip())
    # for

    if checkHashes(hashes):
        print("Existing Hashes: ")
        for i in hashes:
            print(i)
        # for
        exit()
    # if

    sql = "select max(id) from malware_samples"
    cursor.execute(sql)
    x = cursor.fetchall()
    currentID = x[0][0]
    values = list()

    sql = "insert into malware_samples (id, md5) values (%s, %s)"
    for i in hashes:
        currentID = currentID + 1
        values.append((currentID, i))
    # for

    cursor.executemany(sql, values)
    conn.commit()
    recordsInserted(cursor.rowcount)
# main

def recordsInserted(count):
    if count == 0:
        print("No records inserted.")
    elif count == 1:
        print(count, "record inserted.")
    else:
        print(count, "records inserted.")
    # match
# function

def checkHashes(hashes):
    sql = "SELECT md5 FROM malware_samples"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    buffer = list()

    for i in hashes:
        if i in results:
            buffer.add(i)
        # if
    # for

    if buffer:
        return buffer
    else:
        return None
    # if
# end

main()