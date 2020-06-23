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
        self.types = [x.capitalize() for x in list(types.loc[self.species]) if str(x) != "nan"]
        self.fainted = False
        self.guarantee_attacking_move()

    def guarantee_attacking_move(self):
        df = moves_dict[self.species]
        df = df[df["level"] <= self.level].copy()
        def damage_dealing(move):
            if move_details[move]["power"] != "NA":
                return 1
            else:
                return 0
        df["damage_dealing"] = df["move"].apply(damage_dealing)
        damaging_df = df[df["damage_dealing"] == 1]
        best_damaging_move = df.iloc[damaging_df.last_valid_index()]["move"]
        other_moves = df[df["move"] != best_damaging_move]["move"].tail(3)
        self.moves = {best_damaging_move: move_details[best_damaging_move]["pp"]}
        self.moves.update({move: move_details[move]["pp"] for move in list(other_moves)})

    def get_stat(self, stat):
        return self.stats[stat]

    def speak(self):
        dprint("I am a Pokemon")

    def display(self):
        dprint(self.name, " the ", self.species, " Lv. ", self.level)

    def faint(self):
        self.fainted = True
        dprint("{} ({}) fainted!".format(self.name, self.species))

class WildPokemon(Pokemon):
    def take_turn(self):
        pass

a = Pokemon("Blastoise", name = "Graham", owner = "Will", level = 50)
b = Pokemon("Vileplume", name = "Jim", owner = "Will", level = 57)
