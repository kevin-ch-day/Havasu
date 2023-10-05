# main.py
# Main application driver for havasu

from Analysis import static
from Server import dataAnalysis as server

__version__ = "1.0.1" # verion number

# main
def main():
    print("*~*~*~* Havasu *~*~*~*")
    
    while True:
        menuChoices()
        menuChoice = input("Select choice: ")
        menuChoice = int(menuChoice)

        if menuChoice == 0: # Exit Application
            print("Exiting.")
            exit(0)
        
        elif menuChoice == 1: # Static analysis
            print("Static Analysis\n")
            static.run()
        
        elif menuChoice == 2: # APK Data Analysis
            print("APK Data Analysis\n")
            server.run()

        elif menuChoice == 3: # About
            about()

        elif menuChoice == 4: # Help
            help()
        
        else:
            print("Invalid Selected\n")

# Menu Choices
def menuChoices():
    print("\nMain Menu")
    print(" 1 - Static Analysis")
    print(" 2 - APK Data Analysis")
    print(" 3 - About")
    print(" 4 - Help")
    print(" 0 - Exit\n")

# about
def about():
    print("Havasu Version: " + __version__)
    print("A tool for analyzing Android APK files")

# help
def help():
    print("Help")

# run app
if __name__ == "__main__":
   main()