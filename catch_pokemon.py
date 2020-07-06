from player import Player
from pokemon import Pokemon
from test import *

p = Player("Will")
player_poke = Pokemon("Milotic", level = 74)
player_poke_2 = Pokemon("Kangaskhan", level = 58)
p.add_pokemon(player_poke)
p.add_pokemon(player_poke_2)
p.inventory.add_item("Ultra Ball", quantity = 10)
p.inventory.add_item("Super Potion", quantity = 3)
wild_poke = Pokemon("Forretress", level = 69)
Battle_Wild_Pokemon(p, wild_poke)
