
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


#extract text page by page
apex = open("usa.txt", "w")
path = r"US-State-Abbreviations.pdf"


company = re.compile(r"^[\s]+.*?")
dubai = re.compile(r"^P.O. Box 961029 Invoice Date [\d,][\d,][\d]*?")
address = re.compile(r"^Fort Worth, Texas  76161-1029.*?")
box = re.compile(r"^.* \d")
street = re.compile(r"^[\d]* .*")


pickup = re.compile(r"^Pickup .*, .*")
Drop = re.compile(r"^Dropoff .*, .*")
DriverName = re.compile(r"Driver.*")
TruckNo = re.compile(r"Truck Number.*") 
Amount = re.compile(r"Invoice Total .*")
datas = open("apex22.txt", "r")

Inv = namedtuple('Inv', 'DRIVER TRUCKNUMBER SHIP_DATE DELIVER_DATE CUSTOMER ORIGIN ORIGIN_STATE  DESTINATION DEST_STATE  TOTAL_RATE ')
line_items =[]


def extractText():
    with pdfplumber.open(path) as doc:
        for page in doc.pages:
            dataz = page.extract_text()
            apex.write(str(dataz))

def textToCsv():
    for line in datas:
        if not line.isspace():
            if DriverName.search(line):
                na1, na2, na3, na4, na5, *Drivers1 = line.split()
                DriveName =  " ".join(Drivers1) 
            elif TruckNo.match(line):
                TruckNumber = line.split()[-1]
            elif pickup.match(line):
                title, *placeName, pickDate = line.split()
                pickPlace = " ".join(placeName)
                PickTown, *PickSt = pickPlace.split(",")
                pickState1 = "".join(PickSt).strip()
                pickState = re.sub("\d", "", pickState1)    
            elif Drop.match(line):
                title, *placeName, dropDate = line.split()
                dropPlace = " ".join(placeName)
                DropTown, *DropSt = dropPlace.split(",")
                DropState1 = "".join(DropSt).strip()
                DropState = re.sub("\d", "", DropState1)
            elif company.search(line):
                spaceless =(line.strip())
                if not dubai.search(spaceless) and not address.search(spaceless) and not box.match(spaceless) and not street.match(spaceless):
                    billing = spaceless
            elif Amount.match(line):
                rateAmount = line.split()[-2]
                line_items.append(Inv(DriveName,TruckNumber,pickDate,dropDate,billing,PickTown,pickState,DropTown,DropState,rateAmount ))
                df = pd.DataFrame(line_items)
    # print(df.head)
    # df.to_csv('apx.csv', ",")
# extractText()
# textToCsv()

driverpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
trucknumberpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
pickdatepath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
dropdatepath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input'
customerpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input'
originpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input'
originstatepath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input'
destinationpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input'
destinationstatepath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input'
totalamountpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div[1]/div/div[1]/input'
submitpath = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span'


PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# chrome_options.add_argument("start-maximized")
options.add_argument('--disable-gpu')
url = "https://docs.google.com/forms/d/e/1FAIpQLSccoIzoMK305RH1kRzy062JBrwnc_6dFqMsc7tvT40pAx3k2g/viewform"
datenow ='//*[@id="sh_date_1"]'

def toITS():
    csv_file = open("apx 22-11-2021.csv", "r")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == -1:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                options.add_experimental_option("detach", True)
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                time.sleep(2)
                driverinfo = driver.find_element_by_xpath(driverpath)
                driverinfo.send_keys(row[1])
                truckinfo = driver.find_element_by_xpath(trucknumberpath)
                truckinfo.send_keys(row[2])
                pickdateinfo = driver.find_element_by_xpath(pickdatepath)
                pickdateinfo.send_keys(row[3])
                dropdateinfo = driver.find_element_by_xpath(dropdatepath)
                dropdateinfo.send_keys(row[4])
                customerinfo = driver.find_element_by_xpath(customerpath)
                customerinfo.send_keys(row[5])
                origininfo = driver.find_element_by_xpath(originpath)
                origininfo.send_keys(row[6])
                originstateinfo = driver.find_element_by_xpath(originstatepath)
                originstateinfo.send_keys(row[7])
                destinationinfo = driver.find_element_by_xpath(destinationpath)
                destinationinfo.send_keys(row[8])
                destinatinstateinfo = driver.find_element_by_xpath(destinationstatepath)
                destinatinstateinfo.send_keys(row[9])
                rateinfo = driver.find_element_by_xpath(totalamountpath)
                rateinfo.send_keys(row[10])
                rateinfo = driver.find_element_by_xpath(submitpath)
                rateinfo.click()
                
            line_count += 1
        


# toITS()

def dispatch():
     options.add_experimental_option("detach", True)
     driver = webdriver.Chrome(options=options)
     driver.get(url)
     time.sleep(2)
