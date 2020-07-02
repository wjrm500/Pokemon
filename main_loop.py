from funcs import dprint
from location_loops import *
from save_game import save_game
from game import main_menu

class MainLoop():
    def __init__(self, player):
        self.locations = {
            "Grass": DoGrass,
            # "Gym": DoGym,
            # "Home": DoHome,
            "Pokemon Centre": DoPokemonCentre,
            # "PokeMart": DoPokeMart,
            # "Rival's House": DoRivalsHouse,
            # "Water": DoWater
            }
        while True:
            dprint("Where would you like to go?")
            available_locations = [location for location in self.locations.keys() if location != player.location]
            for index, available_location in enumerate(available_locations):
                dprint("({}) {}".format(index + 1, available_location))
            dprint("")
            dprint("Or you could...")
            ### TODO view Pokemon, view inventory
            dprint("")
            dprint("(A) Save game")
            dprint("(B) Exit game (with save)")
            dprint("(C) Exit game (without save)")
            choice = input()
            if choice.isnumeric():
                choice = int(choice)
                if choice in [1, 2, 3, 4, 5, 6]:
                    mapped_choice = available_locations[choice - 1]
                    dprint("You selected {}.".format(mapped_choice))
                    self.locations[mapped_choice](player)
                    player.location = mapped_choice
                else:
                    dprint("Valid input please.")
            elif choice.lower() == "a":
                save_game(player)
            elif choice.lower() == "b":
                save_game(player)
                dprint("{} exited to the main menu.".format(player.name))
                dprint("-" * 50)
                main_menu()
            elif choice.lower() == "c":
                dprint("{} exited to the main menu.".format(player.name))
                dprint("-" * 50)
                main_menu()
            else:
                dprint("Invalid input detected. Please try again.")
                input()
