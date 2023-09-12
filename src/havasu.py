# havasu.py

from Analysis import static
import Server

__version__ = "1.0.1" # verion number

# prompts user to enter a hash to search for
def checkHash():
    hash = input("Enter hash: ")
    if not hash:
        print("No hash entered.")
    else:
        Server.checkHash(hash)
    # if

def about():
    print("Havasu Version: " + __version__)
    print("A tool for analyzing Android APK files")

def accessDatabase():
    pass

def staticAnalysis():
    static.main()