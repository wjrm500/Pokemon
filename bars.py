import sys
import time
from pokemon_csv import exp_by_level

def health_bar(hp, health, change, type):
    sleep_time = 2.5 / hp
    start_health = health
    if type == "damage":
        damage = change
        while health >= start_health - damage:
            health_as_pct = health / hp
            blocks = int(60 * health_as_pct)
            display_health = " " + str(health) if health_as_pct < 0.95 else ""
            print("0|{:60}|{}".format((("■" * blocks) + display_health), hp), end = "\r")
            time.sleep(sleep_time)
            health -= 1
    elif type == "health_added":
        health_added = change
        while health <= start_health + health_added:
            health_as_pct = health / hp
            blocks = int(60 * health_as_pct)
            display_health = " " + str(health) if health_as_pct < 0.95 else ""
            print("0|{:60}|{}".format((("■" * blocks) + display_health), hp), end = "\r")
            time.sleep(sleep_time)
            health += 1
    print("\r")

def exp_bar(pokemon, exp_gain):
    sleep_time = 1.5 / exp_gain
    exp = int(pokemon.exp)
    pokemon_level = pokemon.level
    start_exp = exp
    while exp <= start_exp + exp_gain:
        base_exp_at_current_level = int(exp_by_level.loc[pokemon_level, pokemon.growth_pattern])
        base_exp_at_next_level = int(exp_by_level.loc[pokemon_level + 1, pokemon.growth_pattern])
        if exp >= base_exp_at_next_level and pokemon_level != 100:
            exp_as_pct = (exp - base_exp_at_current_level) / (base_exp_at_next_level - base_exp_at_current_level)
            blocks = int(60 * exp_as_pct)
            display_exp = " " + str(int(exp_as_pct * 100)) + "%" if exp_as_pct < 0.95 else ""
            print("Lv. {}|{:60}|Lv. {}".format(pokemon_level, (("■" * blocks) + display_exp), pokemon_level + 1))
            pokemon_level += 1
            base_exp_at_current_level = int(exp_by_level.loc[pokemon_level, pokemon.growth_pattern])
            base_exp_at_next_level = int(exp_by_level.loc[pokemon_level + 1, pokemon.growth_pattern])
        else:
            exp_as_pct = (exp - base_exp_at_current_level) / (base_exp_at_next_level - base_exp_at_current_level)
            blocks = int(60 * exp_as_pct)
            display_exp = " " + str(int(exp_as_pct * 100)) + "%" if exp_as_pct < 0.95 else ""
            print("Lv. {}|{:60}|Lv. {}".format(pokemon_level, (("■" * blocks) + display_exp), pokemon_level + 1), end = "\r")
        time.sleep(sleep_time)
        exp += 1

    print("\r")
