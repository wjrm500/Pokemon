from person import Player, NPC
from pokemon import Pokemon
from funcs import dprint, final_comma_ampersand
from battle import Battle_Trainer
import random
import sys
from main_loop import MainLoop

verbose = True

def beginning(player_name):
    p = Player(player_name)
    old_man = NPC("Old Man")
    if verbose == True:
        dprint("You wake up bound, gagged and tied by the wrists to a steel bedframe in a dark, dingy room.")
        dprint("An old man totters in. He stops in front of you, licks his lips, and then sets to work carefully untying you.")
        old_man.speak("Good day {}! I hope this doesn't seem rude, but please could you state your gender?".format(p.name))
    while True:
        try:
            dprint("Input your gender:")
            gender = input()
            if gender.lower()[0] == "m":
                p.set_gender("male")
                if verbose == True:
                    dprint("The old man frowns slightly at your response, and examines you with a squint.")
                    old_man.speak("Male eh? Hmm... Well then, if you say so!")
                else:
                    print("You selected {}.".format(p.gender))
                break
            elif gender.lower()[0] == "f":
                p.set_gender("female")
                if verbose == True:
                    dprint("The old man frowns slightly at your response, and examines you with a squint.")
                    old_man.speak("Female eh? Hmm... Well then, if you say so!")
                else:
                    print("You selected {}.".format(p.gender))
                break
            elif len(gender) > 0:
                if verbose == True:
                    old_man.speak("Your gender is {}? Are you sure?".format(gender))
                    dprint("Input \"Yes\" or \"No\":")
                else:
                    print("Are you sure?")
                answer = input()
                if answer.lower()[0] == "y":
                    p.set_gender("unspecified")
                    if verbose == True:
                        old_man.speak("Ah well, times change!")
                    else:
                        print("You selected {}.".format(p.gender))
                    break
                elif answer.lower()[0] == "n":
                    if verbose == True:
                        old_man.speak("Well what in God's name are you then?")
                else:
                    if verbose == True:
                        old_man.speak("Stop muttering gobbledigook would you?")
                    else:
                        print("Invalid input.")
        except:
            pass
    pokemon_options = {"A": "Bulbasaur", "B": "Charmander", "C": "Squirtle"}
    if verbose == True:
        dprint("The old man fumbles in his pocket for a few seconds, before drawing out three small orbs.")
        old_man.speak("Three wonderful Pokemon are imprisoned within these Pokeballs: {}. Which one would you like?".format(final_comma_ampersand(pokemon_options)))
    for alphabet, pokemon in pokemon_options.items():
        dprint(alphabet + " - " + pokemon)
    while True:
        dprint("Input A, B or C:")
        starter_choice = input().upper()
        if starter_choice in pokemon_options.keys():
            break
        else:
            if verbose == True:
                old_man.speak("That wasn't on the agenda! Try again...")
            else:
                print("Invalid input.")
    real_choice = pokemon_options.pop(starter_choice)
    fake_choice = random.choice(list(pokemon_options.keys()))
    if verbose == True:
        old_man.speak("""You chose {}!
...
...
Just joking! You chose {}! Care to give the little bugger a name?""".format(pokemon_options[fake_choice], real_choice)
        )
    else:
        print("You selected {}".format(real_choice))
    while True:
        dprint("Name your {}:".format(real_choice))
        starter_name = input()
        if len(starter_name) >= 2 and len(starter_name) <= 15 and starter_name.isalpha():
            break
        else:
            if verbose == True:
                old_man.speak("Being known only as \"Old Man\", I'm hardly an expert on the subject of names, but come up with a proper name would you?!")
            else:
                print("Invalid name.")

    starter_pokemon = Pokemon(species = real_choice, name = starter_name)
    p.add_pokemon(starter_pokemon)
    if verbose == True:
        starter_pronoun, fellow_lass = ("He", "fellow") if p.active_pokemon.gender == "Male" else ("She", "lass")
        starter_nature = p.active_pokemon.nature.lower()
        a_an = "an" if starter_nature[0] in list("aeiou") else "a"
        dprint("{} pockets the orb containing {} the {}.".format(p.name, p.active_pokemon.name, p.active_pokemon.species))
        old_man.speak("{} should serve you well. {}'s {} {} little {}!".format(p.active_pokemon.name, starter_pronoun, a_an, p.active_pokemon.nature.lower(), fellow_lass))

    ### RIVAL ARRIVES
    if verbose == True:
        dprint("Suddenly, there is a loud thud and the door to the hallway collapses inwards, sending a cloud of dust into the air. When the dust clears, you see a large man clambering slowly to his feet.")
    else:
        print("Johnson arrives.")
    rival = NPC("Johnson")
    rival_starter_mapping = {
    "Bulbasaur": "Charmander",
    "Charmander": "Squirtle",
    "Squirtle": "Bulbasaur"
    }
    rival_starter = rival_starter_mapping[p.active_pokemon.species]
    rival.add_pokemon(Pokemon(species = rival_starter, name = "Scunt", level = 5))
    if verbose == True:
        old_man.speak("Ah, I see {} has arrived!".format(rival.name))
        dprint("You've never met this {} fellow, but there's something about him you don't like.".format(rival.name))
    while True:
        if verbose == True:
            rival.speak("We meet at last {}. I've been waiting for this moment for quite some time. Are you ready to FIGHT?!".format(p.name))
        else:
            rival.speak("Fight?")
        dprint("Input \"Yes\" or \"No\":")
        fight_choice = input()
        if len(fight_choice) > 0:
            if fight_choice.lower()[0] == "y":
                winner = Battle_Trainer(p, rival)
                break
            elif fight_choice.lower()[0] == "n":
                if verbose == True:
                    dprint("Both the old man and {} appear crestfallen.".format(rival.name))
                old_man.speak("Are you sure?")
                dprint("Input \"Yes\" or \"No\":")
                choice = input()
                if choice.lower()[0] == "y":
                    if verbose == True:
                        rival.speak("You great namby-pamby!")
                        dprint("The old man shakes his head sadly and pulls the ropes that previously bound you to the bedframe from his pocket.")
                        old_man.speak("{}, hold him still would you?".format(rival.name))
                        dprint("* THE FOLLOWING TEXT HAS BEEN REDACTED *")
                    winner = rival
                    break
                else:
                    if verbose == True:
                        old_man.speak("Make your bloody mind up!")
            else:
                if verbose == True:
                    old_man.speak("Stop muttering gobbledigook would you?")
                else:
                    print("Invalid input.")
    if p == winner:
        if verbose == True:
            rival.speak("Hoisted on my own petard! You're not quite as incompetent as you seem, {}. Until next time!".format(p.name))
            dprint("{} hitches up his trousers, which had fallen down during the battle, and blunders out of the room.".format(rival.name))
            old_man.speak("Well done {}! That'll show Johnson. Ha!".format(p.name))
    else:
        if verbose == True:
            rival.speak("Ha-ha! I won!")
            dprint("{} grabs the unconscious {} by the scruff of its neck, swings it around his head, and launches it out of the open window.".format(rival.name, starter_pokemon.species))
        rejected_pokemon = p.party.pop(p.party.index(starter_pokemon))
        if verbose == True:
            rival.speak("Better luck next time, loser!")
            dprint("{} hitches up his trousers, which had fallen down during the battle, and blunders out of the room.".format(rival.name))
            old_man.speak("Classic Johnson! Don't worry about {}, we'll find you another {}.".format(starter_pokemon.name, starter_pokemon.species))
            dprint("The old man fumbles in his other pocket and hands you a new Pokeball.")
            old_man.speak("What are you going to call this one?")
        else:
            print("Johnson murders your {}. The old man presents you with a new one.".format(starter_pokemon.species))
        while True:
            dprint("Name your new {}:".format(real_choice))
            starter_name = input()
            if starter_name.lower().strip() == rejected_pokemon.name.lower().strip():
                if verbose == True:
                    old_man.speak("That's imaginative isn't it! Choose a new name, for heaven's sake.")
                else:
                    print("Invalid name.")
            elif len(starter_name) >= 2 and len(starter_name) <= 15 and starter_name.isalpha():
                break
            else:
                if verbose == True:
                    old_man.speak("Being known only as \"Old Man\", I'm hardly an expert on the subject of names, but come up with a proper name would you?!")
                else:
                    print("Invalid name.")
        new_starter_pokemon = Pokemon(species = real_choice, name = starter_name)
        p.add_pokemon(new_starter_pokemon)
        if verbose == True:
            dprint("{} pockets the orb containing {} the {}.".format(p.name, new_starter_pokemon.name, new_starter_pokemon.species))
            old_man.speak("Let's hope {} serves you better than {}. This one's a bit more {}!".format(new_starter_pokemon.name, rejected_pokemon.name, new_starter_pokemon.nature.lower()))
    if verbose == True:
        old_man.speak("Now that you've had your training, it's time for you to venture into the wider world.")
        dprint("With a small \"poof\", the old man disappears. You hesitate before exiting the room, excited to start your adventure...")
        dprint("Press any key to continue.")
    else:
        print("Press any key to enter main game loop.")
    input()
    MainLoop(p)
