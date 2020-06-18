from funcs import dprint

def battle(player, npc):
    dprint("-" * 50)
    dprint("IT'S BATTLE TIME")
    dprint("-" * 50)

    player_pokemon = player.pokemon[0]
    npc_pokemon = npc.pokemon[0]
    for i, j in zip([player, npc], [player_pokemon, npc_pokemon]):
        dprint("{} sent out {}!".format(i.name, j.name))
    while player_pokemon.health > 0 and npc_pokemon.health > 0:
        if player_pokemon.get_stat("speed") >= npc_pokemon.get_stat("speed"):
            player_pokemon.attack(npc_pokemon)
            npc_pokemon.attack(player_pokemon)
        else:
            npc_pokemon.attack(player_pokemon)
            player_pokemon.attack(npc_pokemon)
    if player_pokemon.health <= 0:
        winner = npc
        dprint("{} fainted! {} won the battle!".format(player_pokemon.name, winner.name))
    else:
        winner = player
        dprint("{} fainted! {} won the battle!".format(npc_pokemon.name, winner.name))

    return winner
