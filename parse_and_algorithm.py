import cv2
import os
from datetime import date
import requests
import time
from fuzzywuzzy import fuzz
import keyboard as keyb
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By

months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
          "декабря"]


class Card():
    fname = ''
    breed = ''
    category = ''
    sex = ''
    size = ''
    wool = ''
    date_of_lose = ''
    locality = ''
    place_of_loss = ''
    age = ''
    special_sign = ''
    add_info = ''
    mail = ''


def find_match(lost_animal, found_animals, path1, path2):
    max_global_similarity = -1000000
    most_similar_found_animal = Card()
    image_lost_animal = cv2.imread(path1 + lost_animal.fname)
    hist1 = cv2.calcHist([image_lost_animal], [0], None, [256], [0, 256])
    for found_animal in found_animals:
        filter_similarity = 0

        if (lost_animal.category != found_animal.category) & (lost_animal.category != "") & (found_animal.category != ""):
            continue
        if (lost_animal.date_of_lose != "") & (found_animal.date_of_lose != ""):
            temp1 = lost_animal.date_of_lose.split()
            temp2 = (found_animal.date_of_lose.
                     split())
            d1 = date(int(temp1[2]), months.index(temp1[1]) + 1, int(temp1[0]))
            d2 = date(int(temp2[2]), months.index(temp2[1]) + 1, int(temp2[0]))

            if d1 > d2:
                continue
            if (d2 - d1).days <= 365:
                filter_similarity += 365 - (d2 - d1).days

        if (lost_animal.locality == found_animal.locality) & (lost_animal.locality != "") & (found_animal.locality != ""):
            filter_similarity += 100
            if (lost_animal.place_of_loss == found_animal.place_of_loss) & (lost_animal.place_of_loss != "") & (found_animal.place_of_loss != ""):
                filter_similarity += 100
        if (lost_animal.size == found_animal.size) & (lost_animal.size != "") & (found_animal.size != ""):
            filter_similarity += 75
        if (lost_animal.wool == found_animal.wool) & (lost_animal.wool != "") & (found_animal.wool != ""):
            filter_similarity += 50
        if (lost_animal.breed == found_animal.breed) & (lost_animal.breed != "") & (found_animal.breed != ""):
            filter_similarity += 50
        if (lost_animal.sex == found_animal.sex) & (lost_animal.sex != "") & (found_animal.sex != ""):
            filter_similarity += 25
        if (lost_animal.age == found_animal.age) & (lost_animal.age != "") & (found_animal.age != ""):
            if abs(int(lost_animal.age) - int(found_animal.age)) > 3:
                filter_similarity += 15 * (abs(int(lost_animal) - int(found_animal)))
        if (lost_animal.special_sign != "") & (found_animal.special_sign != ""):
            filter_similarity += fuzz.token_sort_ratio(lost_animal.special_sign, found_animal.special_sign)
        if (lost_animal.add_info != "") & (found_animal.add_info != ""):
            filter_similarity += fuzz.token_sort_ratio(lost_animal.add_info, found_animal.add_info)

        image_lost_animal = cv2.imread(path2 + found_animal.fname)
        hist2 = cv2.calcHist([image_lost_animal], [0], None, [256], [0, 256])

        photo_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL) + 0.2
        global_similarity = photo_similarity + filter_similarity * 0.0025

        if global_similarity > max_global_similarity:
            max_global_similarity = global_similarity
            most_similar_found_animal = found_animal

    return most_similar_found_animal

def download_image_from_page(page_url, save_folder, i):
    driver = webdriver.Chrome()
    driver.get(page_url)
    time.sleep(5)
    btn_k = driver.find_element(By.CLASS_NAME, "k-input-button")
    btn_k.click()
    keyb.press_and_release("enter")
    keyb.press_and_release("down")
    keyb.press_and_release("down")
    keyb.press_and_release("down")
    time.sleep(10)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    img_tags = soup.find_all('img') # парсим все теги img
    btn_cards = driver.find_elements(By.CLASS_NAME, "card")

    for img_tag in img_tags:
        img_url = urljoin('https://animals.admhmao.ru', img_tag['src']) #добавляем url страницы к url изображения из src
        print(img_url)
        save_path = os.path.join(save_folder, f"{os.path.basename(img_url)}.png") # создание пути сохранения изображения
        i += 1
        # Проверка наличия файла перед сохранением
        if not os.path.exists(save_path):
            print('Сохраняем изображение...')
            download_image(img_url, save_path, driver, i, btn_cards)
        else:
            print('Изображение уже существует.')


def download_image(url, save_path, driver, i, btn_cards): #img_tag - типа i
    try: # проверка наличия картинки
        new_lost_animal = Card()
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path, format='PNG')
        new_lost_animal.fname = os.path.basename(save_path) #== 2.png

        btn_cards[i].click()
        values = driver.find_elements(By.CLASS_NAME, "value")
        new_lost_animal.breed = values[0].text
        new_lost_animal.category = values[1].text
        new_lost_animal.sex = values[2].text
        new_lost_animal.size = values[3].text
        new_lost_animal.wool = values[4].text
        new_lost_animal.date_of_lose = values[5].text
        new_lost_animal.locality = values[6].text
        new_lost_animal.place_of_loss = values[7].text
        new_lost_animal.age = values[8].text
        new_lost_animal.special_sign = values[9].text
        new_lost_animal.add_info = values[10].text
        new_lost_animal.mail = "modin.ru2@mail.ru"

        x = driver.find_elements(By.CLASS_NAME, "k-icon-button")
        x[len(x) - 1].click()

        lost_animals.append(new_lost_animal)

    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")


page_url = "https://animals.admhmao.ru/animals/advertisement-public"
save_folder = r"lost_animals_img"
found_animals = []
lost_animals = []
urls_img = []
i = -1
download_image_from_page(page_url, save_folder, i)


