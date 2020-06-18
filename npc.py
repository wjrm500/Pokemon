from funcs import dprint

class NPC():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.pokemon = []

    def add_pokemon(self, poke):
        self.pokemon.append(poke)

    def speak(self, text = "Bugger me, I've got nothing to say!"):
        dprint('{}: "{}"'.format(self.name, text))
