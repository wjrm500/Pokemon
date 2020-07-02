from funcs import dprint, remove_dirs_not_containing_pickle
import pickle
import os
import sys

# from player import Player
# from pokemon import Pokemon
#
# p = Player("Will")
# poke1 = Pokemon("Blastoise", "Brian", p, level = 45)
# poke2 = Pokemon("Golduck", "Shimmer", p, level = 31)
# poke3 = Pokemon("Ninetales", "Topaz", p, level = 35)
# poke4 = Pokemon("Graveler", "Rocky", p, level = 22)
# poke5 = Pokemon("Lapras", "Aloha", p, level = 34)
# poke6 = Pokemon("Venomoth", "Peregrin", p, level = 38)
# for poke in [poke1, poke2, poke3, poke4, poke5, poke6]:
#     p.add_pokemon(poke)

# Removes games that have been created but never saved
storage_directory = os.getcwd() + "/Storage/"
remove_dirs_not_containing_pickle(storage_directory)

def new_game():
    while True:
        dprint("Choose a player name:")
        name = input().capitalize()
        if len(name) >= 2 and len(name) <= 15 and name.isalpha():
            dirname = os.getcwd() + "\\Storage\\"
            path = os.path.join(dirname, name)
            if not os.path.exists(path):
                os.mkdir(path)
                path = os.path.join(path, "Party")
                os.mkdir(path)
                dprint("Created new directory for {}.".format(name))
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
            dprint("({}) {}".format(index + 1, option))
        choice = int(input())
        mapped_choice = options[choice - 1]
        dprint("You selected {}.".format(mapped_choice))
        with open("Storage/{}/player.pickle".format(mapped_choice), "rb") as f:
            player = pickle.load(f)
        mypath = os.getcwd() + "\\Storage\\" + mapped_choice + "\\Party\\"
        party_pokemon = [f.name for f in os.scandir(mypath)]
        for pokemon in party_pokemon:
            with open("Storage/{}/Party/{}".format(mapped_choice, pokemon), "rb") as f:
                loaded_pokemon = pickle.load(f)
            player.add_pokemon(loaded_pokemon)
        dprint("Loading game...")
        from main_loop import MainLoop
        MainLoop(player)
    else:
        dprint("No saved games to load.")

def quit_game():
    sys.exit()

def main_menu():
    while True:
        dprint("Welcome to my homemade text-based Pokemon game!")
        dprint("What would you like to do?")
        dprint("(N) Start new game")
        dprint("(L) Load existing game")
        dprint("(Q) Quit game")
        choice = input()
        if choice.lower() == "n":
            new_game()
        elif choice.lower() == "l":
            load_game()
        elif choice.lower() == "q":
            quit_game()
        else:
            "Valid input please."
