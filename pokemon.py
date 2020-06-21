from pokemon_csv import base_stats, natures, exp_by_level, growth_patterns, moves, types, type_effectiveness
from pokemon_stat_calc import StatCalculator
from funcs import dprint
import random
import pickle
import string
import numpy as np
from npc import NPC

pickle_in = open("moves_dict.pickle", "rb")
moves_dict = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class Pokemon():
    def __init__(self, species, name, owner, level = 5):
        self.species = species
        self.name = name.capitalize()
        self.owner = owner
        self.level = level
        self.ivs = random_ivs = {stat: random.randint(1, 31) for stat in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]}
        self.nature = random_nature = random.choice(natures.index)
        self.gender = random_gender = random.choice(["Female", "Male"])
        self.base_stats = base_stats.loc[self.species].to_dict()
        self.stats = StatCalculator(self.level, self.ivs, self.nature, self.base_stats)
        self.battle_stats = self.stats.copy().update({"flee_attempts": 0})
        self.health = self.get_stat("hp")
        self.growth_pattern = growth_patterns.loc[self.species][0]
        self.exp = exp_by_level.loc[self.level, self.growth_pattern]
        df = moves_dict[self.species]
        moves_list = list(df[df["level"] <= self.level]["move"].tail(4))
        self.moves = {move: move_details[move]["pp"] for move in moves_list} # TODO Ensure at least one attacking move is available
        self.types = [x.capitalize() for x in list(types.loc[self.species]) if str(x) != "nan"]

    def get_stat(self, stat):
        return self.stats[stat]

    def speak(self):
        dprint("I am a Pokemon")

    def display(self):
        dprint(self.name, " the ", self.species, " Lv. ", self.level)

class WildPokemon(Pokemon):
    def take_turn(self):
        pass
