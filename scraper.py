from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class_info_xpath = '/html/body/main/p[2]/table/tbody/tr[3]/td[2]/table/tbody'
class_info_alt_xpath = '/html/body/main/p[2]/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td[2]/table/tbody'

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
        try: 
            element = self.driver.find_element(By.XPATH, class_info_xpath)
            return element.text
        except Exception as e:
            element = self.driver.find_element(By.XPATH, class_info_xpath)
            return element.text
        

    def quit(self):
        self.driver.quit()
