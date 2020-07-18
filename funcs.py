import time
import sys
import pdb

verbose = False
def verbosity_setup():
    global verbose
    dprint("Press \"V\" for high verbosity, or \"v\" for low verbosity.")
    user_input = input()
    if user_input == "V":
        dprint("You selected \"high verbosity\". Congratulations - a truly magnificent choice!")
        verbose = True
    elif user_input == "v":
        dprint("Verbosity set to \"low\".")
        verbose = False
    return verbose

text_speeds = {
    "Slow":        0.100,
    "Medium-slow": 0.050,
    "Medium":      0.025,
    "Medium-fast": 0.010,
    "Fast":        0.005
    }
text_speed = text_speeds["Fast"]
text_speeds_reverse_mapping = {v: k for k, v in text_speeds.items()}
def dprint_setup():
    global text_speed
    dprint("How fast do you want text to appear? (Speed is currently set to {})".format(text_speeds_reverse_mapping[text_speed]))
    for i, text_speed_key in enumerate(text_speeds.keys()):
        print("({}) {}".format(i + 1, text_speed_key))
    while True:
        user_input = input()
        try:
            user_input = int(user_input)
            selection =  list(text_speeds.keys())[user_input - 1]
            dprint("You selected {}.".format(selection))
            # pdb.set_trace()
            old_text_speed = text_speeds_reverse_mapping[text_speed]
            text_speed = text_speeds[selection]
            dprint("Text speed changed from {} to {}.".format(old_text_speed, selection))
            break
        except:
            dprint("Invalid input detected. Please try again.")

exp_gain_speeds = {
    "Normal": 1,
    "Fast": 8,
    "Rapid": 27,
    "Stupid": 64
    }
exp_gain_speed = exp_gain_speeds["Normal"]
exp_gain_speeds_reverse_mapping = {v: k for k, v in exp_gain_speeds.items()}
def exp_gain_setup():
    global exp_gain_speed
    dprint("How fast do you want Pokemon to gain experience? (Speed is currently set to {})".format(exp_gain_speeds_reverse_mapping[exp_gain_speed]))
    for i, exp_gain_speed_key in enumerate(exp_gain_speeds.keys()):
        print("({}) {}".format(i + 1, exp_gain_speed_key))
    while True:
        user_input = input()
        try:
            user_input = int(user_input)
            selection =  list(exp_gain_speeds.keys())[user_input - 1]
            dprint("You selected \"{}\".".format(selection))
            # pdb.set_trace()
            old_exp_gain_speed = exp_gain_speeds_reverse_mapping[exp_gain_speed]
            exp_gain_speed = exp_gain_speeds[selection]
            dprint("Experience gain speed changed from {} to {}.".format(old_exp_gain_speed, selection))
            break
        except:
            dprint("Invalid input detected. Please try again.")

def dprint(string):
    if isinstance(string, list):
        string = " ".join(string)
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(text_speed)
    print("\r")

def final_comma_ampersand(l):
    if isinstance(l, dict):
        l = list(l.values())
    if isinstance(l, list):
        l = ", ".join(l)
        last_comma_index = l.rfind(",")
        if last_comma_index != -1:
            return l[:last_comma_index] + " &" + l[last_comma_index + 1:]
        else:
            return str(l)
    else:
        pass

def inclusive_range(num1, num2):
    return list(range(num1, num2 + 1))

def get_user_input(dict, first_word_select = False):
    for outer_key, outer_dict in dict.items():
        for inner_key in outer_dict.keys():
            print("({}) {}".format(outer_key, inner_key))
    while True:
        user_input = input()
        try:
            selection = list(dict[user_input].keys())[0]
            if first_word_select:
                dprint("You selected \"{}\".".format(selection.split()[0]))
            else:
                dprint("You selected \"{}\".".format(selection))
            return dict[user_input][selection]
        except:
            dprint("Invalid input detected. Please try again.")
