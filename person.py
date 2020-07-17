from funcs import dprint, final_comma_ampersand
from taketurn import TakeTurn
import pickle
import numpy as np
from inventory import Inventory
import random
import pdb

pickle_in = open("moves_by_level.pickle", "rb")
moves_by_level = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class Person():
    def __init__(self, name):
        self.name = name.capitalize()
        self.location = None
        self.money = 100
        self.inventory = Inventory(self)
        self.party = []
        self.storage = []
        self.flee_attempts = 0

    def add_pokemon(self, pokemon, to = "party"):
        if not isinstance(pokemon, list):
            pokemon = [pokemon]
        for poke in pokemon:
            poke.owner = self
            if len(self.party) >= 6 or to == "storage":
                self.storage.append(poke)
                poke.fainted = False
                poke.stats["hp"]["temp"] = poke.stats["hp"]["perm"]
                dprint("{} was added to storage.".format(poke.battle_name))
            else:
                self.party.append(poke)
                self.active_pokemon = self.party[0]
                # dprint("{} was added to your party.".format(poke.battle_name))

    def release_pokemon(self, pokemon):
        self.party.remove(pokemon)
        self.active_pokemon = self.party[0]

    def set_gender(self, gender):
        self.gender = gender

    def display_pokemon(self):
        print("■" * 62)
        switch_text = "Press "
        for pokemon in self.party:
            pokemon.display()
            if self.party.index(pokemon) == 0:
                text_to_append = ""
            elif self.party.index(pokemon) == len(self.party) - 1:
                if len(self.party) == 2:
                    text_to_append = "{} to switch in {}.".format(self.party.index(pokemon), pokemon.battle_name)
                else:
                    text_to_append = "or {} to switch in {}.".format(self.party.index(pokemon), pokemon.battle_name)
            else:
                text_to_append = "{} to switch in {}, ".format(self.party.index(pokemon), pokemon.battle_name)
            switch_text += text_to_append
        if len(self.party) > 1:
            dprint(switch_text)
            user_input = input()
            if user_input.isnumeric():
                try:
                    user_input = int(user_input)
                    if not self.party[user_input].fainted:
                        self.party.insert(0, self.party.pop(user_input))
                        self.active_pokemon = self.party[0]
                        dprint("{} switched in {} (Lv. {})!".format(self.name, self.active_pokemon.battle_name, self.active_pokemon.level))
                    else: # Pokemon cannot be switched in as fainted
                        dprint("{} is unconscious, and therefore cannot be switched in!".format(self.party[user_input].battle_name))
                except:
                    dprint("Invalid input detected.")
            else:
                dprint("No switches made; {} remains active.".format(self.active_pokemon.battle_name))

    def reset_party_stats(self):
        for pokemon in self.party:
            pokemon.non_hp_stat_refresh()
        self.flee_attempts = 0

    def has_pokemon_available(self):
        if np.sum([pokemon.get_health() for pokemon in self.party]) > 0:
            return True
        return False

class Player(Person):
    def __init__(self, name):
        super().__init__(name)

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
                    dprint("{} switched in {} (Lv. {})!".format(self.name, self.active_pokemon.battle_name, self.active_pokemon.level))
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

    def handle_faint(self, battle):
        battle.participants.remove(self.active_pokemon)
        self.switch_pokemon(battle, type = "enforced")

class NPC(Person):
    def __init__(self, name, bounty = 25):
        super().__init__(name)
        self.bounty = bounty

    def speak(self, words):
        dprint("{}: \"{}\"".format(self.name, words))

    def switch_pokemon(self, battle, type = "voluntary"):
        if len([pokemon for pokemon in self.party[1:] if not pokemon.fainted]) > 0:
            # chosen_pokemon = random.choice([pokemon for pokemon in self.party[1:] if not pokemon.fainted])
            chosen_pokemon = [pokemon for pokemon in self.party[1:] if not pokemon.fainted][0]
            self.party.insert(0, self.party.pop(self.party.index(chosen_pokemon)))
            self.active_pokemon = self.party[0]
            dprint("{} switched in {} (Lv. {})!".format(self.name, self.active_pokemon.battle_name, self.active_pokemon.level))
            return "switched"
        else:
            if type == "voluntary":
                dprint("{} only has one Pokemon in their party!".format(self.name))
            elif type == "enforced":
                dprint("{} is all out of Pokemon!".format(self.name))
            return "unswitched"

    def take_turn(self, battle, opponent):
        mapped_choice = random.choice(list(self.active_pokemon.moves.keys()))
        if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
            TakeTurn.deal_damage(self.active_pokemon, opponent.active_pokemon, mapped_choice)
            TakeTurn.check_pokemon_fainted(battle, opponent.active_pokemon)
        else: # Pokemon move does not deal damage
            dprint("{} played a move that does not deal damage.".format(self.active_pokemon.battle_name))
            pass
        self.active_pokemon.pp_reduce(mapped_choice)

    def handle_faint(self, battle):
        self.switch_pokemon(battle, type = "enforced")
