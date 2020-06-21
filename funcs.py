import time
import sys

def dprint(string):
    if isinstance(string, list):
        string = " ".join(string)
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)
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
