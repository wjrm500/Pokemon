from funcs import dprint, inclusive_range, options_from_dict
from numpy.random import choice
import random
from pokemon import Pokemon
from battle import *
from person import *
import pdb
from save_game import *
import sys

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
        dprint("What would you like to do?")
        print("")
        dprint("Location-specific options")
        print("·" * 62)
        for key, value in self.action_options.items():
            if key.isnumeric():
                print("({}) {}".format(key, value["display_text"]))
        print("")
        dprint("Generic options")
        print("·" * 62)
        for key, value in self.action_options.items():
            if not key.isnumeric():
                print("({}) {}".format(key, value["display_text"]))
        print("")
        while True:
            choice = input().upper()
            try:
                mapped_choice = self.action_options[choice]
                display_text = mapped_choice["display_text"]
                dprint("You selected \"{}\".".format(display_text))
                if display_text == "View items in inventory":
                    mapped_choice["function"](player.inventory)
                else:
                    mapped_choice["function"](player)
                input()
                break
            except SystemExit:
                sys.exit()
            except:
                dprint("Invalid input detected. Please try again.")
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
                for move in pokemon.moves.keys():
                    pokemon.moves[move]["temp"] = pokemon.moves[move]["perm"]
            dprint("All Pokemon healed to full health!")
            dprint("All Pokemon had their PP restored!")
        def use_computer(player):
            self.computer = NPC("Computer")
            self.computer.speak("How may I be of service?")
            dprint("(1) Withdraw Pokemon")
            dprint("(2) Deposit Pokemon")
            print("")
            dprint("(X) Exit computer")
            while True:
                user_input = input()
                try:
                    if user_input == "1":
                        ### If withdraw Pokemon selected
                        if len(player.party) < 6 and len(player.storage) > 0:
                            choice_mapping = {}
                            max_name_len = max([len(pokemon.battle_name) for pokemon in player.storage]) + 5
                            max_level_len = max([len(str(pokemon.level)) for pokemon in player.storage]) + 5
                            max_types_len = max([len(final_comma_ampersand(pokemon.types)) for pokemon in player.storage])
                            dprint("Which of the following Pokemon would you like to add to your party?")
                            for index, pokemon in enumerate(player.storage):
                                print(
                                    "({})".format(index + 1),
                                    "{}".format(pokemon.battle_name).ljust(max_name_len),
                                    " Level: ", str(pokemon.level).ljust(max_level_len),
                                    " Type(s): ", final_comma_ampersand(pokemon.types).ljust(max_types_len)
                                    )
                                choice_mapping[index + 1] = pokemon
                            print("")
                            print("(X) Exit computer")
                            while True:
                                user_input = input()
                                if user_input.upper() == "X":
                                    self.computer.speak("Bye!")
                                    break
                                elif user_input.isnumeric():
                                    try:
                                        user_input = int(user_input)
                                        chosen_pokemon = choice_mapping[user_input]
                                        player.storage.pop(player.storage.index(chosen_pokemon))
                                        player.add_pokemon(chosen_pokemon)
                                        dprint("{} moved {} out of storage and into their party.".format(player.name, chosen_pokemon.battle_name))
                                        break
                                    except:
                                        self.computer.speak("Stupid human! Input a valid keypress.")
                                else:
                                    self.computer.speak("Stupid human! Input a valid keypress.")
                        else:
                            if len(player.party) >= 6 and len(player.storage) == 0:
                                self.computer.speak("Your party is at full capacity, and you have no Pokemon in storage to withdraw.")
                            elif len(player.party) >= 6:
                                self.computer.speak("Your party is at full capacity.")
                            elif len(player.storage) == 0:
                                self.computer.speak("You have no Pokemon in storage to withdraw.")
                        break
                    elif user_input == "2":
                        if len(player.party) > 1:
                            choice_mapping = {}
                            max_name_len = max([len(pokemon.battle_name) for pokemon in player.party]) + 5
                            max_level_len = max([len(str(pokemon.level)) for pokemon in player.party]) + 5
                            max_types_len = max([len(final_comma_ampersand(pokemon.types)) for pokemon in player.party])
                            dprint("Which of the following Pokemon would you like to deposit in storage?")
                            for index, pokemon in enumerate(player.party):
                                print(
                                    "({})".format(index + 1),
                                    "{}".format(pokemon.battle_name).ljust(max_name_len),
                                    " Level: ", str(pokemon.level).ljust(max_level_len),
                                    " Type(s): ", final_comma_ampersand(pokemon.types).ljust(max_types_len)
                                    )
                                choice_mapping[index + 1] = pokemon
                            print("")
                            print("(X) Exit computer")
                            while True:
                                user_input = input()
                                if user_input.upper() == "X":
                                    self.computer.speak("Bye!")
                                    break
                                elif user_input.isnumeric():
                                    try:
                                        user_input = int(user_input)
                                        chosen_pokemon = choice_mapping[user_input]
                                        player.party.pop(player.party.index(chosen_pokemon))
                                        player.storage.append(chosen_pokemon)
                                        player.active_pokemon = player.party[0]
                                        dprint("{} moved {} out of their party and into storage.".format(player.name, chosen_pokemon.battle_name))
                                        break
                                    except:
                                        self.computer.speak("Stupid human! Input a valid keypress.")
                                else:
                                    self.computer.speak("Stupid human! Input a valid keypress.")
                        else:
                            self.computer.speak("You need at least two Pokemon in your party to make a deposit.")
                        break
                    elif user_input.upper() == "X":
                        self.computer.speak("Bye!")
                        break
                    else:
                        self.computer.speak("Stupid human! Input a valid keypress.")
                except:
                    self.computer.speak("Stupid human! Input a valid keypress.")

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
                    break
                except:
                    if user_input.upper() == "X":
                        self.vendor.speak("I'll get back to my nap then.")
                        break
                    self.vendor.speak("I beg pardon?")

