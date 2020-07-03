from player import Player
from pokemon import Pokemon
import pickle

a = Player("Will")
a.add_pokemon(Pokemon("Sceptile", level = 100))
with open ("Storage/{}/player.pickle".format(a.name), "wb") as f:
    pickle.dump(a, f)

with open ("Storage/{}/player.pickle".format(a.name), "rb") as f:
    b = pickle.load(f)

b
