# Name: main.py

# ==[ IMPORTS ]==
from Tracker import Tracker

# ==[ FUNCTIONS ]==
def present_main_menu() -> int:
    user_choice: int = -1
    while user_choice != 0:
        print("Main Menu:")
        print("[1] View Player Progress")
        print("[2] Add Player Save Data")
        print("[3] Refresh Player Save")
        print("[0] Exit")
        
        try:
            user_choice = int(input("Select an option: "))
        except ValueError:
            continue
        
        if not (user_choice in [0, 1, 2, 3]):
            continue
        else:
            return user_choice
        
    return 0


# ==[ MAIN ]==
def main():
    print("=============================", "\n"*2)

    # initialize tracker
    save_tracker = Tracker()

    # menu loop
    user_choice = present_main_menu()
    user_quit = False
    while not user_quit:
        if user_choice == 0:
            user_quit = True
        elif user_choice == 1:
            print("View Player Progress - Not Implemented Yet")
        elif user_choice == 2:
            print("Add Player Save Data - Not Implemented Yet")
        elif user_choice == 3:
            print("Refresh Player Save - Not Implemented Yet")
        
        if not user_quit:
            user_choice = present_main_menu()


    print("\n"*2, "=============================")


# ==================================== #
if __name__ == "__main__":
    main()