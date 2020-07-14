from funcs import dprint
import pickle
import os
from game import main_menu
import pdb

def save_game(player):
    # TODO: Allow multiple save files per user. Group Pickles by date in individual directories
    player.location = None
    dirname = os.getcwd() + "\\Storage\\"
    path = os.path.join(dirname, player.name)
    if not os.path.exists(path):
        os.mkdir(path)
        dprint("Created new save file for {}.".format(player.name))
    with open("Storage/{}/player.pickle".format(player.name), "wb") as f:
        pickle.dump(player, f)
    dprint("{} saved the game.".format(player.name))

def exit_to_main_menu(player):
    dprint("{} exited to the main menu.".format(player.name))
    dprint("-" * 50)
    main_menu()

def save_game_and_exit_to_main_menu(player):
    save_game(player)
    input()
    exit_to_main_menu(player)
