from funcs import dprint, inclusive_range
from numpy.random import choice
import random
from pokemon import Pokemon
from battle import *
from person import *
import pdb
from save_game import *

class DoLocation():
    def __init__(self, player):
        player.location = self.location
        self.leave = False
        self.initiate_generic_functions()
        self.action_options = {
            "P": {
                "display_text": "View Pokemon in party",
                "function": Player.display_pokemon
            },
            "I": {
                "display_text": "View items in inventory",
                "function": Inventory.display_items
            },
            "L": {
                "display_text": "Return to main loop",
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
            print("")
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
                break
            display_text = mapped_choice["display_text"]
            dprint("You selected \"{}\".".format(display_text))
            if display_text == "View items in inventory":
                mapped_choice["function"](player.inventory)
            else:
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
            "rate": 0.28,
            "levels": inclusive_range(2, 3)
            },
        "Weedle": {
            "rate": 0.28,
            "levels": inclusive_range(2, 3)
            },
        "Pidgey": {
            "rate": 0.14,
            "levels": inclusive_range(2, 4)
            },
        "Rattata": {
            "rate": 0.15,
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
        # "Nidoran♀": {
        #     "rate": 0.05,
        #     "levels": inclusive_range(3, 4)
        #     },
        # "Nidoran♂": {
        #     "rate": 0.05,
        #     "levels": inclusive_range(3, 4)
        #     }
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
            Battle_Wild_Pokemon(player, wild_pokemon)

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
            },
            "2": {
                "display_text": "Use computer",
                "function": use_computer
            }
        }
        DoLocation.__init__(self, player)

    def initiate_unique_functions(self):
        global heal_pokemon
        global use_computer
        def heal_pokemon(player):
            for pokemon in player.party:
                pokemon.fainted = False
                pokemon.stats["hp"]["temp"] = pokemon.stats["hp"]["perm"]
                dprint("All Pokemon healed to full health!")
                for move in pokemon.moves.keys():
                    pokemon.moves[move]["temp"] = pokemon.moves[move]["perm"]
                dprint("All Pokemon had their PP restored!")
                input()
        def use_computer(player):
            self.computer = NPC("Computer")
            ### If withdraw Pokemon selected
            if len(player.party) < 6:
                choice_mapping = {}
                max_name_len = max([len(pokemon.battle_name) for pokemon in player.storage]) + 5
                max_level_len = max([len(str(pokemon.level)) for pokemon in player.storage]) + 5
                max_types_len = max([len(final_comma_ampersand(pokemon.types)) for pokemon in player.storage])
                dprint("Which of the following Pokemon would you like to add to your party?")
                for index, pokemon in enumerate(player.storage):
                    print(
                        "({})".format(index + 1),
                        " {}".format(pokemon.battle_name).ljust(max_name_len),
                        " Level: ", str(pokemon.level).ljust(max_level_len),
                        " Type(s): ", final_comma_ampersand(pokemon.types).ljust(max_types_len)
                        )
                    choice_mapping[index + 1] = pokemon
                choice = int(input())
                chosen_pokemon = choice_mapping[choice]
                player.storage.pop(player.storage.index(chosen_pokemon))
                player.add_pokemon(chosen_pokemon)
                dprint("{} moved {} out of storage and into their party.".format(player.name, chosen_pokemon.battle_name))
            else:
                self.computer.speak("No.")
            input()



class DoPokeMart(DoLocation):
    items = {
        "Poke Ball": 10,
        "Great Ball": 30,
        "Ultra Ball": 60,
        "Master Ball": 750,
        "Potion": 10,
        "Super Potion": 20,
        "Hyper Potion": 50,
        "Max Potion": 80
    }
    def __init__(self, player):
        self.location = "Pokemon Centre"
        self.initiate_unique_functions()
        self.unique_actions = {
            "1": {
                "display_text": "Buy items",
                "function": buy_items
            }
        }
        DoLocation.__init__(self, player)

    def initiate_unique_functions(self):
        global buy_items
        self.vendor = NPC("Vendor")
        def buy_items(player):
            dprint("You have £{} to spend.".format(player.money))
            self.vendor.speak("What would like to buy today?")
            for i, (item, price) in enumerate(DoPokeMart.items.items()):
                print("({}) {:13} £{}".format(i + 1, item, price))
            print("(X) Nothing")
            while True:
                try:
                    user_input = int(input())
                    chosen_item = list(DoPokeMart.items.keys())[user_input - 1]
                    self.vendor.speak("And how many {}s would you like?".format(chosen_item))
                    while True:
                        try:
                            chosen_quantity = int(input())
                            if chosen_quantity == 0:
                                self.vendor.speak("Time waster!")
                            else:
                                total_price = DoPokeMart.items[chosen_item] * chosen_quantity
                                if total_price > player.money:
                                    self.vendor.speak("I'm afraid you don't have enough money for that.")
                                else:
                                    self.vendor.speak("{} {}s? That'll be £{} please.".format(chosen_quantity, chosen_item, total_price))
                                    dprint("You hand over £{} and stash the {}s in your inventory.".format(total_price, chosen_item))
                                    player.money -= total_price
                                    dprint("You have £{} remaining.".format(player.money))
                                    player.inventory.add_item(chosen_item, chosen_quantity)
                            break
                        except:
                            self.vendor.speak("I beg pardon?")
                    input()
                    break
                except:
                    if user_input.upper() == "X":
                        self.vendor.speak("I'll get back to my nap then.")
                        break
                    self.vendor.speak("I beg pardon?")








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
