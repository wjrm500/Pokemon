from funcs import dprint
import random
import pickle
import numpy as np
from pokemon_csv import type_effectiveness
from taketurn import TakeTurn

pickle_in = open("moves_by_level.pickle", "rb")
moves_by_level = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class NPC():
    def __init__(self, name):
        self.name = name
        self.party = []

    def add_pokemon(self, pokemon):
        pokemon.owner = self
        self.party.append(pokemon)
        self.active_pokemon = self.party[0]

    def speak(self, text = "Bugger me, I've got nothing to say!"):
        dprint('{}: "{}"'.format(self.name, text))

    def take_turn(self, opponent, battle):
        mapped_choice = random.choice(list(self.active_pokemon.moves.keys()))
        if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
            TakeTurn.deal_damage(self.active_pokemon, opponent.active_pokemon, mapped_choice)
        else: # Pokemon move does not deal damage
            dprint("{} played a move that does not deal damage.".format(self.active_pokemon.battle_name))
            pass
        self.active_pokemon.pp_reduce(mapped_choice)

    def handle_faint(self, battle):
        if len([pokemon for pokemon in self.party[1:] if not pokemon.fainted]) > 0:
            self.active_pokemon = [pokemon for pokemon in self.party if not pokemon.fainted][0]
            dprint("{} switched in {}!".format(self.name, self.active_pokemon.battle_name))
        else:
            pass

    def reset_party_stats(self):
        for pokemon in self.party:
            pokemon.non_hp_stat_refresh()
