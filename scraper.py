from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def quit(self):
        self.driver.quit()
