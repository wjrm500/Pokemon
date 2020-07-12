from funcs import dprint, inclusive_range, final_comma_ampersand
import random
import pickle
import numpy as np
from pokemon_csv import type_effectiveness, catch_rates
from bars import health_bar
import time
import pdb

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
            dprint("{}{} inflicted {} damage!{}".format(critical_text, attacking_pokemon.battle_name, int(damage), effectiveness_text))
            health_bar(defending_pokemon.get_stat("hp", type = "perm"), defending_pokemon.get_stat("hp", type = "temp"), damage, type = "damage")
            defending_pokemon.reduce_health(damage)
            dprint("{} has {}/{} HP remaining.".format(defending_pokemon.battle_name, defending_pokemon.get_health(), defending_pokemon.get_stat("hp", type = "perm")))
        else: # Move misses
            dprint("{} missed!".format(attacking_pokemon.species))

    def check_pokemon_fainted(battle, x):
        if x.get_health() == 0:
            x.faint()
            if x.owner != battle.player:
                for participant in battle.participants:
                    participant.gain_exp(x, len(battle.participants))
                battle.participants = [battle.participants[-1]]
            if x.owner != "NA":
                x.owner.handle_faint(battle)

    def see_move_details(attacking_pokemon):
        nums = list(range(1, 5))
        nums.reverse()
        max_move_len = len(max(attacking_pokemon.moves.keys(), key = len))
        for index, (move, pp) in enumerate(attacking_pokemon.moves.items()):
            print("({})".format(nums.pop()),
                move.ljust(max_move_len),
                "      Effect: ", move_details[move]["effect"])

    def attempt_to_flee(escapee, guard):
        if escapee.get_stat("speed") > guard.get_stat("speed"): # Player Pokemon is faster than opposing Pokemon
            dprint("{} fled!".format(escapee.battle_name))
            escapee.flee()
        else: # Player Pokemon is slower than opposing Pokemon
            A = escapee.get_stat("speed")
            B = guard.get_stat("speed")
            C = escapee.flee_attempts
            F = (((A * 128) / B) + 30 * C) % 256
            randnum = random.randint(0, 255)
            if randnum < F:
                dprint("{} fled!".format(escapee.battle_name))
                escapee.flee()
                return True
            else:
                dprint("{} tried to flee, but was caught in the act!".format(escapee.battle_name))
                escapee.flee_attempts += 1
                return False

    def throw_pokeball(player, wild_pokemon, ball_type = "Poke Ball"):
        def pokemon_caught(player, wild_pokemon):
            dprint("{} was caught!".format(wild_pokemon.species))
            while True:
                dprint("Name your {}:".format(wild_pokemon.species))
                name = input()
                if len(name) >= 2 and len(name) <= 15 and name.isalpha():
                    break
                else:
                    dprint("Please enter a valid name. Use only alphabetic characters and keep the length between 2 and 15 characters.")
            wild_pokemon.take_name(name)
            player.add_pokemon(wild_pokemon)
        dprint("{} threw a {} at {}!".format(player.name, ball_type, wild_pokemon.species))
        if ball_type == "Master Ball":
            dprint("The Master Ball shook once...".format(ball_type))
            pokemon_caught(player, wild_pokemon)
        else:
            hp_max = wild_pokemon.get_stat("hp", type = "perm")
            hp_current = wild_pokemon.get_stat("hp", type = "temp")
            catch_rate = catch_rates.loc[wild_pokemon.species]["catch_rate"]
            if ball_type == "Poke Ball":
                ball_bonus = 1
            elif ball_type == "Great Ball":
                ball_bonus = 1.5
            elif ball_type == "Ultra Ball":
                ball_bonus = 2
            ### Modified catch rate
            a = ((3 * hp_max - 2 * hp_current) * catch_rate * ball_bonus) / (3 * hp_max)
            ### Shake probability
            b = 1048560 / np.sqrt(np.sqrt(16711680 / a))
            ### Shake checks
            for i in ["once", "twice", "three times", "four times"]:
                dprint("The {} shook {}...".format(ball_type, i))
                time.sleep(0.5)
                rand_num = random.randint(0, 65_535)
                if rand_num >= b:
                    dprint("{} escaped!".format(wild_pokemon.species))
                    return False
            pokemon_caught(player, wild_pokemon)
            return True

    def drink_potion(player, potion_type = "Potion"):
        choice_mapping = {}
        max_name_len = max([np.sum([len(pokemon.name), len(pokemon.species)]) for pokemon in player.party if not pokemon.fainted]) + 4
        max_level_len = len(max([str(pokemon.level) for pokemon in player.party if not pokemon.fainted], key = len))
        max_types_len = max([np.sum([len(type) for type in pokemon.types]) for pokemon in player.party if not pokemon.fainted]) + 3
        dprint("Which Pokemon would you like to give the {} to?".format(potion_type))
        for index, pokemon in enumerate([pokemon for pokemon in player.party if not pokemon.fainted]):
            print("({})".format(index + 1),
                " {}".format(pokemon.battle_name).ljust(max_name_len),
                "      Level: ", str(pokemon.level).ljust(max_level_len),
                "      Type(s): ", final_comma_ampersand(pokemon.types).ljust(max_types_len),
                "      HP remaining: ", pokemon.get_health(), "/", pokemon.get_stat("hp", type = "perm"))
            choice_mapping[index + 1] = pokemon
        choice = int(input())
        chosen_pokemon = choice_mapping[choice]
        health_from_full = chosen_pokemon.stats["hp"]["perm"] - chosen_pokemon.stats["hp"]["temp"]
        potion_mapping = {
            "Potion": min(20, health_from_full),
            "Super Potion": min(50, health_from_full),
            "Hyper Potion": min(200, health_from_full),
            "Max Potion": health_from_full
        }
        health_added = potion_mapping[potion_type]
        dprint("{} gave {} a {}!".format(player.name, chosen_pokemon.battle_name, potion_type))
        health_bar(chosen_pokemon.get_stat("hp", type = "perm"), chosen_pokemon.get_stat("hp", type = "temp"), health_added, type = "health_added")
        chosen_pokemon.add_health(health_added)
        dprint("{}'s HP increased by {}!".format(chosen_pokemon.battle_name, health_added))
