# debug.py

from config import DEBUGGING, VERBOSE

# define the debug function
def debug(*args):
    if DEBUGGING:
        print("DEBUG:", *args)

# define the verbose function
def verbose(*args):
    if VERBOSE:
        print("VERBOSE:", *args)

# define the error function
def error(*args):
    print("ERROR:", *args)

def info(*args):
    print("INFO:", *args)

