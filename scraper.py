from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import format_class

# constants
# classes
xpath_classes_list_1 = '//*[@id="__KUALI_TLP"]/div/div[2]/div[4]/span/div/div/div/div/div/div/section[2]/div/div[2]/section[1]/div/div/div/ul/li/div/div/ul'
xpath_classes_list_2 = '//*[@id="__KUALI_TLP"]/div/div[2]/div[4]/span/div/div/div/div/div/div/section[2]/div/div[2]/section[2]/div/div/div/ul/li/ul/li[2]/div/div/ul'


table_xpath = "/html/body/main/p[2]/table/tbody"
class_info_links = [
    "/html/body/main/p[2]/table/tbody/tr[3]/td[2]/table/tbody",
    "/html/body/main/p[2]/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td[2]/table/tbody",
    "/html/body/main/p[2]/table/tbody/tr[4]/td[2]/table/tbody",
]


class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    def get_element_info(self, xpath):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_class_info(self):
        self.driver.get(self.url)

        self.driver.find_element(By.XPATH, table_xpath)

        for xpath in class_info_links:
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                return element.text
            except Exception as e:
                print(f"err w link {self.url}")
                continue

    def get_classes(self, use_cache=True):
        if use_cache:
            with open("classes.txt", "r") as f:
                classes = f.readlines()
        else:
            classes = self.get_element_info(xpath_classes_list_2).split("\n")
            classes.extend(self.get_element_info(xpath_classes_list_2).split("\n"))

            with open("classes.txt", "w") as f:
                f.write("\n".join(classes))

        return [format_class(c) for c in classes]

    def quit(self):
        self.driver.quit()
