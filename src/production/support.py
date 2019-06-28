# -*- coding: utf-8 -*-
import holidays
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pathlib import Path
from pyvirtualdisplay import Display


BASE_PATH_NATIONS = "/HERE/nations/"
BASE_PATH_RESOURCES = "/HERE/resources/"


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
        print ""


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
    display = Display(visible=0, size=(3000, 2000))
    display.start()
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(BASE_PATH_RESOURCES + "chromedriver", chrome_options=options)
    driver.set_window_size(3000, 2000)
    driver.maximize_window()
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

    display.stop()
    try:
        driver.close()
    except WebDriverException:
        pass


def convert_column_to_index(column_name):
    if column_name == "nation_code":
        return 0
    elif column_name == "year":
        return 1
    elif column_name == "day_in_year":
        return 2
    elif column_name == "holiday":
        return 3
    elif column_name == "hour":
        return 4
    elif column_name == "production_pv":
        return 5
    elif column_name == "production_hydro":
        return 6
    elif column_name == "production_biomass":
        return 7
    elif column_name == "production_wind":
        return 8
    elif column_name == "consumption":
        return 9
    elif column_name == "transits":
        return 10
    elif column_name == "price_oil":
        return 11
    elif column_name == "price_gas":
        return 12
    elif column_name == "price_carbon":
        return 13
    elif column_name == "production_fossil_coal_gas":
        return 14
    elif column_name == "production_fossil_gas":
        return 15
    elif column_name == "production_fossil_hard_coal":
        return 16
    elif column_name == "production_fossil_oil":
        return 17
    elif column_name == "production_nuclear":
        return 18
    elif column_name == "production_other":
        return 19
    elif column_name == "production_waste":
        return 20
    elif column_name == "production_lignite":
        return 21
    elif column_name == "production_other_renewable":
        return 22
    elif column_name == "production_other_geothermal":
        return 23
    else:
        return -1


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