class DoGym(DoLocation):
    def __init__(self, player):
        self.location = "Gym"
        self.initiate_unique_functions()
        self.unique_actions = {
            "1": {
                "display_text": "Bug Gym",
                "function": bug_gym
            }
        }
        DoLocation.__init__(self, player)

    def initiate_trainer(trainer_name, pokemon):
        trainer = NPC(trainer_name)
        for poke in pokemon:
            poke_name = poke[0]
            poke_level = random.randint(poke[1][0], poke[1][1])
            poke_object = Pokemon(poke_name, level = poke_level)
            trainer.add_pokemon(poke_object)

        trainer.party.sort(key = lambda x: x.total_stat)
        total_stats = np.sum([pokemon.total_stat for pokemon in trainer.party])
        divisor = 15 # random.randint(15, 20)
        bounty = int(total_stats / divisor)
        trainer.bounty = bounty
        return trainer

    def initiate_unique_functions(self):
        global bug_gym
        def bug_gym(player):
            viola = DoGym.initiate_trainer("Viola",
                [["Caterpie", [4, 5]], ["Paras", [6, 9]], ["Surskit", [5, 8]]])
            gnathan = DoGym.initiate_trainer("Gnathan",
                [["Nincada", [8, 12]], ["Weedle", [6, 8]], ["Wurmple", [5, 6]]])
            crick = DoGym.initiate_trainer("Crick",
                [["Ledyba", [8, 10]], ["Pineco", [9, 13]], ["Spinarak", [11, 14]]])
            wiggy = DoGym.initiate_trainer("Wiggy",
                [["Anorith", [10, 14]], ["Venonat", [12, 15]], ["Illumise", [13, 14]]])
            entabi = DoGym.initiate_trainer("Entabi",
                [["Dustox", [16, 20]], ["Masquerain", [22, 24]], ["Volbeat", [15, 16]], ["Yanma", [14, 19]]])
            calico = DoGym.initiate_trainer("Calico",
                [["Butterfree", [18, 22]], ["Parasect", [24, 25]], ["Scyther", [23, 28]], ["Shuckle", [19, 23]]])
            sessid = DoGym.initiate_trainer("Sessid",
                [["Heracross", [22, 27]], ["Ledian", [18, 24]], ["Pinsir", [25, 31]], ["Scizor", [30, 36]], ["Venomoth", [31, 33]]])
            carabus = DoGym.initiate_trainer("Carabus",
                [["Ariados", [27, 33]], ["Armaldo", [40, 42]], ["Beautifly", [25, 32]], ["Beedrill", [25, 32]], ["Forretress", [34, 38]], ["Ninjask", [30, 35]]])
            trainer_dict = {}
            i = 0
            for var, trainer_obj in list(locals().items()):
                if var not in ["player", "trainer_dict", "i"]:
                    i += 1
                    inner_key = "{:12} (Difficulty: {})".format(trainer_obj.name, trainer_obj.bounty)
                    inner_value = "Battle_Trainer(player, {})".format(var)
                    trainer_dict.update({str(i): {inner_key: inner_value}})
            dprint("Which trainer would you like to battle?")
            eval(options_from_dict(trainer_dict))






# p = Player("Will")
# p.add_pokemon(Pokemon("Bulbasaur"))
# DoGrass(p)

# def do_gym():
#     dprint("Welcome to the gym")
#     # Idea could be that you sequentially fight all the gym leaders before League
#     """
#     One gym
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
