from pokemon_csv import base_stats, natures, exp_by_level, growth_patterns
from pokemon_stat_calc import StatCalculator
from funcs import dprint
import random
import pickle

pickle_in = open("moves_dict.pickle", "rb")
moves_dict = pickle.load(pickle_in)

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
        self.health = self.get_stat("hp")
        self.growth_pattern = growth_patterns.loc[self.species][0]
        self.exp = exp_by_level.loc[self.level, self.growth_pattern]
        df = moves_dict[self.species]
        self.moves = list(df[df["level"] <= self.level]["move"].tail(4))

    def get_stat(self, stat):
        return self.stats[stat]

    def speak(self):
        dprint("I am a Pokemon")

    def display(self):
        dprint(self.name, " the ", self.species, " Lv. ", self.level)

    # def attack(self, opponent):
    #     dprint("{} attacked {}!".format(self.name, opponent.name))
    #     damage = random.randint(1, 10)
    #     if damage > opponent.health:
    #         damage = opponent.health
    #     opponent.health -= damage
    #     dprint("{} inflicted {} damage! {} has {}/{} HP remaining!".format(self.name, int(damage), opponent.name, int(opponent.health), int(opponent.get_stat("hp"))))
    #     print("")


a = Pokemon("Bulbasaur", "Graham", "Will", level = 25)
print(a.moves)
