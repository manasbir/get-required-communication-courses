from scraper import Scraper
import re
from helpers import format_class, add_query_params

# mandatory classes
classes_url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/rJj6aXDk6?searchTerm=bachelor%20of%20math&bc=true&bcCurrent=Bachelor%20of%20Mathematics%20Degree%20Requirements&bcItemType=programs"

# class info
class_info_url = "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1251"

# get required classes from uwaterloo.ca
scraper = Scraper(classes_url)
classes = scraper.get_classes(use_cache=True)
scraper.quit()

list_of_classes = []

for c in classes:
    try:
        list_of_info = []
        scraper = Scraper(add_query_params(class_info_url, c))
        scraper.quit()
        lines = scraper.get_class_info().split("\n")[1:]
        columns = [c.split(" ") for c in lines]

        for col in columns:
            if col[0].isdigit(): # col is good to check
                if col[4] != "ONLINE":
                    list_of_info.append({ "class": " ".join(c), "online": "no"})
                list_of_info.append({ "class": " ".join(c), "online": "yes" ,"available": col[6]>col[7] })
            else:
                continue
        if len(list_of_info) == 0:
            list_of_classes.append({ "class": " ".join(c), "available": "err/not offered this semester" })
        elif len(list_of_info) > 1:
            for list in list_of_info:
                if list["online"] == "yes":
                    list_of_classes.append(list)
                    break
        else: 
            list_of_classes.extend(list_of_info)

    except Exception as e:
        scraper.quit()
        print(f"Error with class {c}, \nError: {e}")
        list_of_info.append({ "class": " ".join(c), "available": "err/not offered this semester" })

print(list_of_info)
