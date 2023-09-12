# main.py
# Main app driver for havasu

import havasu

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
        
        elif menuChoice == 1:
            print("Access Database\n")
            havasu.accessDatabase()

        elif menuChoice == 2:
            havasu.staticAnalysis()
        
        elif menuChoice == 3:
            print("Check Hash\n")
            havasu.checkHash()
        
        elif menuChoice == 4:
            print("About Application\n")
            havasu.about()
        
        else:
            print("Invalid Selected\n")
        # if
    # menu
# main

def menuChoices():
    print("\nMain Menu")
    print(" 1 - Access Database")
    print(" 2 - Static Analysis")
    print(" 3 - Check Hash")
    print(" 4 - About Application")
    print(" 0 - Exit\n")

if __name__ == "__main__":
   main() # run app
# if