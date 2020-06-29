from funcs import dprint, inclusive_range
from numpy.random import choice
import random
from pokemon import Pokemon
from battle import Battle
from player import Player

class DoGrass():
    """ IDEAS
    Search for Pokemon
    Go deeper into the grass
    """
    def __init__(self, player):
        self.pokemon = {
            "Caterpie": {
                "rate": 0.25,
                "levels": inclusive_range(2, 3)
                },
            "Weedle": {
                "rate": 0.25,
                "levels": inclusive_range(2, 3)
                },
            "Pidgey": {
                "rate": 0.12,
                "levels": inclusive_range(2, 4)
                },
            "Rattata": {
                "rate": 0.13,
                "levels": inclusive_range(2, 4)
                },
            "Spearow": {
                "rate": 0.09,
                "levels": inclusive_range(2, 4)
                },
            "Ekans": {
                "rate": 0.04,
                "levels": inclusive_range(3, 4)
                },
            "Pikachu": {
                "rate": 0.02,
                "levels": inclusive_range(3, 5)
                },
            "Nidoran♀": {
                "rate": 0.05,
                "levels": inclusive_range(3, 4)
                },
            "Nidoran♂": {
                "rate": 0.05,
                "levels": inclusive_range(3, 4)
                }
            }
        self.welcome(player)
        global leave_grass
        leave_grass = False

    def welcome(self, player):
        dprint("You arrive on the grass.")
        self.loop(player)

    def loop(self, player):
        while True:
            self.display_options(player)
            if leave_grass == True:
                break

    def display_options(self, player):
        dprint("What would you like to do?")
        dprint("(1) Search for Pokemon")
        dprint("(2) Go somewhere else")
        while True:
            try:
                a = int(input())
                if a == 1:
                    dprint("You selected \"Search for Pokemon\"")
                    self.pokemon_search(player)
                    break
                elif a == 2:
                    dprint("You selected \"Go somewhere else\"")
                    global leave_grass
                    leave_grass = True
                    break
                else:
                    dprint("That number is not available. Please try again.")
            except:
                dprint("Invalid input detected. Please try again.")

    def pokemon_search(self, player):
        search_time = random.randint(1, 10)
        dprint("Hunting...")
        for i in range(search_time):
            dprint("...")
        dprint("Wild Pokemon found!")
        species_found = choice(
            list(self.pokemon.keys()), # Pokemon
            1, # Number to return
            p = [i["rate"] for i in self.pokemon.values()] # Weights
            )[0]
        level_found = random.choice(self.pokemon[species_found]["levels"])
        wild_pokemon = Pokemon(species = species_found, level = level_found)
        fight = Battle()
        winner = fight.battle(player, wild_pokemon)
        return winner


# p = Player("Will")
# p.add_pokemon(Pokemon("Bulbasaur"))
# DoGrass(p)

# def do_gym():
#     dprint("Welcome to the gym")
#     # Idea could be that you sequentially fight all the gym leaders before League
#     """
#     Bug Gym
#     Fire Gym
#     Grass Gym
#     Water Gym
#     Psychic Gym
#     Fighting Gym
#     Ice Gym
#     Rock Gym
#     Normal Gym
#     Steel Gym
#     Dragon Gym
#     Electric Gym
#     Flying Gym
#     Ground Gym
#     Pokemon League (Locked)
#     Do gyms in any order. For every two gyms you do, the difficulty of remaining gyms increases by one stage. Therefore you can choose any order and gyms will still get more difficult.
#     """
#
# def do_home():
#     dprint("Welcome home!")
#     """
#     Rest
#     Chat to Mother
#     """
#
# def do_pokemon_centre():
#     dprint("Welcome to the Pokemon Centre.")
#     """
#     Heal Pokemon
#     Use Computer
#     - Manage Pokemon
#     - View statistics
#     """
#
# def do_pokemart():
#     dprint("Welcome to the PokeMart.")
#     """
#     Approach vendor
#     Unlock Pokemon?
#     """
#
# def do_rivals_house():
#     dprint("Welcome to your rival's house")
#     """
#     Assault rival
#     Taunt rival
#     """
#
# def do_water():
#     dprint("Welcome to the water")
#     """
#     Fish (Pull out your rod)
#     Surf (Surf's up!)
#     Dive (Take the plunge)
#     """
