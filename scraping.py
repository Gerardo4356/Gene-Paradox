from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def Browser(headless=False):
    options = webdriver.EdgeOptions()
    if headless: options.add_argument("--headless")
    # options.add_argument("start-maximized")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=options)
    return driver