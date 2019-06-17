from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import requests

from datetime import datetime, timedelta

import csv

import time
import os
from pathlib import Path


def is_download_finished(temp_folder):
    firefox_temp_file = sorted(Path(temp_folder).glob('*.part'))
    chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    downloaded_files = sorted(Path(temp_folder).glob('*.*'))
    if (len(firefox_temp_file) == 0) and \
       (len(chrome_temp_file) == 0) and \
       (len(downloaded_files) >= 1):
        return True
    else:
        return False

BASE_PATH_NATIONS = "/Users/francesco/Desktop/Cose da Sistemare/test_p/"



local_saving_folder = BASE_PATH_NATIONS + "raw_data"


# carbon
http_request = requests.get('https://www.quandl.com/api/v3/datasets/CHRIS/ICE_C1.csv?api_key=-q3ecFz_jdpZBNM73ozq')

with open(local_saving_folder + "/carbon.csv", "w") as carbon_file:
    carbon_file.write(http_request.text)

carbon_prices = {}
with open(local_saving_folder + "/carbon.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first = True
    for row in csv_reader:
        if first:
            first = False

        else:
            raw_date = str(str(row[0]).split(' ')[0]).split('-')
            current_date = datetime(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
            carbon_prices[current_date] = float(row[4])


for a in carbon_prices:
    print str(a) + " " + str(carbon_prices[a])






