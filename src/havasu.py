# havasu.py

from Analysis import static
from Server import main as server

__version__ = "1.0.1" # verion number

def about():
    print("Havasu Version: " + __version__)
    print("A tool for analyzing Android APK files")

def help():
    print("Help")

def accessDatabase():
    server.main()

def staticAnalysis():
    static.main()