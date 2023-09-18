# main.py
# Main application driver for havasu

from Analysis import static
from Server import main as server

__version__ = "1.0.1" # verion number

# main
def main():
    print("*~*~*~* Havasu *~*~*~*")
    while True:
        menuChoices()
        menuChoice = input("Select choice: ")
        menuChoice = int(menuChoice)
        if menuChoice == 0:
            print("Exiting.")
            exit(0)
        
        elif menuChoice == 1: # Static analysis
            print("Static Analysis\n")
            static.main()
        
        elif menuChoice == 2: # Access database
            print("Access Database\n")
            server.main()

        elif menuChoice == 3: # About
            print("Havasu Version: " + __version__)
            print("A tool for analyzing Android APK files")

        elif menuChoice == 4: # Help
            print("Help")
        
        else:
            print("Invalid Selected\n")
        # if
    # menu
# main

# Menu Choices
def menuChoices():
    print("\nMain Menu")
    print(" 1 - Access Database")
    print(" 2 - Static Analyis")
    print(" 3 - About")
    print(" 4 - Help")
    print(" 0 - Exit\n")

# run app
if __name__ == "__main__":
   main()
# if