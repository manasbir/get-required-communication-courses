from scraper import Scraper
import re
from helpers import format_class

url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/rJj6aXDk6?searchTerm=bachelor%20of%20math&bc=true&bcCurrent=Bachelor%20of%20Mathematics%20Degree%20Requirements&bcItemType=programs"
xpath_1 = '//*[@id="__KUALI_TLP"]/div/div[2]/div[4]/span/div/div/div/div/div/div/section[2]/div/div[2]/section[1]/div/div/div/ul/li/div/div/ul'
xpath_2 = '//*[@id="__KUALI_TLP"]/div/div[2]/div[4]/span/div/div/div/div/div/div/section[2]/div/div[2]/section[2]/div/div/div/ul/li/ul/li[2]/div/div/ul'

scraper = Scraper(url)

classes = scraper.get_element_info(xpath_1).split("\n")
classes.extend(scraper.get_element_info(xpath_2).split("\n"))
scraper.quit()

classes = [format_class(c) for c in classes]

print(classes[0])



