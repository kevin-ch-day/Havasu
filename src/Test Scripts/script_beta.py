import mysql.connector
import pandas as pd
import sys

def main(argv):
    print(argv[0])
# main

if __name__ == "__main__":
    if not sys.argv[1:]:
       print("Error")
       exit()
    else:
        main(sys.argv[1:])
    # if
# if