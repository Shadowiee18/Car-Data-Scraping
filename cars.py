from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def fetch_brands():
    brand_model = {}
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    service = Service(executable_path=r'C:\Users\bai4o\PycharmProjects\pythonProject\PyCharm Projects\Self Learning\Web scraping\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    root = "https://www.mobile.bg"
    driver.get(root)
    driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]/div[2]/div[2]/button[1]/p').click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    brand = soup.find('div', id='cat5')
    brand_options = brand.find_all('option')
    car_brands = [option.text.strip() for option in brand_options][2:-4]
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "cat5")))
    brands = Select(driver.find_element(By.XPATH, '//*[@id="cat5"]/select'))
    for car_brand in car_brands:
        brands.select_by_value(car_brand)
        brand_model[car_brand] = driver.find_element(By.ID, 'cat7').text.strip().split()[1:]
    return brand_model


fetch_brands()
