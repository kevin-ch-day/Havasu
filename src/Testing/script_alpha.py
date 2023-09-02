import mysql.connector
import pandas as pd
import sys

def main(argv):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    #password="yourpassword",
    database="cyberops_capstone_android")

    cursor = conn.cursor()
    sql = "select x.id, "
    sql = sql + "x.size, "
    sql = sql + "y.activities, "
    sql = sql + "y.services, "
    sql = sql + "y.receivers, "
    sql = sql + "y.providers "
    sql = sql + "from malware_samples x "
    sql = sql + "join mobfs_analysis y "
    sql = sql + "on y.id = x.id "
    sql = sql + "where x.family = '"+argv[0]+"' "
    sql = sql + "order by x.id "

    cursor.execute(sql)
    results = cursor.fetchall()

    print() # newline
    for row in results:
        buff = ""
        cnt = 0

        for element in row:
            if cnt == (len(row) - 1):
                buff = buff + str(element) + " \\\\"
            else:
                buff = buff + str(element) + " & "
            # if

            cnt = cnt + 1 # increment
        # for

        print(buff)
    # for

    print() # newline
# main

if __name__ == "__main__":
    if not sys.argv[1:]:
       print("Error: no malware family name given")
       exit()
    else:
        main(sys.argv[1:])
    # if
# if