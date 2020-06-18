from inventory import Inventory

class Player():
    def __init__(self, name):
        self.name = name.capitalize()
        self.location = "home"
        self.inventory = Inventory()
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
        self.inventory.display()
