# Tracker.py
# Description: This file contains the Tracker class, which is responsible for
#              tracking player progress in the game.

# ==[ IMPORTS ]==
import os
from typing import Set
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


# ==[ CONSTANTS ]==
DECYPHER_KEY = "68 00 33 00 79 00 5F 00 67 00 55 00 79 00 5A 00"
SAVE_FILE_PATH = {
    os.path.join(os.getenv("USERPROFILE"), "Documents", "My Games", "Terraria", "Players"),
    os.path.join(os.getenv("USERPROFILE"), "OneDrive", "Documents", "My Games", "Terraria", "Players")
}
ALL_RESEARCHABLE_ITEMS = {}
DELIMITER = "|"


# ==[ FUNCTIONS ]==
# Name: load_researchable_items() -> None
# Desc: Loads the list of all researchable items from `./RESEARCH_ITEMS.txt`
#       into the ALL_RESEARCHABLE_ITEMS set
# Preconditions: `./RESEARCH_ITEMS.txt` exists
# Postconditions: ALL_RESEARCHABLE_ITEMS is populated
def load_researchable_items() -> None:
    # line format: ID|Name|Internal Name
    try:
        with open("RESEARCH_ITEMS.txt", "r"):
            pass
    except FileNotFoundError:
        print("Could not locate research items file: \"RESEARCH_ITEMS.txt\"")

# Name: prompt_yn(prompt: str) -> bool
# Desc: Prompts the user with a yes/no question until a valid response is given
# Preconditions: None
# Postconditions: None
# Returns: True if the user responds with 'Y' or 'y', False otherwise
def prompt_yn(prompt: str) -> bool:
    valid_answer: bool = False
    while not valid_answer:
        manual_check = input(prompt + " (Y/N) ")
        if manual_check.lower() == "y":
            return True
        elif manual_check.lower() == "n":
            return False
        else:
            print("Please enter either Y or N.")


def determine_save_path() -> str:
    chosen_path: str = ""

    # determine save path
    for path in SAVE_FILE_PATH:
        if not does_path_exist(path):
            continue

        print("Checking directory:", path)
        
        is_save_path: bool = check_save_directory(path)

        if is_save_path:
            chosen_path = path
    
    # user manual check (optional)
    manual_check: bool = prompt_yn("Would you like to manually check these directories?")

    # only check for yes, skip if no
    if manual_check:
        for path in SAVE_FILE_PATH:
            if not does_path_exist(path):
                continue

            # print contents of directory
            print_directory_contents(path)
            
            # ask user if this is the correct path
            user_choice: bool = prompt_yn("Do these files look correct to you?")
            if user_choice:
                chosen_path = path
                break

    print("Selected path:", chosen_path, "\n")

    # get specific save
    save_path: str = get_save(chosen_path)
    return save_path


# Name: does_path_exist(path: str) -> bool
# Desc: Checks if the given path exists on the system.
# Preconditions: None
# Postconditions: None
# Returns: True if the path exists, False otherwise
def does_path_exist(path: str) -> bool:
    return os.path.exists(path)


# Name: print_directory_contents(path: str) -> None
# Desc: Prints the contents of the given directory.
# Preconditions: path exists on the system
# Postconditions: None
# Returns: None
def print_directory_contents(path: str) -> None:
    if not does_path_exist(path):
        # print("Path does not exist: ", path) # debug, dont spam user with this
        return
    
    print("Checking directory: ", path)
    for file in os.listdir(path):
        print(" > ", file)


# Name: get_save(save_location: str) -> str
# Desc: Prompts the user to select a save file from the given directory.
# Preconditions: save_location exists on the system
# Postconditions: None
# Returns: The full path to the selected save file, or an empty string if the path does not exist
def get_save(save_location: str) -> str:
    if not does_path_exist(save_location):
        return ""
    
    print("Available saves in directory:", save_location)
    saves = os.listdir(save_location)
    for index, save in enumerate(saves):
        print(f"[{index}] {save}")
    
    chosen_index: int = -1
    while chosen_index < 0 or chosen_index >= len(saves):
        try:
            chosen_index = int(input(f"Select a save by index (0-{len(saves)-1}): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    chosen_save: str = saves[chosen_index]
    full_save_path: str = os.path.join(save_location, chosen_save)
    print("Chosen save path:", full_save_path)
    return full_save_path


# Name: check_save_directory(path: str) -> bool
# Desc: Checks if the given directory contains save files by verifying if it is not empty.
# Preconditions: path exists on the system
# Postconditions: None
# Returns: True if the directory contains files, False otherwise
def check_save_directory(path: str) -> bool:
    # check if directory exists
    if os.path.isdir(path) and os.listdir(path) != {}:
        return True
    else:
        return False


def decrypt_save_file(file_path):
    # mode is CBC
    pass


# ==[ CLASSES ]==
# Class: PlayerProgress
# Description: This class represents the progress of a single player, including
#              their name and the items they have completed.
class PlayerProgress:
    def __init__(self, player_name):
        self.m_player_name: str = player_name
        self.m_save_file_path: str = None
        self.m_decrypted_save_data = None # decoded save -> dict
        self.m_item_progress: Set[str] = set()

    def get_player_name(self):
        return self.m_player_name
    
    def get_item_progress(self):
        return self.m_item_progress
    
    def complete_item(self, item_name):
        self.m_item_progress.add(item_name)

    def is_item_completed(self, item_name):
        return item_name in self.m_item_progress


class Tracker:
    def __init__(self):
        self.m_player_progress: dict[str, PlayerProgress] = {}
        self.m_save_directory: str = None;

    def set_save_directory(self, save_directory: str):
        if does_path_exist(save_directory):
            self.m_save_directory = save_directory
            print("Save directory set to: ", save_directory)
        else:
            print("Invalid save directory: ", save_directory)

    def add_player(self, player_name):
        if player_name not in self.m_player_progress:
            self.m_player_progress[player_name] = PlayerProgress(player_name)
        else:
            print("Player already exists: ", player_name)

    def get_player_progress(self, player_name):
        return self.m_player_progress.get(player_name, None)

    def complete_item_for_player(self, player_name, item_name):
        player_progress = self.get_player_progress(player_name)
        if player_progress:
            player_progress.complete_item(item_name)

    def is_item_completed_for_player(self, player_name, item_name):
        player_progress = self.get_player_progress(player_name)
        if player_progress:
            return player_progress.is_item_completed(item_name)
        return False
    
    def list_players(self):
        return list(self.m_player_progress.keys())
    
    def list_completed_items_for_player(self, player_name):
        player_progress = self.get_player_progress(player_name)
        if player_progress:
            return player_progress.get_item_progress()
        return set()
    
