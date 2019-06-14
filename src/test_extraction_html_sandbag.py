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



url = "https://sandbag.org.uk/carbon-price-viewer/"
download_folder = "/Users/francesco/Desktop/Cose da Sistemare/test_p/raw_data"



options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome("/Users/francesco/Desktop/Cose da Sistemare/test_p/chromedriver", chrome_options=options)
driver.get(url)


iframe = driver.find_elements_by_xpath('//iframe')[0]
driver.switch_to.frame(iframe)

driver.execute_script("document.getElementsByClassName('highcharts-contextmenu')[0].style.display = 'block';")


#driver.execute_script("(document.getElementsByClassName('highcharts-contextmenu')[0]).style.display = 'block';")

time.sleep(3)

print len(driver.find_elements_by_xpath("//div"))

#//*[contains(@class, 'highcharts-button')







"""
lined_button = driver.find_elements_by_xpath("//*[name()='svg']//*[name()='g']")[23]
lined_button.click()

finished = False
while not finished:
    time.sleep(1)
    finished = is_download_finished(download_folder)

#driver.close()



lined_button = driver.find_elements_by_xpath("//*[name()='svg']/*[name()='g']")[13]
lined_button.click()

buttons = driver.find_elements_by_class_name("highcharts-menu-item")

print len(buttons)

buttons[5].click()




"""