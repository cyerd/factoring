

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

Inv = namedtuple('Inv', 'DRIVER TRUCKNUMBER SHIP_DATE DELIVER_DATE ORIGIN ORIGIN_STATE  DESTINATION DEST_STATE  TOTAL_RATE ')
line_items =[]


def textToCsv():
    Apex_text_data = open("ExtractedData.txt", "r", encoding="utf-8")
    for line in Apex_text_data:
        if not line.isspace():
            if DriverName.search(line):
                na1, na2, na3, na4, na5, *Drivers1 = line.split()
                DriveName =  " ".join(Drivers1)
                print(DriveName)
            elif TruckNo.match(line):
                TruckNumber = line.split()[-1]
                print(TruckNumber)
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
                line_items.append(Inv(DriveName,TruckNumber,pickDate,dropDate,PickTown,pickState,DropTown,DropState,rateAmount ))
    df = pd.DataFrame(line_items)
    print(df.head)
    df.to_csv('apx.csv', ",")
textToCsv()