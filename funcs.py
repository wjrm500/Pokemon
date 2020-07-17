import time
import sys
import pdb

speeds = {
    "Slow":        0.100,
    "Medium-slow": 0.050,
    "Medium":      0.025,
    "Medium-fast": 0.010,
    "Fast":        0.005
    }
speed = speeds["Medium-fast"]
speeds_reverse_mapping = {v: k for k, v in speeds.items()}

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

def dprint_setup():
    global speed
    dprint("How fast do you want text to appear? (Speed is currently set to {})".format(speeds_reverse_mapping[speed]))
    for i, speed_key in enumerate(speeds.keys()):
        print("({}) {}".format(i + 1, speed_key))
    while True:
        user_input = input()
        try:
            user_input = int(user_input)
            selection =  list(speeds.keys())[user_input - 1]
            dprint("You selected {}.".format(selection))
            # pdb.set_trace()
            old_speed = speeds_reverse_mapping[speed]
            speed = speeds[selection]
            dprint("Speed changed from {} to {}.".format(old_speed, selection))
            break
        except:
            dprint("Invalid input detected. Please try again.")

def dprint(string):
    if isinstance(string, list):
        string = " ".join(string)
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
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

def options_from_dict(dict):
    for outer_key, outer_dict in dict.items():
        for inner_key in outer_dict.keys():
            dprint("({}) {}".format(outer_key, inner_key))
    while True:
        user_input = input()
        try:
            selection = list(dict[user_input].keys())[0]
            dprint("You selected {}.".format(selection))
            return dict[user_input][selection]
        except:
            dprint("Invalid input detected.")
        input()
