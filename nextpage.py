from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def next_page(url):
    options = Options()
    options.add_argument('--headless=new')
    service = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    pages = driver.find_element(By.XPATH, '/html/body/form[3]/div[1]').text.split()
    pages = round(int(pages[pages.index('общо') + 1].replace('+', '')) / 20)
    return pages
