from funcs import dprint
import numpy as np
from pokemon import Pokemon
from npc import NPC
import pdb

class Battle():
    def __init__(self):
        self.participants = [] # For experience sharing
        self.battle_intro()

    def battle_intro(self):
        dprint("-" * 62)
        dprint("IT'S BATTLE TIME")
        dprint("-" * 62)

    def battle(self, player, opponent):
        if isinstance(opponent, NPC):
            npc = opponent
            def speed_check():
                global player_pokemon, npc_pokemon
                player_pokemon, npc_pokemon = player.active_pokemon, npc.active_pokemon
                global player_go_first
                player_go_first = True if player_pokemon.get_stat("speed") >= npc_pokemon.get_stat("speed") else False
            speed_check()
            self.participants.append(player_pokemon) # For experience sharing
            for i, j in zip([player, npc], [player_pokemon, npc_pokemon]):
                dprint("{} sent out {} ({} - Lv. {})!".format(i.name, j.name, j.species, j.level))
            speed_text = "{} has the speed advantage, which means {} will go first!"
            print(speed_text.format(player_pokemon.battle_name, player.name) if player_go_first else speed_text.format(npc_pokemon.battle_name, npc.name))
            def check_pokemon_fainted(x):
                if x.active_pokemon.get_health() == 0:
                    x.active_pokemon.faint()
                    if x == npc: # If fainted Pokemon belongs to NPC
                        for participant in self.participants:
                            participant.gain_exp(x.active_pokemon, len(self.participants))
                        self.participants = [self.participants[-1]] # For experience sharing - ensures only most recently appended participant remains as a participant
                    x.handle_faint(self)
            def all_pokemon_fainted():
                return np.sum([pokemon.get_health() for pokemon in player.party if not pokemon.fainted]) == 0 or np.sum([pokemon.get_health() for pokemon in npc.party if not pokemon.fainted]) == 0
            while not all_pokemon_fainted():
                speed_check()
                a, b = [player, npc] if player_go_first else [npc, player]
                input()
                a.take_turn(self, b)
                check_pokemon_fainted(b)
                if all_pokemon_fainted():
                    break
                input()
                b.take_turn(self, a)
                check_pokemon_fainted(a)
            for i in [player, npc]:
                i.reset_party_stats()
            winner = npc if np.sum([pokemon.get_health() for pokemon in player.party]) == 0 else player
            dprint("{} won the battle!".format(winner.name))
            return winner
        elif isinstance(opponent, Pokemon):
            def speed_check():
                global player_pokemon, wild_pokemon
                player_pokemon, wild_pokemon = player.active_pokemon, opponent
                global player_go_first
                player_go_first = True if player_pokemon.get_stat("speed") >= wild_pokemon.get_stat("speed") else False
            speed_check()
            self.participants.append(player_pokemon) # For experience sharing
            dprint("Wild {} (Lv. {}) appeared!".format(wild_pokemon.species, wild_pokemon.level))
            dprint("{} sent out {} (Lv. {})!".format(player.name, player_pokemon.battle_name, player_pokemon.level))
            speed_text = "{} has the speed advantage, which means {} will go first!"
            print(speed_text.format(player_pokemon.battle_name, player.name) if player_go_first else speed_text.format(wild_pokemon.battle_name, "it"))
            def check_pokemon_fled(x):
                if isinstance(x, Pokemon):
                    if x.fled == True:
                        return True
                    return False
                else:
                    if x.active_pokemon.fled == True:
                        return True
                    return False
            def all_pokemon_fainted():
                return np.sum([pokemon.get_health() for pokemon in player.party if not pokemon.fainted]) == 0 or wild_pokemon.get_health() == 0
            while not all_pokemon_fainted():
                speed_check()
                a, b = [player, wild_pokemon] if player_go_first else [wild_pokemon, player]
                input()
                a.take_turn(self, b)
                if check_pokemon_fled(a):
                    break
                if all_pokemon_fainted():
                    break
                input()
                b.take_turn(self, a)
                if check_pokemon_fled(b):
                    break
            if player.active_pokemon.fled:
                winner = None
            else:
                if np.sum([pokemon.get_health() for pokemon in player.party]) == 0:
                    winner = wild_pokemon
                else:
                    winner = player
                dprint("{} won the battle!".format(winner.name))
            input()
            dprint("-" * 62)
            player.reset_party_stats()
            return winner
