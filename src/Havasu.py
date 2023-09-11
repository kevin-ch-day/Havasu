# havasu.py

import StaticAnalysis
import Server

# prompts user to enter a hash to search for
def checkHash():
    hash = input("Enter hash: ")
    if not hash:
        print("No hash entered.")
    else:
        Server.checkHash(hash)

def staticAnalysis():
    pass

# Decompile APK file
def decompileAPK():
    pass