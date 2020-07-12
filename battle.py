from funcs import dprint
import numpy as np
import pdb
import os
from location_loops import *

class Battle():
    def __init__(self, player):
        self.player = player
        self.participants = [player.active_pokemon]
        if self.player.has_pokemon_available():
            self.intro()
            self.battle_start()
            self.battle_loop()
            self.battle_end()
        else:
            dprint("You have no conscious Pokemon!")

    def intro(self):
        dprint("-" * 62)
        dprint("IT'S BATTLE TIME")
        dprint("-" * 62)

    def battle_loop(self):
        while True:
            fastest, slowest = self.speed_check()
            fastest.take_turn(battle = self, opponent = slowest)
            input()
            if self.check_over():
                break
            slowest.take_turn(battle = self, opponent = fastest)
            input()
            if self.check_over():
                break

class Battle_Trainer(Battle):
    def __init__(self, player, trainer):
        self.trainer = trainer
        Battle.__init__(self, player)

    def speed_check(self):
        if self.player.active_pokemon.get_stat("speed") > self.trainer.active_pokemon.get_stat("speed"):
            return (self.player, self.trainer)
        else:
            return (self.trainer, self.player)

    def check_over(self):
        if np.sum([pokemon.get_health() for pokemon in self.player.party]) == 0 or np.sum([pokemon.get_health() for pokemon in self.trainer.party]) == 0:
            return True
        return False

    def battle_start(self):
        for competitor in (self.player, self.trainer):
            dprint("{} sent out {} (Lv. {})!".format(competitor.name, competitor.active_pokemon.battle_name, competitor.active_pokemon.level))
        fastest = self.speed_check()[0]
        placeholder_text = "{} has the speed advantage, which means {} will go first!"
        dprint(placeholder_text.format(self.player.active_pokemon.battle_name, self.player.name) if fastest == self.player else placeholder_text.format(self.trainer.active_pokemon.battle_name, self.trainer.name))
        input()

    def battle_end(self):
        self.player.reset_party_stats()
        for pokemon in self.trainer.party:
            pokemon.fainted = False
            pokemon.stats["hp"]["temp"] = pokemon.stats["hp"]["perm"]
            for move in pokemon.moves.keys():
                pokemon.moves[move]["temp"] = pokemon.moves[move]["perm"]
        if np.sum([pokemon.get_health() for pokemon in self.player.party]) == 0:
            self.winner = self.trainer
        else:
            self.winner = self.player
        dprint("{} won the battle!".format(self.winner.name))
        if self.winner == self.player:
            self.player.money += self.trainer.bounty
            dprint("{} pocketed £{}.".format(self.player.name, self.trainer.bounty))
        dprint("-" * 62)
        input()
        return self.winner

class Battle_Wild_Pokemon(Battle):
    def __init__(self, player, wild_pokemon):
        self.wild_pokemon = wild_pokemon
        self.player_fled = False
        self.wild_pokemon_fled = False
        self.wild_pokemon_caught = False
        Battle.__init__(self, player)

    def speed_check(self):
        if self.player.active_pokemon.get_stat("speed") > self.wild_pokemon.get_stat("speed"):
            return (self.player, self.wild_pokemon)
        else:
            return (self.wild_pokemon, self.player)

    def check_over(self):
        if np.sum([pokemon.get_health() for pokemon in self.player.party]) == 0 or self.wild_pokemon.get_health() == 0 or self.player_fled or self.wild_pokemon_caught:
            return True
        return False

    def battle_start(self):
        dprint("Wild {} (Lv. {}) appeared!".format(self.wild_pokemon.species, self.wild_pokemon.level))
        dprint("{} sent out {} (Lv. {})!".format(self.player.name, self.player.active_pokemon.battle_name, self.player.active_pokemon.level))
        fastest = self.speed_check()[0]
        placeholder_text = "{} has the speed advantage, which means {} will go first!"
        dprint(placeholder_text.format(self.player.active_pokemon.battle_name, self.player.name) if fastest == self.player else placeholder_text.format(self.wild_pokemon.battle_name, "it"))
        input()

    def battle_end(self):
        self.player.reset_party_stats()
        if self.player_fled or self.wild_pokemon_fled or self.wild_pokemon_caught:
            self.winner = None
        else:
            if np.sum([pokemon.get_health() for pokemon in self.player.party]) == 0:
                self.winner = self.wild_pokemon
            else:
                self.winner = self.player
            dprint("{} won the battle!".format(self.winner.name))
        dprint("-" * 62)
        return self.winner
