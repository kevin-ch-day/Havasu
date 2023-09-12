# havasu.py

import ApkAnalysis
import Server

# prompts user to enter a hash to search for
def checkHash():
    hash = input("Enter hash: ")
    if not hash:
        print("No hash entered.")
    else:
        Server.checkHash(hash)

def staticAnalysis():
    ApkAnalysis.

def about():
    pass

def accessDatabase():
    pass