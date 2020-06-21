import requests
from bs4 import BeautifulSoup
import pickle
from slugify import slugify
import pandas as pd

pickle_in = open("all_moves.pickle", "rb")
all_moves = pickle.load(pickle_in)

def convert_to_na(str):
    if str == "—":
        return "NA"
    else:
        return str

move_details = {}
for index, move in enumerate(all_moves):
    print(index, move)
    slug_move = slugify(move)
    page = requests.get("https://pokemondb.net/move/{}".format(slug_move))
    soup = BeautifulSoup(page.content, "html.parser")
    all_tds = soup.find_all("td")
    move_type = all_tds[0].find("a").get_text()
    category = all_tds[1].get_text().strip()
    power = convert_to_na(all_tds[2].get_text())
    accuracy = convert_to_na(all_tds[3].get_text())
    pp = all_tds[4].get_text().split()[0]
    effect = soup.find_all("div")[2].find("p").get_text()
    move_dict = {
    "move_type": move_type,
    "category": category,
    "power": power,
    "accuracy": accuracy,
    "pp": pp,
    "effect": effect
    }
    move_details[move] = move_dict

pickle_out = open("move_details.pickle", "wb")
pickle.dump(move_details, pickle_out)
pickle_out.close()
