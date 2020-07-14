from main_loop import MainLoop
from person import Player
from pokemon import Pokemon
from location_loops import *

p = Player("Will")
player_poke = Pokemon("Weedle", name = "Pip", level = 6)
player_poke.level_up()
# stored_poke1 = Pokemon("Metagross", level = 72)
# stored_poke2 = Pokemon("Bulbasaur", name = "Paul", level = 14)
# stored_poke3 = Pokemon("Sentret", name = "Graham", level = 9)
# stored_poke4 = Pokemon("Tyranitar", name = "Steve", level = 100)
# stored_poke5 = Pokemon("Altaria", level = 45)
# stored_poke6 = Pokemon("Linoone", level = 35)
# stored_poke7 = Pokemon("Wingull", level = 20)
# stored_poke8 = Pokemon("Lapras", level = 39)
# stored_pokes = [
#     stored_poke1,
#     stored_poke2,
#     stored_poke3,
#     stored_poke4,
#     stored_poke5,
#     stored_poke6,
#     stored_poke7,
#     stored_poke8,
# ]
p.add_pokemon(player_poke)
# wild_poke = Pokemon("Rattata", level = 5)
# p.add_pokemon(stored_pokes, to = "storage")
# MainLoop(p)
