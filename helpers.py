import re

def format_class(s):
    return re.split(r'(\d+[^\d]*)', s.split(" ")[0])[:-1]

def add_query_params(url, class_name):
    return f"{url}&subject={class_name[0]}&cournum={class_name[1]}"