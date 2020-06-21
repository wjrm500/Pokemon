from funcs import dprint

def battle(player, npc):
    dprint("-" * 50)
    dprint("IT'S BATTLE TIME")
    dprint("-" * 50)

    player_pokemon = player.pokemon[0]
    npc_pokemon = npc.pokemon[0]
    for i, j in zip([player, npc], [player_pokemon, npc_pokemon]):
        dprint("{} sent out {}!".format(i.name, j.name))
    speed_text = "{} ({}) has the speed advantage and will strike first!"
    print(speed_text.format(player_pokemon.name, player_pokemon.species) if player_pokemon.get_stat("speed") >= npc_pokemon.get_stat("speed") else speed_text.format(npc_pokemon.name, npc_pokemon.species))
    while player_pokemon.health > 0 and npc_pokemon.health > 0:
        if player_pokemon.get_stat("speed") >= npc_pokemon.get_stat("speed"):
            input()
            player_pokemon.attack(npc_pokemon)
            if npc_pokemon.health == 0:
                break
            input()
            npc_pokemon.attack(player_pokemon)
        else:
            input()
            npc_pokemon.attack(player_pokemon)
            if player_pokemon.health == 0:
                break
            input()
            player_pokemon.attack(npc_pokemon)
    if player_pokemon.health <= 0:
        winner = npc
        dprint("{} fainted! {} won the battle!".format(player_pokemon.name, winner.name))
    else:
        winner = player
        dprint("{} fainted! {} won the battle!".format(npc_pokemon.name, winner.name))

    return winners
