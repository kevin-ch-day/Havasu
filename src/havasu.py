# havasu.py

from Analysis import Static
import Server

# prompts user to enter a hash to search for
def checkHash():
    hash = input("Enter hash: ")
    if not hash:
        print("No hash entered.")
    else:
        Server.checkHash(hash)

def staticAnalysis():
    Static.main()

def about():
    pass

def accessDatabase():
    pass