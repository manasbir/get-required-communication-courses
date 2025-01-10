from scraper import Scraper
import pandas as pd
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
        scraper = Scraper(add_query_params(class_info_url, c))
        lines = scraper.get_class_info().split("\n")[1:]
        scraper.quit()
        rows = [c.split(" ") for c in lines]

        for idx, row in enumerate(rows):
            if row[0].isdigit():  # col is good to check
                list_of_classes.append(["".join(c), row[4] == "ONLINE", row[6] > row[7]])
            elif row[0] == "Reserve:" and row[1] == "Math":
                list_of_classes.append(["".join(c),rows[idx-1][4] == "ONLINE",rows[idx-1][6] > rows[idx-1][7]])
            else:
                print(f"Error with class {c}, \nError: {row}")
                continue

        # if len(list_of_info) == 0:
        #     list_of_classes.append(
        #         {"class": "".join(c), "available": "err/not offered this semester"}
        #     )
        # # elif len(list_of_info) > 1:
        # #     for row in list_of_info:
        # #         if row["online"] == "yes":
        # #             list_of_classes.append(row)
        # #             break
        # else:
        #     list_of_classes.extend(list_of_info)

    except Exception as e:
        scraper.quit()
        print(f"Error with class {c}, \nError: {e}")
        list_of_classes.append([" ".join(c), "err", "err"])

df = pd.DataFrame(list_of_classes, columns=["class", "is online?", "is full?"])
df.to_csv("classes.csv", index=False)
# sort by online and then by full
df = df.sort_values(["is online?", "is full?"], ascending=[False, True])
df.to_csv("classes_sorted.csv", index=False)
# filter by online
df = df[df["is online?"] == True]
df.to_csv("classes_online.csv", index=False)