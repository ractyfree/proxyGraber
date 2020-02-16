from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SeleniumWrapper:
    def __init__(self):
        self.__driver = webdriver.Chrome()
        self.__delay = 3

    def openPage(self, link):
        return self.__driver.get(link)


    def input(self, xpath, input):
        pass

    def click(self, xpath):
        return self.__driver.find_element_by_xpath(xpath).click()

    def waitPageLoaded(self, xpath):
        return WebDriverWait(self.__driver, self.__delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def getCurrentPage(self):
        return self.__driver.page_source
    
    def close(self):
        return self.__driver.quit()

    def getElementByXPATH(self, xpath):
        return self.__driver.find_element_by_xpath(xpath)
