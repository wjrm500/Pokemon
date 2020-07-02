from pokemon_csv import base_stats, natures, exp_by_level, growth_patterns, types, type_effectiveness, exp_yield
from pokemon_stat_calc import StatCalculator
from funcs import dprint
import random
import pickle
import string
import numpy as np
from npc import NPC
from taketurn import TakeTurn

pickle_in = open("moves_by_level.pickle", "rb")
moves_by_level = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class Pokemon():
    ### TODO evolve function
    ### TODO level-up function
    ### TODO history subclass? Things like total pokemon defeated, total faints, total move usage, total damage inflicted and taken, pokemon defeated with type breakdown
    def __init__(self, species, name = None, level = 5):
        self.species = species
        if name is None:
            self.name = self.species
        else:
            self.name = name.capitalize()
        self.battle_name = "{} ({})".format(self.name, self.species) if self.name != self.species else self.species
        self.owner = "NA"
        self.level = level
        self.ivs = random_ivs = {stat: random.randint(1, 31) for stat in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]}
        self.nature = random_nature = random.choice(natures.index)
        self.gender = random_gender = random.choice(["Female", "Male"])
        self.base_stats = base_stats.loc[self.species].to_dict()
        self.base_exp_yield = exp_yield.loc[self.species][0]
        self.stats = StatCalculator(self.level, self.ivs, self.nature, self.base_stats)
        for key, value in self.stats.items():
            self.stats[key] = {"temp": int(value), "perm": int(value)}
        self.growth_pattern = growth_patterns.loc[self.species][0]
        self.exp = exp_by_level.loc[self.level, self.growth_pattern]
        self.exp_next_level = 0 if self.level == 100 else exp_by_level.loc[self.level + 1, self.growth_pattern]
        self.types = [x.capitalize() for x in list(types.loc[self.species]) if str(x) != "nan"]
        self.fainted = False
        self.fled = False
        self.guarantee_attacking_move()

    def non_hp_stat_refresh(self):
        for key, value in self.stats.items():
            if key != "hp":
                self.stats[key]["temp"] = self.stats[key]["perm"]

    def guarantee_attacking_move(self): # Generate a set of moves for the Pokemon
        df = moves_by_level[self.species] # Bring in moves learnt by level for particular species
        df = df[df["level"] <= self.level].copy() # Only look at moves possible at Pokemon's level
        def damage_dealing(move): # Function to create a filtered dataframe containing only damage-dealing moves
            if move_details[move]["power"] != "NA":
                return move
            else:
                pass
        damaging_df = df["move"].apply(damage_dealing) # Creating this dataframe
        best_damaging_move = df.iloc[damaging_df.last_valid_index()]["move"] # Picking out highest-level damage-dealing move to guarantee it is retained
        other_moves = df[df["move"] != best_damaging_move]["move"].tail(3) # Picking out up to three highest-level moves that are not the best damaging move, to pad moveset
        self.moves = {best_damaging_move: int(move_details[best_damaging_move]["pp"])} # Adding best damaging move to move dictionary, along with its PP
        self.moves.update({move: int(move_details[move]["pp"]) for move in list(other_moves)}) # Adding remaining moves to move dictionary, along with their PP
        for key, value in self.moves.items():
            self.moves[key] = {"temp": value, "perm": value}

    def get_stat(self, stat, type = "temp"):
        return self.stats[stat][type]

    def get_health(self):
        return self.stats["hp"]["temp"]

    def reduce_health(self, damage):
        self.stats["hp"]["temp"] -= damage

    def speak(self):
        dprint("I am a Pokemon")

    def display(self):
        dprint(self.name, " the ", self.species, " Lv. ", self.level)

    def faint(self):
        self.fainted = True
        dprint("{} fainted!".format(self.battle_name))

    def pp_reduce(self, move):
        self.moves[move]["temp"] -= 1

    def gain_exp(self, opposing_pokemon, participants):
        a = 1 if opposing_pokemon.owner == "NA" else 1.5
        b = opposing_pokemon.base_exp_yield
        l = opposing_pokemon.level
        s = participants
        exp_gain = int((a * b * l) / (7 * s))
        self.exp += exp_gain
        dprint("{} gained {:,} experience.".format(self.battle_name, exp_gain))
        while self.exp > self.exp_next_level and self.exp_next_level != 0:
            self.level_up()
        exp_needed = int(self.exp_next_level - self.exp)
        dprint("{} needs {:,} experience to reach Lv. {}.".format(self.battle_name, exp_needed, self.level + 1))
        return exp_gain

    def level_up(self):
        self.level += 1
        dprint("{} went from Lv. {} to Lv. {}!".format(self.battle_name, self.level - 1, self.level))
        self.exp_next_level = exp_by_level.loc[self.level + 1, self.growth_pattern]

    def take_turn(self, opponent, battle):
        mapped_choice = random.choice(list(self.moves.keys()))
        if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
            TakeTurn.deal_damage(self, opponent.active_pokemon, mapped_choice)
        else: # Pokemon move does not deal damage
            dprint("{} played a move that does not deal damage.".format(self.battle_name))
            pass
        self.pp_reduce(mapped_choice)

    def flee(self):
        self.fled = True
