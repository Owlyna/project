#Спарсить Топ 250
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

data=[]
for page in range(1, 6):
    url = f'https://www.kinopoisk.ru/lists/movies/top250/?page=' + str(page) + '&utm_referrer=www.kinopoisk.ru'
    driver = webdriver.Edge()
    driver.get(url)    
    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "styles_contentSlot__h_lSN"))
        )        
    finally:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        films = soup.find_all(class_="styles_root__ti07r")
        for film in films:
            #название фильма
            film_name = film.find(class_="styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj")
            for name in film_name:
                name = name.text
            #год выпуска
            year_film = film.find(class_="desktop-list-main-info_secondaryText__M_aus")
            for year in year_film:
                year = year.text.lstrip(", ")[:4]
            import re
            info_film = film.find(string=re.compile("Режиссёр")).text
            #страна выпуска
            country = info_film.split(" • ")[0]
            #режиссер
            director = info_film.split(': ')[-1] 
            #жанр
            genre = info_film.replace('\xa0', ' • ').split(" • ")[1]
            #рейтинг
            #количество голосов
            votes_film = film.find(class_="styles_kinopoiskCount__PT7ZX")
            for votes in votes_film:
                votes = votes.text.lstrip(" ")
            value_film = film.find(class_="styles_kinopoiskValuePositive__7AAZG styles_kinopoiskValue__nkZEC styles_top250Type__QsUyJ")
            for value in value_film:
                value = value.text
            
            driver.quit()
            data.append([name, year, country, genre, director, value, votes])
table_header = ['Название фильма', 'Год выпуска', 'Страна выпуска', 'Жанр', 'Режиссер', 'Оценка', 'Количество отзывов']
df = pd.DataFrame(data, columns = table_header)
df.to_excel (r'C:\Users\supei\OneDrive\Рабочий стол\parsing\database.xlsx')
