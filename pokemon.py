from pokemon_csv import base_stats, natures, exp_by_level, growth_patterns, moves, types, type_effectiveness
from pokemon_stat_calc import StatCalculator
from funcs import dprint
import random
import pickle
import string
import numpy as np
from player import Player
from npc import NPC
from attack import Attack

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

    def attack(self, opponent):
        if isinstance(self.owner, Player): # Pokemon is owned by controlled player
            choice, mapped_choice = Attack.display_options(self.owner)
            if choice.isnumeric(): # Player selected Pokemon move
                if move_details[mapped_choice]["power"] != "NA": # Pokemon move deals damage
                    Attack.deal_damage(self, opponent, mapped_choice)
                else: # Pokemon move does not deal damage
                    dprint("{} ({}) played a move that does not deal damage.".format(self.name, self.species))
                    pass
                    # TODO Consider non-attacking moves - need battle-specific stats that get reset. Where to store all moves?
            else: # Player did not select Pokemon move
                if choice == "d": # See detailed move information selected
                    Attack.see_move_details(self)
                elif choice == "b": # Rummage in bag selected
                    self.owner.display_inventory()
                elif choice == "s": # Switch Pokemon selected
                    self.owner.switch_pokemon()
                elif choice == "f": # Attempt to flee selected
                    if opponent.owner == "NA": # Opposing Pokemon is wild
                        if self.get_stat("speed") > opponent.get_stat("speed"): # Player Pokemon is faster than opposing Pokemon
                            dprint("{} ({}) fleed!".format(self.name, self.species))
                            #self.flee()
                        else: # Player Pokemon is slower than opposing Pokemon
                            A = self.get_stat("speed")
                            B = opponent.get_stat("speed")
                            C = self.battle_stats["flee_attempts"]
                            F = (((A * 128) / B) + 30 * C) % 256
                            randnum = random.randint(0, 255)
                            if randnum < F:
                                dprint("{} ({}) fleed!".format(self.name, self.species))
                                #self.flee()
                            else:
                                dprint("{} ({}) tried to flee, but was caught in the act!".format(self.name, self.species))
                                self.battle_stats["flee_attempts"] += 1
                    else: # Opposing Pokemon belongs to a trainer
                        dprint("You cannot flee from a trainer battle!")
        elif isinstance(self.owner, NPC): # Pokemon is owned my non-player character
            mapped_choice = random.choice(list(self.moves.keys()))
            if move_details[mapped_choice]["power"] != "NA":
                dprint("{} ({}) used {}!".format(self.name, self.species, mapped_choice))
                rand_miss = random.random()
                if rand_miss <= float(move_details[mapped_choice]["accuracy"]) / 100:
                    level = self.level
                    power = int(move_details[mapped_choice]["power"])
                    attack = self.get_stat("attack") if move_details[mapped_choice]["category"] == "Physical" else self.get_stat("sp_attack")
                    defense = opponent.get_stat("defense") if move_details[mapped_choice]["category"] == "Physical" else opponent.get_stat("sp_defense")
                    randnum = random.uniform(0.85, 1.00)
                    stab = 1.5 if move_details[mapped_choice]["move_type"] in self.types else 1
                    rand_crit = random.randint(0, 255)
                    critical_threshold = np.floor(self.base_stats["speed"] / 2)
                    critical = 2 if rand_crit < critical_threshold else 1
                    type_eff = np.prod([type_effectiveness.loc[move_details[mapped_choice]["move_type"]][type] for type in opponent.types])
                    damage = int(((((((2 * level) / 5) + 2) * power * attack / defense) / 50) + 2) * randnum * stab * critical * type_eff)
                    critical_text = "Critical hit! " if critical == 2 else ""
                    if type_eff <= 0.5:
                        effectiveness_text = " It wasn't very effective..."
                    elif type_eff >= 2:
                        effectiveness_text = " It was super effective!"
                    else:
                        effectiveness_text = ""
                    if damage > opponent.health:
                        damage = opponent.health
                    opponent.health -= damage
                    dprint("{}{} ({}) inflicted {} damage!{}".format(critical_text, self.name, self.species, int(damage), effectiveness_text))
                    dprint("{} ({}) has {}/{} HP remaining.".format(opponent.name, opponent.species, int(opponent.health), int(opponent.get_stat("hp"))))
                else:
                    dprint("{} missed!".format(self.species))
            else:
                print("Pokemon played non-attacking move")
                ### Move does not inflict damage
                pass
        elif self.owner == "NA": # Pokemon is not owned (wild)
            print("Wild Pokemon")
        # print(move_details[i]["effect"])
            # print("")
            # print("")

# a = Pokemon("Charizard", "Psycho", "Will", level = 50)
# d = Pokemon("Blastoise", "Runt", "Johnson", level = 100)
# a.attack(d)
# print(type(a.base_stats["speed"]))
