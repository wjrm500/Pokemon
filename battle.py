from funcs import dprint
import numpy as np

class Battle():
    def __init__(self):
        self.battle_intro()

    def battle_intro(self):
        dprint("-" * 50)
        dprint("IT'S BATTLE TIME")
        dprint("-" * 50)

    def battle(player, npc):
        def speed_check():
            global player_pokemon, npc_pokemon
            player_pokemon, npc_pokemon = player.active_pokemon, npc.active_pokemon
            global player_go_first
            player_go_first = True if player_pokemon.get_stat("speed") >= npc_pokemon.get_stat("speed") else False
        speed_check()
        for i, j in zip([player, npc], [player_pokemon, npc_pokemon]):
            dprint("{} sent out {}!".format(i.name, j.name))
        speed_text = "{} ({}) has the speed advantage, which means {} will go first!"
        print(speed_text.format(player_pokemon.name, player_pokemon.species, player.name) if player_go_first else speed_text.format(npc_pokemon.name, npc_pokemon.species, npc.name))
        def all_pokemon_fainted():
            return np.sum([pokemon.health for pokemon in player.party]) == 0 or np.sum([pokemon.health for pokemon in npc.party]) == 0
        while not all_pokemon_fainted():
            speed_check()
            a, b = [player, npc] if player_go_first else [npc, player]
            input()
            a.take_turn(b)
            if all_pokemon_fainted():
                break
            input()
            b.take_turn(a)
        winner = npc if np.sum([pokemon.health for pokemon in player.party]) == 0 else player
        dprint("{} won the battle!".format(winner.name))
        return winner
