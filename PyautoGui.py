
from datetime import datetime
from multiprocessing.connection import wait
import re
import pdfplumber
import requests
import pandas as pd
from collections import namedtuple
import fitz  # this is pymupdf
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from time import sleep
import requests
from bs4 import BeautifulSoup
import pyautogui




PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# chrome_options.add_argument("start-maximized")
options.add_argument('--disable-gpu')
url = "https://app.itsdispatch.com/dispatch.php"

options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get(url)
driver.set_window_position(0, 0,)
driver.set_window_size(973,1080)    
driver.find_element(By.ID, "email").send_keys("Abdikamil10@hotmail.com" + Keys.TAB)
driver.find_element(By.ID, "password").send_keys("Abdinasir@21" + Keys.RETURN)
with open('App.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            pyautogui.moveTo(57, 245)
            pyautogui.click()
            sleep(7)
            pyautogui.moveTo(150, 409)
            sleep(2)
            pyautogui.click()
            pyautogui.write("10 ")
            sleep(1)
            pyautogui.moveTo(238, 449)
            sleep(1)
            pyautogui.click()
            pyautogui.write(row[1])
            for i in range(13):
                pyautogui.press('tab')
            pyautogui.write(row[2])
            sleep(1)
            pyautogui.press('tab')
            pyautogui.write(row[5])
            sleep(1)
            pyautogui.press('tab')
            pyautogui.write(row[7])
            sleep(1)
            pyautogui.moveTo(314, 557)
            sleep(1)
            pyautogui.click()
            pyautogui.moveTo(84, 569)
            sleep(1)
            pyautogui.click()
            pyautogui.write(row[9])
            sleep(3)
            pyautogui.moveTo(720,570)
            pyautogui.click()
            sleep(3)
            x1 = int(row[11])
            y1 = int(row[12])
            sleep(2)
            pyautogui.moveTo(x1, y1)
            pyautogui.click()
            sleep(1)
            pyautogui.moveTo(80, 710)
            pyautogui.click()
            pyautogui.write(row[14])
            sleep(3)
            pyautogui.moveTo(720,710)
            pyautogui.click()
            sleep(2)
            x2 = int(row[16])
            y2 = int(row[17])
            pyautogui.moveTo(x2, y2)
            pyautogui.click()
            sleep(1)
            pyautogui.moveTo(890, 866)
            pyautogui.click()
            sleep(5)



