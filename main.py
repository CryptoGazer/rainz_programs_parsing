import requests
from bs4 import BeautifulSoup

import re
import csv
from pprint import pprint


RAINZ_URL = "https://rainz.ru"
PROGRAMS_URL = "https://rainz.ru/programs"


def rainz_parsing() -> list:

    response = requests.get(PROGRAMS_URL)

    soup = BeautifulSoup(response.text, "lxml")

    # body = soup.find_all("body")
    # outer_section_wrapper = soup.find("section", class_="section section_catalog section_dark").find("div", class_="section__wrapper")
    section_catalogs = soup.find_all("div", class_="catalog section__catalog")
    # pprint(section_catalogs)

    programs = []

    for section_catalog in section_catalogs:
        # pprint(section_catalog)
        print()
        print()

        catalog_title = section_catalog.find_next("h2", class_="catalog__title").text
        catalog_items = section_catalog.find_all_next("div", class_="catalog__item")

        print(catalog_title)
        for catalog_item in catalog_items:
            # print(catalog_item)
            program_title = catalog_item.find_next("span", class_="program-block__caption").text
            popularity = re.search(r"width:(\d+%)", catalog_item.find_next("span", class_="progress-bar__value").get("style")).group(1)
            duration = catalog_item.find_next("span", class_="program-block__duration").text
            short_description = catalog_item.find_next("span", class_="program-block__text").find_next('p').text

            # получение большого описания
            program_url = RAINZ_URL + catalog_item.find_next('a', class_="program-block program-block_catalog").get("href")
            program_url_response = requests.get(program_url)
            program_soup = BeautifulSoup(program_url_response.text, "lxml")
            extended_description = (
                program_soup.find("body")
                .find_next("section", class_="section section_dark")
                .find_next("div", class_="section__wrapper")
                .find_next("div", class_="section__header")
                .find_next("div", class_="section__text")
                .find_next('p')
                .text
            )

            programs.append([program_title, catalog_title, popularity, duration, short_description, extended_description])

            # programs[catalog_title].append(
            #     {
            #         program_title: {  # значения словаря соответствуют значениям столбцов таблицы, начиная с 3-го включительно
            #             "popularity": popularity,
            #             "duration": duration,
            #             "short_description": short_description,
            #             "extensive_description": extensive_description
            #         }
            #     }
            # )
    # pprint(programs)

    return programs


parsed_programs = rainz_parsing()
# pprint(parsed_programs)
# print()

# в Гугл-таблицы

table_data = [["Название", "Категория", "Популярность", "Длительность", "Краткое описание", "Полное описание"]]
table_data.extend(parsed_programs)
pprint(table_data)

with open("/csv_data/programs_knowledge_base.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(table_data)
