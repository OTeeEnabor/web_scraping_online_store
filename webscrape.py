import time
import re
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import date
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# define DRIVER PATH

"""
1 - go to department site
2 - go through each page collecting page url
3 - use bs4 to parse through each page collecting - product name, weight, price, number, date
4 - 
"""
def create_directory(path):
    today = date.today()

    date_folder = f"{today.year}{today.month}{today.day}"

    # check if today_directory exists
    folder_path = f'{path}/{date_folder}'
    # check if exists
    is_exists = os.path.exists(folder_path)
    if is_exists:
        print('exists')
    else:
        os.mkdir(folder_path)
        print(f'{folder_path} created')



def pagination(base_url,category):
    # create pagination logger
    pagination_logger = logging.getLogger(f'Pagination_{category}')
    # set logger level to information
    pagination_logger.setLevel(logging.INFO)
    # define configuration for logger
    global date_stamp
    pagination_config = {
        "FORMATTER_FORMAT": "%(levelname)s - %(asctime)s - %(name)s: -%(message)s",

        "LOG_FILE": f"woolworth_urls/log_files/{date_stamp}/pagination_logger_{category}.log"
    }
    # create log file that has date stamp
    formatter = logging.Formatter(pagination_config["FORMATTER_FORMAT"])
    file_handler = logging.FileHandler(pagination_config["LOG_FILE"])
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    pagination_logger.addHandler(file_handler)
    # log successfull creation of logg object
    pagination_logger.info("Pagination logger created - ")
    DRIVER_PATH = r"C:/Users/user/Documents/Eden_AI/DataEngineerRoadMap/Web_Scrape_Project/chromedriver.exe"
    serv_obj = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=serv_obj)
    # implicit wait
    driver.implicitly_wait(0.5)
    # maximize the browser window
    driver.maximize_window()
    # get the html of the base url
    driver.get(base_url)
    pagination_logger.info(f"{base_url} opened and page downloaded.")
    time.sleep(5)
    # get product url in each page
    # find the next pagination button
    next_button = driver.find_elements(By.CLASS_NAME,"pagination__nav")[1]
    # check if the button page is displayed
    next_button_displayed = next_button.is_displayed()
    # if button is displayed -
    if next_button_displayed:
        # sleep for 5 seconds
        time.sleep(5)
        # create an empty list of product links
        product_links = []
        while True:
            try:
                # find all anchor tags with class - product--view
                product_anchors = driver.find_elements(By.CLASS_NAME, "product--view")
                # for each url in this page
                for link in product_anchors:
                    # get the url
                    link_href = link.get_attribute('href')
                    # append the url to the product link
                    product_links.append(link_href)
                    pagination_logger.info(f'{link_href} appended into product link list.')
                # print the length of product urls collected in each page
                pagination_logger.info(f'len(product_links) collected...')
                # print(len(product_links))
                # find the next button - again (to keep element fresh)
                next_button = driver.find_elements(By.CLASS_NAME, "pagination__nav")
                # check if there is more than one button found
                if len(next_button) > 1:
                    # if more than one - get the second button
                    next_button = next_button[1]
                    # scroll to the button
                    driver.execute_script('arguments[0].scrollIntoView(true);', next_button)
                    # click on the button
                    next_button.click()
                    pagination_logger.info(f"Next page button clicked")
                    print("next button clicked")
                else:
                    # select first button
                    #then fail successfully
                    next_button = next_button[0]
                driver.implicitly_wait(10)
            except Exception as e:
                pagination_logger.error(f"error occurred - {e}")
                break
    return product_links

# url =
url_list = [
    'https://www.woolworths.co.za/cat/Food/Fruit-Vegetables-Salads/_/N-lllnam',
    'https://www.woolworths.co.za/cat/Food/Meat-Poultry-Fish/_/N-d87rb7',
    'https://www.woolworths.co.za/cat/Food/Bread-Bakery-Desserts/_/N-1bm2new',
    'https://www.woolworths.co.za/cat/Food/Ready-Meals/_/N-s2csbp',
    'https://www.woolworths.co.za/cat/Food/Milk-Dairy-Eggs/_/N-1sqo44p',
    'https://www.woolworths.co.za/cat/Food/Deli-Entertaining/_/N-13b8g51'
    'https://www.woolworths.co.za/cat/Food/Beverages-Juices/_/N-mnxddc',
    'https://www.woolworths.co.za/cat/Food/Pantry/_/N-1lw4dzx',
    'https://www.woolworths.co.za/cat/Food/Toiletries-Health/_/N-1q1wl1r',
    'https://www.woolworths.co.za/cat/Food/Household/_/N-vvikef',
    'https://www.woolworths.co.za/cat/Food/Frozen-Food/_/N-j8pkwq',
    'https://www.woolworths.co.za/cat/Food/Cleaning/_/N-o1v4pe',

]
category_list = [
    'Fruit_Veg',
    'Meat_poultry_fish',
    'Bread_Bakery_Deserts',
    'Ready_meals',
    'Milk_Dairy_Eggs',
    'Deli_Entertaining'
    'Beverages_Juices',
    'Pantry',
    'Toiletries_health',
    'Household',
    'Frozen_food',
    'Cleaning'
]

current_date = date.today()
day = current_date.day
month = current_date.month
year = current_date.year
date_stamp = f"{year}{month}{day}"
create_directory(f"woolworth_urls")
create_directory(f"woolworth_urls/log_files")
for index in range(len(url_list)):
    product_links = pagination(url_list[index], category_list[index])
    product_dictionary = {'links': product_links}
    product_df = pd.DataFrame(product_dictionary)
    product_df['date'] = current_date # can get date using date module date.today()
    product_df['category'] = category_list[index]
    product_file_name = f'woolworth_urls/{date_stamp}/{category_list[index]}_{date_stamp}.csv'
    product_df.to_csv(product_file_name)

