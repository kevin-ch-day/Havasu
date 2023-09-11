# main.py
# Main app driver for havasu

import havasu

__version__ = "1.0.1"

def main():
    while True:
        menuChoices()
        menuChoice = input("Select choice: ")
        if menuChoice == 0:
            print("Exiting.")
            exit(0)
        
        elif menuChoice == 1:
            print("Access Database")

        elif menuChoice == 2:
            print("Static Analysis")
        
        elif menuChoice == 3:
            print("Check Hash")
            havasu.checkHash()
        
        elif menuChoice == 4:
            print("About Application")
        
        else:
            print("Invalid Selected")
        # if
    # menu loop
# main

def menuChoices():
    print("1 - Access Database")
    print("2 - Static Analysis")
    print("3 - Check Hash")
    print("4 - About Application")
    print("0 - Exit")

if __name__ == "__main__":
   main() # run app
# if