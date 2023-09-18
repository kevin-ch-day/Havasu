# havasu.py

from Analysis import static
from Server import database

__version__ = "1.0.1" # verion number

# prompts user to enter a hash to search for
def checkHash():
    database.checkHash()

def about():
    print("Havasu Version: " + __version__)
    print("A tool for analyzing Android APK files")

def accessDatabase():
    pass

def staticAnalysis():
    static.main()