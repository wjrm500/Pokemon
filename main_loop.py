from funcs import dprint
from location_loops import *
from save_game import *
from person import Player
import sys

class MainLoop():
    def __init__(self, player):
        self.action_options = {
            "1": {
                "display_text": "Go to grass",
                "function": DoGrass
            },
            "2": {
                "display_text": "Go to Pokemon Centre",
                "function": DoPokemonCentre
            },
            "3": {
                "display_text": "Go to PokeMart",
                "function": DoPokeMart
            },
            "4": {
                "display_text": "Go to Gym",
                "function": DoGym
            },
            "P": {
                "display_text": "View Pokemon in party",
                "function": Player.display_pokemon
            },
            "I": {
                "display_text": "View items in inventory",
                "function": Inventory.display_items
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
        while True:
            dprint("What would you like to do?")
            print("")
            dprint("Go somewhere")
            print("·" * 62)
            for key, value in self.action_options.items():
                if key.isnumeric():
                    print("({}) {}".format(key, value["display_text"]))
            print("")
            dprint("Do something")
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
                        input()
                    else:
                        mapped_choice["function"](player)
                    break
                except SystemExit:
                    sys.exit()
                except:
                    dprint("Invalid input detected. Please try again.")
                    break
