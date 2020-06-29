from funcs import dprint
import pickle
import os

def save_game(player):
    dprint("{} saved the game.".format(player.name))
    # Pickle player
    with open("Storage/{}/player.pickle".format(player.name), "wb") as f:
        pickle.dump(player, f)

    ### Remove existing party Pokemon from directory
    mypath = os.getcwd() + "\\Storage\\" + player.name + "\\Party\\"
    for file in os.scandir(mypath):
        os.remove(os.path.join(mypath, file))

    # Pickle party Pokemon
    for pokemon in player.party:
        with open("Storage/{}/Party/{}.pickle".format(player.name, pokemon.name), "wb") as f:
            pickle.dump(pokemon, f)
