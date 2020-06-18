import pickle
pickle_in = open("moves_dict.pickle", "rb")
moves_dict = pickle.load(pickle_in)
for key, value in moves_dict.items():
    print(key)
    print(value.head())
    print("")
