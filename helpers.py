import re

def format_class(s):
    print( s.split(" ")[0])
    return re.split(r'(\d+)', s.split(" ")[0])[:-1]