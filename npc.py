from funcs import dprint
import random
import pickle
import numpy as np
from pokemon_csv import type_effectiveness
from taketurn import TakeTurn

pickle_in = open("moves_dict.pickle", "rb")
moves_dict = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class NPC():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.party = []

    def add_pokemon(self, pokemon):
        self.party.append(pokemon)
        self.active_pokemon = self.party[0]

    def speak(self, text = "Bugger me, I've got nothing to say!"):
        dprint('{}: "{}"'.format(self.name, text))

    def take_turn(self, opponent):
        mapped_choice = random.choice(list(self.active_pokemon.moves.keys()))
        if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
            TakeTurn.deal_damage(self.active_pokemon, opponent.active_pokemon, mapped_choice)
        else: # Pokemon move does not deal damage
            dprint("{} ({}) played a move that does not deal damage.".format(self.active_pokemon.name, self.active_pokemon.species))
            pass
