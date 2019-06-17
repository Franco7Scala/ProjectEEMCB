# -*- coding: utf-8 -*-
import holidays
import sys
import time
from selenium import webdriver
from pathlib import Path


BASE_PATH_NATIONS = "/Users/francesco/Desktop/Cose da Sistemare/test_p/"


def colored_print(text, color):
    if color == "yellow":
        code_color = '\033[93m'
    elif color == "blue":
        code_color = '\033[94m'
    elif color == "green":
        code_color = '\033[92m'
    elif color == "red":
        code_color = '\033[91m'
    elif color == "pink":
        code_color = '\033[95m'
    else:
        code_color = ''
    print code_color + str(text) + '\033[0m'


def print_progress_bar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    if iteration == total:
        print()


def calculate_relative_error(real_output, expected_output):
    if real_output != 0:
        return abs((real_output - expected_output) / real_output)
    else:
        return abs((real_output - expected_output) / (real_output + 0.0001))


def is_business_day(date, nation):
    if nation == "FR":
        nation = "FRA"
    
    try:
        return date in holidays.CountryHoliday(nation)
    except KeyError:
        return False


def double_contains(value, elements):
    for element in elements:
        if value in element:
            return True

    return False


def download_from_macrotrends(url, download_folder):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(BASE_PATH_NATIONS + "chromedriver", chrome_options=options)
    driver.get(url)
    ul = driver.find_elements_by_id("myTabs")[0]
    li = ul.find_elements_by_tag_name("li")[1]
    li.click()
    iframe = driver.find_elements_by_id("chart_iframe_menu1")[0]
    driver.switch_to.frame(iframe)
    button = driver.find_elements_by_id("dataDownload")[0]
    button.click()
    finished = False
    while not finished:
        time.sleep(1)
        finished = _is_download_finished(download_folder)

    driver.close()


def _is_download_finished(folder):
    firefox_temp_file = sorted(Path(folder).glob('*.part'))
    chrome_temp_file = sorted(Path(folder).glob('*.crdownload'))
    downloaded_files = sorted(Path(folder).glob('*.*'))
    if (len(firefox_temp_file) == 0) and \
       (len(chrome_temp_file) == 0) and \
       (len(downloaded_files) >= 1):
        return True
    else:
        return False