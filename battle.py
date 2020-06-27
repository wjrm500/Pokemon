from funcs import dprint
import numpy as np

class Battle():
    def __init__(self):
        self.participants = [] # For experience sharing
        self.battle_intro()

    def battle_intro(self):
        dprint("-" * 50)
        dprint("IT'S BATTLE TIME")
        dprint("-" * 50)

    def battle(self, player, npc):
        def speed_check():
            global player_pokemon, npc_pokemon
            player_pokemon, npc_pokemon = player.active_pokemon, npc.active_pokemon
            global player_go_first
            player_go_first = True if player_pokemon.get_stat("speed") >= npc_pokemon.get_stat("speed") else False
        speed_check()
        self.participants.append(player_pokemon) # For experience sharing
        for i, j in zip([player, npc], [player_pokemon, npc_pokemon]):
            dprint("{} sent out {} ({} - Lv. {})!".format(i.name, j.name, j.species, j.level))
        speed_text = "{} ({}) has the speed advantage, which means {} will go first!"
        print(speed_text.format(player_pokemon.name, player_pokemon.species, player.name) if player_go_first else speed_text.format(npc_pokemon.name, npc_pokemon.species, npc.name))
        def check_pokemon_fainted(x):
            if x.active_pokemon.get_health() == 0:
                x.active_pokemon.faint()
                if x == npc: # If fainted Pokemon belongs to NPC
                    for participant in self.participants:
                        exp_gain = participant.gain_exp(x.active_pokemon, len(self.participants))
                        dprint("{} ({}) gained {} experience.".format(participant.name, participant.species, exp_gain))
                    self.participants = [self.participants[-1]] # For experience sharing - ensures only most recently appended participant remains as a participant
                x.handle_faint(self)
        def all_pokemon_fainted():
            return np.sum([pokemon.get_health() for pokemon in player.party if not pokemon.fainted]) == 0 or np.sum([pokemon.get_health() for pokemon in npc.party if not pokemon.fainted]) == 0
        while not all_pokemon_fainted():
            speed_check()
            a, b = [player, npc] if player_go_first else [npc, player]
            input()
            a.take_turn(b, self)
            check_pokemon_fainted(b)
            if all_pokemon_fainted():
                break
            input()
            b.take_turn(a, self)
            check_pokemon_fainted(a)
        for i in [player, npc]:
            i.refresh_party_stats()
        winner = npc if np.sum([pokemon.get_health() for pokemon in player.party]) == 0 else player
        dprint("{} won the battle!".format(winner.name))
        return winner
