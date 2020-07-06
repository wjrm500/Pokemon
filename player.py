from funcs import dprint, final_comma_ampersand
from taketurn import TakeTurn
import pickle
from pokemon import Pokemon
import numpy as np
import pdb
from npc import NPC
from inventory import Inventory

pickle_in = open("moves_by_level.pickle", "rb")
moves_by_level = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class Player():
    def __init__(self, name):
        self.name = name.capitalize()
        self.location = "Home"
        self.inventory = Inventory(self)
        self.party = []
        self.flee_attempts = 0

    def add_pokemon(self, pokemon):
        pokemon.owner = self
        self.party.append(pokemon)
        self.active_pokemon = self.party[0]

    def release_pokemon(self, pokemon):
        self.party.remove(pokemon)
        self.active_pokemon = self.party[0]

    def set_gender(self, gender):
        self.gender = gender

    def move(self):
        new_location = input("Where would you like to go?")
        self.location = new_location

    def interact(self):
        self.location.interact(self)

    def display_pokemon(self):
        print("■" * 62)
        for pokemon in self.party:
            pokemon.display()

    def switch_pokemon(self, battle, type = "voluntary"):
        while True:
            try:
                if len([pokemon for pokemon in self.party[1:] if not pokemon.fainted]) > 0:
                    choice_mapping = {}
                    max_name_len = max([np.sum([len(pokemon.name), len(pokemon.species)]) for pokemon in self.party[1:] if not pokemon.fainted]) + 4
                    max_level_len = len(max([str(pokemon.level) for pokemon in self.party[1:] if not pokemon.fainted], key = len))
                    max_types_len = max([np.sum([len(type) for type in pokemon.types]) for pokemon in self.party[1:] if not pokemon.fainted]) + 3
                    dprint("Which of the following Pokemon would you like to switch in?")
                    for index, pokemon in enumerate([pokemon for pokemon in self.party[1:] if not pokemon.fainted]):
                        print("({})".format(index + 1),
                            " {}".format(pokemon.battle_name).ljust(max_name_len),
                            "      Level: ", str(pokemon.level).ljust(max_level_len),
                            "      Type(s): ", final_comma_ampersand(pokemon.types).ljust(max_types_len),
                            "      HP remaining: ", pokemon.get_health(), "/", pokemon.get_stat("hp", type = "perm"))
                        choice_mapping[index + 1] = pokemon
                    choice = int(input())
                    chosen_pokemon = choice_mapping[choice]
                    self.party.insert(0, self.party.pop(self.party.index(chosen_pokemon)))
                    self.active_pokemon = self.party[0]
                    if self.active_pokemon not in battle.participants:
                        battle.participants.append(self.active_pokemon)
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

    def handle_faint(self, battle):
        battle.participants.remove(self.active_pokemon)
        self.switch_pokemon(battle, type = "enforced")

    def take_turn(self, battle, opponent):
        if isinstance(opponent, NPC):
            opponent = opponent.active_pokemon
        while True:
            while True:
                try:
                    choice, mapped_choice = TakeTurn.display_options(self)
                    break
                except:
                    dprint("You must select one of the available options.")
                    input()
            if choice.isnumeric(): # Player selected Pokemon move
                if np.sum([move["temp"] for move in self.active_pokemon.moves.values()]) == 0: # All moves have zero PP
                    dprint("All of {}'s moves are out of PP!".format(self.active_pokemon.species))
                else: # At least one move has PP remaining
                    if self.active_pokemon.moves[mapped_choice]["temp"] == 0: # Chosen move has zero PP
                        dprint("{} has no PP remaining! Choose another move.".format(mapped_choice))
                    else: # Chosen move has PP remaining
                        if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
                            TakeTurn.deal_damage(self.active_pokemon, opponent, mapped_choice)
                            TakeTurn.check_pokemon_fainted(battle, opponent)
                        else: # Pokemon move does not deal damage
                            dprint("{} played a move that does not deal damage.".format(self.active_pokemon.battle_name))
                            # TODO Consider non-attacking moves - need battle-specific stats that get reset. Where to store all moves?
                        self.active_pokemon.pp_reduce(mapped_choice)
                        break
            else: # Player did not select Pokemon move
                if choice == "d": # See detailed move information selected
                    TakeTurn.see_move_details(self.active_pokemon)
                    input()
                elif choice == "b": # Rummage in bag selected
                    value = self.inventory.display_items(opponent)
                    if value == "pokemon_caught":
                        battle.wild_pokemon_caught = True
                        break
                    elif value == "pokeball_missed" or value == "potion_drunk":
                        break
                    input()
                elif choice == "s": # Switch Pokemon selected
                    if self.switch_pokemon(battle) == "switched":
                        break
                    input()
                elif choice == "f": # Attempt to flee selected
                    if opponent.owner == "NA": # Opposing Pokemon is wild
                        flee_successful = TakeTurn.attempt_to_flee(self.active_pokemon, opponent)
                        if flee_successful:
                            battle.player_fled =  True
                        break
                    else: # Opposing Pokemon belongs to a trainer
                        dprint("You cannot flee from a trainer battle!")
                        input()

    def reset_party_stats(self):
        for pokemon in self.party:
            pokemon.non_hp_stat_refresh()
        self.flee_attempts = 0

    def has_pokemon_available(self):
        if np.sum([pokemon.get_health() for pokemon in self.party]) > 0:
            return True
        return False
