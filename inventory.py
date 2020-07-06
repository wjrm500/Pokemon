import numpy as np
from funcs import dprint
from taketurn import TakeTurn

class Inventory():
    def __init__(self, player):
        self.player = player
        self.items = {
            "Poke Ball": 1,
            "Potion": 1
            }

    def add_item(self, item, quantity = 1):
        if item in self.items.values():
            self.items[item] += quantity
        else:
            self.items.update({item: quantity})

    def delete_item(self, item):
        del self.items[item]

    def display_items(self, opponent = "NA"):
        if not self.items:
            dprint("No items in bag!")
            return
        dprint("Your bag contains the following items...")
        for i, (key, value) in enumerate(self.items.items()):
            dprint("({}) {} ({} thereof)".format(i + 1, key, value))
        return self.select_item(opponent)

    def select_item(self, opponent = "NA"):
        while True:
            try:
                dprint("Which item would you like to select?")
                dprint("Input a number:")
                choice = int(input()) - 1
                mapped_choice = list(self.items.keys())[choice]
                dprint("You selected {}.".format(mapped_choice))
                self.items[mapped_choice] -= 1
                if self.items[mapped_choice] == 0:
                    self.delete_item(mapped_choice)
                if "Ball" in mapped_choice:
                    pokeball_success = TakeTurn.throw_pokeball(self.player, opponent, ball_type = mapped_choice)
                    if pokeball_success:
                        return "pokemon_caught"
                    else:
                        return "pokeball_missed"
                elif "Potion" in mapped_choice:
                    TakeTurn.drink_potion(self.player, mapped_choice)
                    return "potion_drunk"
                return "no_item_used"
            except:
                pass
