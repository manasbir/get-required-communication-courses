from scraper import Scraper
import re
from helpers import format_class, add_query_params

# constants
# classes
classes_url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/rJj6aXDk6?searchTerm=bachelor%20of%20math&bc=true&bcCurrent=Bachelor%20of%20Mathematics%20Degree%20Requirements&bcItemType=programs"
xpath_classes_list_1 = '//*[@id="__KUALI_TLP"]/div/div[2]/div[4]/span/div/div/div/div/div/div/section[2]/div/div[2]/section[1]/div/div/div/ul/li/div/div/ul'
xpath_classes_list_2 = '//*[@id="__KUALI_TLP"]/div/div[2]/div[4]/span/div/div/div/div/div/div/section[2]/div/div[2]/section[2]/div/div/div/ul/li/ul/li[2]/div/div/ul'

# class info
class_info_url = "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1251"

# indexes from class_info
indexes = [3 , 6, 7]

# get required classes from uwaterloo.ca
scraper = Scraper(classes_url)

classes = scraper.get_element_info(xpath_classes_list_2).split("\n")
classes.extend(scraper.get_element_info(xpath_classes_list_2).split("\n"))
scraper.quit()

classes = [format_class(c) for c in classes]

list_of_info = []

for c in classes:
    try:
        scraper = Scraper(add_query_params(class_info_url, c))
        scraper.quit()
        lines = scraper.get_class_info().split("\n")[1:]
        columns = [c.split(" ") for c in lines]

        for col in columns:
            if col[0].isdigit(): # col is good to check
                if col[4] != "ONLINE": continue
                list_of_info.append({ "class": " ".join(c), "available": "online, yes, is at capacity?" + col[6]>col[7] })
            else:
                continue

    except Exception as e:
        scraper.quit()
        print(f"Error with class {c}, \nError: {e}")
        list_of_info.append({ "class": " ".join(c), "available": "err/not offered this semester" })

print(list_of_info)
