from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog
import time
import CarData
from nextpage import next_page


def fetch_urls(url):
    links = []
    pages = next_page(url)
    for page in range(pages + 1):
        root_request = requests.get(url)
        if root_request.status_code == 200:
            root_soup = BeautifulSoup(root_request.content, 'html.parser')
            root_tables = root_soup.find_all('div', class_='big')
            for table in root_tables:
                for a in table.find_all('a', class_='image saveSlink'):
                    links.append('https:' + a.get('href'))
            if page >= 2:
                url = url.split(f'/p-{page - 1}')[0] + f'/p-{page}'
    return links


def data_scrape(link):
    car_data = {'Марка': '',
                'Цена': '',
                'Дата на производство': '',
                'Тип двигател': '',
                'Мощност': '',
                'Евростандарт': '',
                'Кубатура [куб.см]': '',
                'Скоростна кутия': '',
                'Категория': '',
                'Пробег [км]': '',
                'Цвят': ''}
    link_request = requests.get(link)
    soup = BeautifulSoup(link_request.content, 'html.parser')
    car_data["Марка"] = ' '.join(soup.find('div', class_='obTitle').text.split()[0:2])
    car_data["Цена"] = ' '.join(soup.find('div', class_='Price').text.strip().split()[0:3])
    tech_data = soup.find('div', class_='techData')
    info = tech_data.find_all("div", class_='item')
    car_info = {}
    for divs in info:
        stripped_divs = [div for div in divs.stripped_strings]
        for index in range(0, len(divs)):
            car_info[stripped_divs[0]] = stripped_divs[1]

    for k, v in car_data.items():
        if k == 'Марка' or k == "Цена":
            continue
        else:
            if k not in car_info:
                car_data[k] = 'Undefined'
    for key, value in car_info.items():
        if key in car_data:
            car_data[key] = value
    return car_data


def main():
    t1 = time.time()
    car_url = 'https://www.mobile.bg/obiavi/avtomobili-dzhipove'
    car_url = car_url + f'/{car_brand_menu.get().lower()}'
    if len(car_model_menu.get()) != 0:
        car_url += f'/{car_model_menu.get().lower()}'
    links = fetch_urls(car_url)
    with ThreadPoolExecutor() as executor:
        dictionaries = list(executor.map(data_scrape, links))
    car_data = {}
    for dictionary in dictionaries:
        for k, v in dictionary.items():
            if k not in car_data:
                car_data[k] = []
            car_data[k].append(v)
    car_data['Links'] = links
    t2 = time.time()
    print(f'{(t2 - t1):.2f}')
    df = pd.DataFrame.from_dict(car_data)
    file_path = filedialog.asksaveasfilename(initialdir='D:', defaultextension=".csv",
                                             filetypes=[("xlsx file", ".xlsx")])
    # df.to_csv(video_path, encoding='utf-8-sig', index=False)
    df.to_excel(file_path, index=False)


def get_values(e):
    car_model_menu.config(values=car_data[car_brand_menu.get()])


if __name__ == '__main__':
    window = Tk()
    root = "https://www.mobile.bg"
    request = requests.get(root)
    soup = BeautifulSoup(request.content, 'html.parser')
    brand = soup.find('div', id='cat5')
    options = brand.find('option')
    car_data = CarData.car_data
    car_brands = [key for key in car_data.keys()]
    variable = StringVar()
    variable.set('Choose a brand:')

    window.geometry('800x800')
    car_brand_label = Label(window,
                            text='Car Brand',
                            font=('Arial', 20, 'bold')
                            )
    car_model_label = Label(window,
                            text='Car Model',
                            font=('Arial', 20, 'bold')
                            )
    car_brand_menu = ttk.Combobox(window,
                                  values=car_brands
                                  )
    car_brand_menu.current(0)
    car_brand_menu.bind("<<ComboboxSelected>>", get_values)
    car_model_menu = ttk.Combobox(window,
                                  values=['']
                                  )
    car_model_menu.current(0)
    scraping_button = Button(window,
                             text='Get information',
                             font=('Arial', 20, 'bold'),
                             command=main,
                             )
    car_brand_label.place(x=200, y=100)
    car_model_label.place(x=400, y=100)
    car_brand_menu.place(x=200, y=150)
    car_model_menu.place(x=400, y=150)
    scraping_button.place(x=270, y=250)
    window.mainloop()
