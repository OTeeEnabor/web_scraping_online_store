import time
import re
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def weight_extract(product_name):
    extract_weight = re.search("[0-9]+ (g|kg)",product_name).group()
    return extract_weight

def weight_converter(extracted_weigt):
    if " g" in extracted_weigt:
        weight = extracted_weigt.replace(" g","")
        weight = float(weight)/1000
    else:
        weight = float(extracted_weigt.replace(" kg",""))
    return weight


def weight_extract_convert(weight_string):
    # combination regular expression
    combination_weight_re = "[0-9]+ x [0-9]+ (g|kg|ml|L)"
    # singular regular expression
    singular_weight_re = "[0-9]+ (g|kg|ml|L)"

    # check for combination string
    if re.search(combination_weight_re, weight_string):
        # split the string into list - [num units , weigh_per_unit]
        combination_split = re.search(combination_weight_re, weight_string).group().split(' x ')
        # num_units
        num_units = int(combination_split[0])
        # unit_string - [g,kg,ml, l]
        weight_unit_string = combination_split[1]
        # check if weight unit is grammes
        if (" g" in weight_unit_string):
            # remove the gramme unit, convert string to float
            weight = float(weight_unit_string.replace(" g", ""))
            # divide weight by 1000 to convert to kg
            weight = weight / 1000 * num_units
        # check if weight unit is mil litres
        elif (" ml" in weight_unit_string):
            # remove the ml unit, convert string to float
            weight = float(weight_unit_string.replace(" ml", ""))
            # divide wight by 1000 to L - 1l -kg
            weight = weight / 1000 * num_units
        # check if kg unit in string
        elif " kg" in weight_unit_string:
            # remove the kg unit in string, convert string to float
            weight = float(weight_unit_string.replace(" kg", "")) * num_units
        else:
            # remove L unit in string, convert string to float
            weight = float(weight_unit_string.replace(" L", "")) * num_units

    elif re.search(singular_weight_re, weight_string):
        # singular algorithm
        weight_string_singular = re.search(singular_weight_re, weight_string).group()
        if " g" in weight_string_singular:
            weight = float(weight_string_singular.replace(" g", "")) / 1000
        elif " ml" in weight_string_singular:
            weight = float(weight_string_singular.replace(" ml", "")) / 1000
        elif " kg" in weight_string_singular:
            weight = float(weight_string_singular.replace(" kg", ""))
        else:
            weight = float(weight_string_singular.replace(" L", ""))
    else:
        weight = None
    try:
        return round(weight, 2)
    except:
        return None
# product_name = "Slicing Tomatoes 8 pk"
def extract_text(soup_object, css_selector):
    return extracted_text
"""

product barcode -class pdp-desc-font
product name - class prod-name
product price - price prod--price
product category - second breadcrumb

"""

options = webdriver.ChromeOptions()
options.add_argument('--headless')
DRIVER_PATH = r"C:/Users/user/Documents/Eden_AI/DataEngineerRoadMap/Web_Scrape_Project/chromedriver.exe"
serv_obj = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=serv_obj,options=options)

category_list = [
    # 'Bread_Brakery_Deserts',
    # 'Milk_Dairy_Eggs',
    # 'Deli_Entertaining',
    # 'Beverages_Juices',
    # 'Pantry',
    # 'Toiletries_health',
    # 'Household',
    # 'Frozen_food',
    # 'Cleaning',
    # 'Snacks'
    # 'meat_poultry'
    'fruit_veg'
]
for index in range(len(category_list)):
    # create file_name
    file_name = f'woolworth_urls/{category_list[index]}_20230513.csv'
    df = pd.read_csv(file_name)
    # get links
    links = df["links"]
    # get category
    cat = df["category"][0]
    output_dict_list = []
    for product_link in links:
        product_dict = {}
        try:
            driver.get(product_link)
            # page_request = requests.get(product_link)
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            # get product name
            product_name = page_soup.css.select(".prod-name")[0].getText()
            # get product barcode
            product_barcode = page_soup.find("li", string="Product code:").find_next_sibling().get_text()
            price_id = f'price_{product_barcode}_{product_barcode}'
            product_price = float(page_soup.css.select(f".prod--price")[0].getText().replace("R ",""))
            # get product weight
            product_weight = weight_extract_convert(product_name)
            # print(product_name)
            # print(product_barcode)
            # print(product_price)
            # print(product_weight)
            product_dict['name'] = product_name
            product_dict['barcode'] = product_barcode
            product_dict['price'] = product_price
            product_dict['weight'] = product_weight
            product_dict['category'] = cat
            product_dict['date'] = '16-05-2023'

            output_dict_list.append(product_dict)
        except Exception as e:
            print(e)
    product_df = pd.DataFrame(output_dict_list)
    product_df.to_csv(f'woolworth_product/woolworths_{cat}_20230516.csv',index=False)
    print(f'Done.{cat}:Saved to csv')