from funcs import dprint, inclusive_range
from numpy.random import choice
import random
from pokemon import Pokemon
from battle import Battle
from player import Player
import pdb
from save_game import *

class DoLocation():
    def __init__(self, player):
        player.location = self.location
        self.leave = False
        self.initiate_generic_functions()
        self.action_options = {
            "V": {
                "display_text": "View Pokemon in party",
                "function": Player.display_pokemon
            },
            "L": {
                "display_text": "Go somewhere else",
                "function": leave
            },
            "S": {
                "display_text": "Save game",
                "function": save_game
            },
            "E": {
                "display_text": "Exit game (with save)",
                "function": save_game_and_exit_to_main_menu
            },
            "X": {
                "display_text": "Exit game (without save)",
                "function": exit_to_main_menu
            }
        }
        self.add_action_options()
        self.welcome()
        self.loop(player)

    def add_action_options(self):
        self.action_options.update(self.unique_actions)

    def welcome(self):
        dprint("You have arrived at your destination.")

    def loop(self, player):
        while True:
            self.display_options(player)
            if self.leave == True:
                break

    def display_options(self, player):
        while True:
            dprint("What would you like to do?")
            dprint("Location-specific options")
            print("·" * 62)
            for key, value in self.action_options.items():
                if key.isnumeric():
                    dprint("({}) {}".format(key, value["display_text"]))
            print("")
            dprint("Generic options")
            print("·" * 62)
            for key, value in self.action_options.items():
                if not key.isnumeric():
                    dprint("({}) {}".format(key, value["display_text"]))
            print("")
            choice = input().upper()
            try:
                mapped_choice = self.action_options[choice]
            except:
                dprint("Invalid input detected. Please try again.")
            display_text = mapped_choice["display_text"]
            dprint("You selected \"{}\".".format(display_text))
            mapped_choice["function"](player)
            break

    def initiate_generic_functions(self):
        global leave
        def leave(player):
            self.leave = True

class DoGrass(DoLocation):
    """ IDEAS
    Search for Pokemon
    Go deeper into the grass
    """
    pokemon = {
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
    def __init__(self, player):
        self.location = "Grass"
        self.initiate_unique_functions()
        self.unique_actions = {
            "1": {
                "display_text": "Search for Pokemon",
                "function": pokemon_search
            }
        }
        DoLocation.__init__(self, player)

    def initiate_unique_functions(self):
        global pokemon_search
        def pokemon_search(player):
            search_time = random.randint(1, 10)
            dprint("Hunting...")
            for i in range(search_time):
                dprint("...")
            dprint("Wild Pokemon found!")
            species_found = choice(
                list(DoGrass.pokemon.keys()), # Pokemon
                1, # Number to return
                p = [i["rate"] for i in DoGrass.pokemon.values()] # Weights
                )[0]
            level_found = random.choice(DoGrass.pokemon[species_found]["levels"])
            wild_pokemon = Pokemon(species = species_found, level = level_found)
            fight = Battle()
            winner = fight.battle(player, wild_pokemon)
            return winner

class DoPokemonCentre(DoLocation):
    """ IDEAS
    Heal Pokemon
    Use Computer
    - Manage Pokemon
    - View statistics
    """
    def __init__(self, player):
        self.location = "Pokemon Centre"
        self.initiate_unique_functions()
        self.unique_actions = {
            "1": {
                "display_text": "Heal Pokemon",
                "function": heal_pokemon
            }
        }
        DoLocation.__init__(self, player)

    def initiate_unique_functions(self):
        global heal_pokemon
        def heal_pokemon(player):
            for pokemon in player.party:
                pokemon.stats["hp"]["temp"] = pokemon.stats["hp"]["perm"]
                dprint("All Pokemon healed to full health!")
                input()

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
#     IV revealer?
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
