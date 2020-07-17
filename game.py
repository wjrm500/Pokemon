from funcs import dprint, verbosity_setup, dprint_setup
import pickle
import os
import pdb
import shutil
import sys

def main_menu():
    while True:
        dprint("Welcome to my homemade text-based Pokemon game!")
        dprint("What would you like to do?")
        print("(N) Start new game")
        print("(L) Load existing game")
        print("(D) Delete existing game")
        print("(S) Settings")
        print("(Q) Quit game")
        choice = input()
        if choice.lower() == "n":
            new_game()
        elif choice.lower() == "l":
            load_game()
        elif choice.lower() == "d":
            delete_game()
        elif choice.lower() ==  "s":
            settings()
        elif choice.lower() == "q":
            quit_game()
        else:
            "Invalid input detected."

def new_game():
    while True:
        dprint("Choose a player name:")
        name = input().capitalize()
        if len(name) >= 2 and len(name) <= 15 and name.isalpha():
            dirname = os.getcwd() + "\\Storage\\"
            path = os.path.join(dirname, name)
            if not os.path.exists(path):
                dprint("The name \"{}\" is available!".format(name))
                break
            else:
                dprint("The name {} is already taken. Please choose another.".format(name))
        else:
            dprint("Please enter a valid name. Use only alphabetic characters and keep the length between 2 and 15 characters.")
    dprint("Starting new game...")
    from story import beginning
    beginning(name)

def load_game(): ### TODO Add total played time next to each load option
    global player
    mypath = os.getcwd() + "\\Storage\\"
    options = [f.name for f in os.scandir(mypath) if f.is_dir()]
    if len(options) > 0:
        dprint("Which game would you like to load?")
        for index, option in enumerate(options):
            print("({}) {}".format(index + 1, option))
        print("")
        dprint("(X) Exit to main menu")
        while True:
            choice = input()
            if choice.isnumeric():
                try:
                    choice = int(choice)
                    mapped_choice = options[choice - 1]
                except:
                    dprint("Invalid input detected.")
                dprint("You selected {}.".format(mapped_choice))
                with open("Storage/{}/player.pickle".format(mapped_choice), "rb") as f:
                    player = pickle.load(f)
                dprint("Loading game...")
                from main_loop import MainLoop
                MainLoop(player)
            else:
                if choice.lower() == "x":
                    main_menu()
                else:
                    dprint("Invalid input detected.")
    else:
        dprint("No saved games to load.")
        input()

def delete_game():
    global player
    mypath = os.getcwd() + "\\Storage\\"
    options = [f.name for f in os.scandir(mypath) if f.is_dir()]
    if len(options) > 0:
        while True:
            dprint("Which game would you like to delete?")
            for index, option in enumerate(options):
                print("({}) {}".format(index + 1, option))
            print("")
            dprint("(X) Exit to main menu")
            choice = input()
            if choice.isnumeric():
                try:
                    choice = int(choice)
                    mapped_choice = options[choice - 1]
                except:
                    dprint("Invalid input detected.")
                while True:
                    dprint("Are you sure you want to delete {}?".format(mapped_choice))
                    dprint("Input \"Yes\" or \"No\":")
                    delete_confirm = input()
                    if delete_confirm.lower() == "y":
                        shutil.rmtree("Storage/{}/".format(mapped_choice))
                        dprint("{} was deleted! They had a good innings.".format(mapped_choice))
                        input()
                        main_menu()
                    elif delete_confirm.lower() == "n":
                        dprint("Lucky escape for {}!".format(mapped_choice))
                        input()
                        break
                    else:
                        dprint("Invalid input detected.")
            else:
                if choice.lower() == "x":
                    main_menu()
                else:
                    dprint("Invalid input detected.")
                    break
    else:
        dprint("No saved games to delete.")
        input()

def settings():
    dprint("Which setting would you like to change?")
    settings = {
        "1": {
            "Verbosity": verbosity_setup
            },
        "2": {
            "Text speed": dprint_setup
        }
    }
    for outer_key, dict in settings.items():
        for inner_key in dict.keys():
            print("({}) {}".format(outer_key, inner_key))
    while True:
        user_input = input()
        try:
            selection = list(settings[user_input].keys())[0]
            dprint("You selected {}.".format(selection))
            settings[user_input][selection]()
        except:
            dprint("Invalid input detected.")
        input()
        break

def quit_game():
    sys.exit()
