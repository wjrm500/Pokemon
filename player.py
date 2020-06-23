from funcs import dprint, final_comma_ampersand
from taketurn import TakeTurn
import pickle
from pokemon import WildPokemon
import numpy as np
import pdb

pickle_in = open("moves_dict.pickle", "rb")
moves_dict = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class Player():
    def __init__(self, name):
        self.name = name.capitalize()
        self.location = "home"
        self.inventory = {"Pokeball": 1, "Potion": 1}
        self.party = []
        self.fainted_pokemon = []

    def add_pokemon(self, pokemon):
        self.party.append(pokemon)
        self.active_pokemon = self.party[0]

    def set_gender(self, gender):
        if gender.lower() in ("male", "m"):
            self.gender = "male"
        elif gender.lower() in ("female", "f"):
            self.gender = "female"
        else:
            self.gender = "unspecified"

    def move(self):
        new_location = input("Where would you like to go?")
        self.location = new_location

    def interact(self):
        self.location.interact(self)

    def display_pokemon(self):
        for pokemon in self.party:
            pokemon.display()

    def display_inventory(self):
        dprint("Your bag contains the following items...")
        for item, quantity in self.inventory.items():
            dprint("{} x {}".format(quantity, item))

    def switch_pokemon(self, type = "voluntary"):
        while True:
            try:
                if len([pokemon for pokemon in self.party[1:] if not pokemon.fainted]) > 0:
                    choice_mapping = {}
                    max_name_len = max([np.sum([len(pokemon.name), len(pokemon.species)]) for pokemon in self.party[1:] if not pokemon.fainted]) + 4
                    max_level_len = len(max([str(pokemon.level) for pokemon in self.party[1:] if not pokemon.fainted], key = len))
                    max_types_len = max([np.sum([len(type) for type in pokemon.types]) for pokemon in self.party[1:] if not pokemon.fainted]) + 3
                    print("Which of the following Pokemon would you like to switch in?")
                    for index, pokemon in enumerate([pokemon for pokemon in self.party[1:] if not pokemon.fainted]):
                        print("({})".format(index + 1),
                            " {} ({})".format(pokemon.name, pokemon.species).ljust(max_name_len),
                            "      Level: ", str(pokemon.level).ljust(max_level_len),
                            "      Type(s): ", final_comma_ampersand(pokemon.types).ljust(max_types_len),
                            "      HP remaining: ", int(pokemon.health), "/", int(pokemon.get_stat("hp")))
                        choice_mapping[index + 1] = pokemon
                    choice = int(input())
                    chosen_pokemon = choice_mapping[choice]
                    self.party.insert(0, self.party.pop(self.party.index(chosen_pokemon)))
                    self.active_pokemon = self.party[0]
                    dprint("{} switched in {}!".format(self.name, self.active_pokemon.name))
                    return "switched"
                else:
                    if type == "voluntary":
                        dprint("You only have one Pokemon in your party!")
                    elif type == "enforced":
                        dprint("You are all out of Pokemon!")
                    return "unswitched"
                break
            except:
                dprint("You must select one of the available options.")

    def handle_faint(self):
        self.active_pokemon.faint()
        self.switch_pokemon(type = "enforced")

    def take_turn(self, opponent):
        while True:
            while True:
                try:
                    choice, mapped_choice = TakeTurn.display_options(self)
                    break
                except:
                    dprint("You must select one of the available options.")
                    input()
            if choice.isnumeric(): # Player selected Pokemon move
                if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
                    TakeTurn.deal_damage(self.active_pokemon, opponent.active_pokemon, mapped_choice)
                else: # Pokemon move does not deal damage
                    dprint("{} ({}) played a move that does not deal damage.".format(self.active_pokemon.name, self.active_pokemon.species))
                    pass
                    # TODO Consider non-attacking moves - need battle-specific stats that get reset. Where to store all moves?
                break
            else: # Player did not select Pokemon move
                if choice == "d": # See detailed move information selected
                    TakeTurn.see_move_details(self.active_pokemon)
                    input()
                elif choice == "b": # Rummage in bag selected
                    self.display_inventory()
                    input()
                elif choice == "s": # Switch Pokemon selected
                    if self.switch_pokemon() == "switched":
                        break
                    input()
                elif choice == "f": # Attempt to flee selected
                    if isinstance(opponent, WildPokemon): # Opposing Pokemon is wild
                        TakeTurn.attempt_to_flee(self.active_pokemon, opponent, self.battle_stats["flee_attempts"])
                        break
                    else: # Opposing Pokemon belongs to a trainer
                        dprint("You cannot flee from a trainer battle!")
                        input()
