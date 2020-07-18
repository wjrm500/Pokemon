import requests
from bs4 import BeautifulSoup, element
import pandas as pd
from pokemon_csv import df
import pdb
import pickle

def see_tag_children(tag):
    for index, value in enumerate(tag.children):
        if isinstance(value, element.Tag):
            closetag_loc = str(value).find(">") + 1
            print(index, " - ", str(value)[0:closetag_loc])
        else:
            print(type(value))
    print("")

def get_tag_child_by_str(tag, string):
    for index, value in enumerate(tag.children):
        if string in str(value):
            return index

def get_moves_from_html_indexes(soup, li):
    moves = []
    lists = []
    a = soup
    for index, value in enumerate(li):
        if index == 3:
            value = get_tag_child_by_str(a, "tabset-moves-game")
        a = list(a.children)[value]
    for child in list(a.children):
        level = int(list(child.children)[0].get_text())
        move = list(child.children)[1].get_text()
        moves.append(move)
        lists.append([level, move])
    return moves, lists

all_moves = []
species_list = list(df["species"])
name_url_mapping = {
    "Nidoran♀": "nidoran-f",
    "Nidoran♂": "nidoran-m",
    "Farfetch'd": "farfetchd",
    "Mr. Mime": "mr-mime"
    }
for key, value in name_url_mapping.items():
    index = species_list.index(key)
    species_list[index] = value
moves_dict = {}
for index, species in enumerate(species_list):
    lists = []
    page = requests.get("https://pokemondb.net/pokedex/{}#dex-moves".format(species))
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        moves, lists  = get_moves_from_html_indexes(soup, [2, 3, 9, "Placeholder", 3, 1, 1, 1, 4, 0, 1])
    except:
        moves, lists = get_moves_from_html_indexes(soup, [2, 3, 9, "Placeholder", 3, 1, 1, 1, 4, 3, 0, 0, 0, 1])
    print(index, species, lists)
    all_moves.append(moves)
    moves_dict[species] = pd.DataFrame(lists, columns = ["level", "move"])

all_moves = list(set([move for moves in all_moves for move in moves]))

moves_by_level["Nidoran♀"] = moves_by_level.pop("nidoran-f")
moves_by_level["Nidoran♂"] = moves_by_level.pop("nidoran-m")
moves_by_level["Farfetch'd"] = moves_by_level.pop("farfetchd")
moves_by_level["Mr. Mime"] = moves_by_level.pop("mr-mime")

pickle_out = open("moves_by_level.pickle", "wb")
pickle.dump(moves_dict, pickle_out)
pickle_out.close()

pickle_out = open("all_moves.pickle", "wb")
pickle.dump(all_moves, pickle_out)
pickle_out.close()
