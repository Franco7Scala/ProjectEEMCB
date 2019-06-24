from pyvirtualdisplay import Display

from selenium import webdriver
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





display = Display(visible=0, size=(2000, 600))
display.start()





url = "https://www.macrotrends.net/1369/crude-oil-price-history-chart"
download_folder = "/Users/francesco/Desktop/Cose da Sistemare/test_p/raw_data"



options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome("/Users/francesco/Desktop/Cose da Sistemare/test_p/resources/chromedriver", chrome_options=options)
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
    finished = is_download_finished(download_folder)



display.stop()
driver.close()