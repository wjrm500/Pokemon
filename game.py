from player import Player
from pokemon import Pokemon
from npc import NPC
from funcs import dprint, final_comma_ampersand
from battle import battle
import random

dprint("""
You wake up bound, gagged and tied by the wrists to a steel bedframe in a dark, dingy room.

An old man totters in. He stops in front of you, licks his lips, and then sets to work carefully untying you.
""")
old_man = NPC("Old Man", "Home")
old_man.speak("Good day little one! What\'s your name then?")
while True:
    dprint("Input your name:")
    name = input()
    if len(name) >= 2 and len(name) <= 15 and name.isalpha():
        break
    else:
        old_man.speak("Being known only as \"Old Man\", I'm hardly an expert on the subject of names, but come up with a proper name would you?!")
p = Player(name)
old_man.speak("Ooh, {}, what a lovely name! I hope this doesn\'t seem rude, but please could you state your gender?".format(p.name))
dprint("Input your gender:")
gender = input()
p.set_gender(gender)
if p.gender.lower() in ("male", "m"):
    old_man.speak("And a strapping young male at that!")
elif p.gender.lower() in ("female", "f"):
    old_man.speak("And a beautiful young lady at that!")
else:
    old_man.speak("Ooh, one of those are you. Ah well, times change!")
dprint("The old man fumbles in his pocket for a few seconds, before drawing out three small orbs.")
pokemon_options = {"A": "Bulbasaur", "B": "Charmander", "C": "Squirtle"}
old_man.speak("Three wonderful Pokemon are imprisoned within these orbs: {}. Which one would you like?".format(final_comma_ampersand(pokemon_options)))
for alphabet, pokemon in pokemon_options.items():
    dprint(alphabet + " - " + pokemon)
while True:
    dprint("Input A, B or C.")
    starter_choice = input().upper()
    if starter_choice in pokemon_options.keys():
        break
    else:
        old_man.speak("That wasn't on the agenda! Try again...")
real_choice = pokemon_options.pop(starter_choice)
fake_choice = random.choice(list(pokemon_options.keys()))
old_man.speak("""You chose {}!
...
...
Just joking! You chose {}! Care to give the little bugger a name?""".format(pokemon_options[fake_choice], real_choice)
)
while True:
    dprint("Name your {}:".format(real_choice))
    starter_name = input()
    if len(starter_name) >= 2 and len(starter_name) <= 15 and starter_name.isalpha():
        break
    else:
        old_man.speak("Being known only as \"Old Man\", I'm hardly an expert on the subject of names, but come up with a proper name would you?!")
p.pokemon.append(Pokemon(species = real_choice, name = starter_name, owner = p))
dprint("{} pocketed the orb containing {} the {}.".format(p.name, p.pokemon[0].name, p.pokemon[0].species))
starter_pronoun = "He" if p.pokemon[0].gender == "Male" else "She"
old_man.speak("{} should serve you well. {}'s a {} little fellow!".format(p.pokemon[0].name, starter_pronoun, p.pokemon[0].nature.lower()))

### RIVAL ARRIVES

dprint("Suddenly, there is a loud thud and the door to the hallway collapses inwards, sending a cloud of dust into the air. When the dust clears, you see a large man clambering slowly to his feet.")
rival = NPC("Johnson", "Rival's Home")
rival_starter_mapping = {
"Bulbasaur": "Charmander",
"Charmander": "Squirtle",
"Squirtle": "Bulbasaur"
}
rival_starter = rival_starter_mapping[p.pokemon[0].species]
Pokemon(species = rival_starter, name = "Scunt", owner = rival)
rival.add_pokemon(Pokemon(species = rival_starter, name = "Scunt", owner = rival))
old_man.speak("Ah, I see {} has arrived!".format(rival.name))
dprint("You've never met this {} fellow, but there's something about him you don't like.".format(rival.name))
rival.speak("We meet at last {}. I've been waiting for this moment for quite some time. Are you ready to FIGHT?!".format(p.name))
dprint("Input \"Yes\" or \"No\":")
fight_choice = input()
if fight_choice.lower() in ["yes", "y"]:
    winner = battle(p, rival)
else:
    rival.speak("You great namby-pamby!")
    dprint("The old man shakes his head sadly and pulls the ropes that previously bound you to the bedframe from his pocket.")
    old_man.speak("{}, hold him still would you?".format(rival.name))
if p == winner:
    rival.speak("Hoisted on my own petard! Well won, {}. Until next time!".format(p.name))
elif rival == winner:
    rival.speak("Ha-ha! I won!")
