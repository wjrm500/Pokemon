from funcs import dprint
import random
import pickle
import numpy as np
from pokemon_csv import type_effectiveness

pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()

class TakeTurn():
    def display_options(attacking_player):
        attacking_pokemon = attacking_player.active_pokemon
        dprint("Your Lv. {} {} has the following {} moves...".format(attacking_pokemon.level, attacking_pokemon.species, len(attacking_pokemon.moves)))
        print("")
        nums = list(range(1, 5))
        nums.reverse()
        max_move_len = len(max(attacking_pokemon.moves.keys(), key = len))
        max_type_len = len(max([move_details[move]["move_type"] for move in attacking_pokemon.moves.keys()], key = len))
        max_category_len = len(max([move_details[move]["category"] for move in attacking_pokemon.moves.keys()], key = len))
        max_power_len = len(max([move_details[move]["power"] for move in attacking_pokemon.moves.keys()], key = len))
        max_accuracy_len = len(max([move_details[move]["accuracy"] for move in attacking_pokemon.moves.keys()], key = len))
        choice_mapping = {}
        for index, (move, pp) in enumerate(attacking_pokemon.moves.items()):
            print("({})".format(nums.pop()),
                move.ljust(max_move_len),
                "      Type: ", move_details[move]["move_type"].ljust(max_type_len),
                "      Category: ", move_details[move]["category"].ljust(max_category_len),
                "      Power: ", move_details[move]["power"].ljust(max_power_len),
                "      Accuracy: ", move_details[move]["accuracy"].ljust(max_accuracy_len),
                "      PP left: ", attacking_pokemon.moves[move]["temp"], "/", attacking_pokemon.moves[move]["perm"])
            choice_mapping[str(index + 1)] = list(attacking_pokemon.moves.keys())[index]
        print("")
        dprint("Alternatively you could...")
        print("")
        dprint(["(D)",
            "See detailed move information"])
        dprint(["(B)",
            "Rummage in bag"])
        dprint(["(S)",
            "Switch Pokemon"])
        dprint(["(F)",
            "Attempt to flee"])
        print("")
        choice_mapping.update({
        "d": "See detailed move information",
        "b": "Rummage in bag",
        "s": "Switch Pokemon",
        "f": "Attempt to flee"
        })
        dprint("What would you like to do?")
        choice = input().lower()
        mapped_choice = choice_mapping[choice]
        dprint("You selected {}.".format(mapped_choice))
        return [choice, mapped_choice]

    def deal_damage(attacking_pokemon, defending_pokemon, chosen_move):
        dprint("{} used {}!".format(attacking_pokemon.battle_name, chosen_move))
        rand_miss = random.random()
        if rand_miss <= float(move_details[chosen_move]["accuracy"]) / 100: # Move hits
            level = attacking_pokemon.level
            power = int(move_details[chosen_move]["power"])
            attack = attacking_pokemon.get_stat("attack") if move_details[chosen_move]["category"] == "Physical" else attacking_pokemon.get_stat("sp_attack")
            defense = defending_pokemon.get_stat("defense") if move_details[chosen_move]["category"] == "Physical" else defending_pokemon.get_stat("sp_defense")
            randnum = random.uniform(0.85, 1.00)
            stab = 1.5 if move_details[chosen_move]["move_type"] in attacking_pokemon.types else 1
            rand_crit = random.randint(0, 255)
            critical_threshold = np.floor(attacking_pokemon.base_stats["speed"] / 2)
            critical = 2 if rand_crit < critical_threshold else 1
            type_eff = np.prod([type_effectiveness.loc[move_details[chosen_move]["move_type"]][type] for type in defending_pokemon.types])
            damage = int(((((((2 * level) / 5) + 2) * power * attack / defense) / 50) + 2) * randnum * stab * critical * type_eff)
            critical_text = "Critical hit! " if critical == 2 else ""
            if type_eff <= 0.5:
                effectiveness_text = " It wasn't very effective..."
            elif type_eff >= 2:
                effectiveness_text = " It was super effective!"
            else:
                effectiveness_text = ""
            if damage > defending_pokemon.get_health():
                damage = defending_pokemon.get_health()
            defending_pokemon.reduce_health(damage)
            dprint("{}{} inflicted {} damage!{}".format(critical_text, attacking_pokemon.battle_name, int(damage), effectiveness_text))
            dprint("{} has {}/{} HP remaining.".format(defending_pokemon.battle_name, defending_pokemon.get_health(), defending_pokemon.get_stat("hp", type = "perm")))
        else: # Move misses
            dprint("{} missed!".format(attacking_pokemon.species))

    def see_move_details(attacking_pokemon):
        nums = list(range(1, 5))
        nums.reverse()
        max_move_len = len(max(attacking_pokemon.moves.keys(), key = len))
        for index, (move, pp) in enumerate(attacking_pokemon.moves.items()):
            print("({})".format(nums.pop()),
                move.ljust(max_move_len),
                "      Effect: ", move_details[move]["effect"])

    def attempt_to_flee(escapee, guard, flee_attempts):
        if escapee.get_stat("speed") > guard.get_stat("speed"): # Player Pokemon is faster than opposing Pokemon
            dprint("{} fled!".format(escapee.battle_name))
            #self.flee()
        else: # Player Pokemon is slower than opposing Pokemon
            A = escapee.get_stat("speed")
            B = guard.get_stat("speed")
            C = flee_attempts
            F = (((A * 128) / B) + 30 * C) % 256
            randnum = random.randint(0, 255)
            if randnum < F:
                dprint("{} fled!".format(escapee.battle_name))
                self.flee()
            else:
                dprint("{} tried to flee, but was caught in the act!".format(escapee.battle_name))
                self.flee_attempts += 1
