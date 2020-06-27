import pickle
pickle_in = open("move_details.pickle", "rb")
move_details = pickle.load(pickle_in)
pickle_in.close()
i = 1
for key, value in move_details.items():
    print("{} - {}".format(key, value["effect"]))
    print("")
    i += 1
    if i > 25:
        break
