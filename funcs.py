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

def inclusive_range(num1, num2):
    return list(range(num1, num2 + 1))

def remove_dirs_not_containing_pickle(dpath):
    import os
    if os.path.isdir(dpath):
        entries = [os.path.join(dpath, entry) for entry in os.listdir(dpath)]
        subdirs = filter(os.path.isdir, entries)
        if all(map(remove_dirs_not_containing_pickle, subdirs)):
            files = filter(os.path.isfile, entries)
            pdf_files = [f for f in files if f.endswith(".PICKLE")]
            if not pdf_files:
                try:
                    for f in files:
                        os.unlink(f)
                    os.rmdir(dpath)
                except OSError as e:
                    return False
                return True
        return False
    else:
        return False
