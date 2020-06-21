from funcs import dprint

class Player():
    def __init__(self, name):
        self.name = name.capitalize()
        self.location = "home"
        self.inventory = {"Pokeball": 1, "Potion": 1}
        self.pokemon = []

    def set_gender(self, gender):
        if gender.lower() in ("male", "m"):
            self.gender = "male"
        elif gender.lower() in ("female", "f"):
            self.gender = "female"
        else:
            self.gender = "unspecified"

    def move(self):
        new_location = input("Where would you like to go?")
        self.location = new_location

    def interact(self):
        self.location.interact(self)

    def display_pokemon(self):
        for pokemon in self.pokemon:
            pokemon.display()

    def display_inventory(self):
        dprint("Your bag contains the following items...")
        for item, quantity in self.inventory.items():
            dprint("{} x {}".format(quantity, item))

    def switch_pokemon(self):
        if len(self.pokemon) > 1:
            choice_mapping = {}
            for index, poke in enumerate(self.pokemon):
                dprint("({}) {} ({})".format(index + 1, poke.name, poke.species))
                choice_mapping[str(index + 1)] = poke
            dprint("Which Pokemon would you like to switch in?")
            choice = input()
            chosen_pokemon = choice_mapping[choice]
            self.pokemon.insert(0, self.pokemon.pop(chosen_pokemon))
        else:
            dprint("You only have one Pokemon in your party!")
