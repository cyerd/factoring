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
import glob
import datetime


company = re.compile(r"^[\s]+.*?")
dubai = re.compile(r"^P.O. Box 961029 Invoice Date [\d,][\d,][\d]*?")
address = re.compile(r"^Fort Worth, Texas  76161-1029.*?")
box = re.compile(r"^.* \d")
street = re.compile(r"^[\d]{3}.*")
streets = re.compile(r"^[\d]{2}\s[A-Z]{1} .*")
Invoice_No = re.compile(r"^Invoice #")
Ref_No = re.compile(r"^Remit To:  Apex Capital Reference #")

pickup = re.compile(r"^Pickup .*, .*")
Drop = re.compile(r"^Dropoff .*, .*")
DriverName = re.compile(r"Driver.*")
TruckNo = re.compile(r"Truck Number.*") 
Amount = re.compile(r"Invoice Total .*")

Inv = namedtuple('Inv', 'DRIVER TRUCKNUMBER SHIP_DATE DELIVER_DATE ORIGIN ORIGIN_STATE ZIPCODE  DESTINATION DEST_STATE ZIP TOTAL_RATE COMPANY INVOICE REFFERENCE')
line_items =[]


def textToCsv():
    # Apex_text_data = open("ExtractedData.txt", "r", encoding="utf-8")
    for Text_path in glob.glob("Output/*.txt", recursive=True):
        spacelesss = re.sub("\s", "", Text_path)
        extensionless = re.sub(".txt", "", spacelesss)
        slashless = re.sub('\W', "_", extensionless )
        shortf = re.sub('Library_', "", slashless )
        opened_file = open(Text_path, "r", encoding="utf-8")
        for line in opened_file:
            if not line.isspace():
                if DriverName.search(line):
                    na1, na2, na3, na4, na5, *Drivers1 = line.split()
                    DriveName =  " ".join(Drivers1)
                    # print(DriveName)
                elif TruckNo.match(line):
                    TruckNumber = line.split()[-1]
                    # print(TruckNumber)
                elif Ref_No.match(line):
                    Refference = line.split()[-1]
                elif Ref_No.match(line):
                    Refference = line.split()[-1]
                elif pickup.match(line):
                    title, *placeName, pickDate = line.split()
                    pickPlace = " ".join(placeName)
                    PickTown, *PickSt = pickPlace.split(",")
                    pickState1 = "".join(PickSt).strip()
                    zipcode1 = pickState1.split()[-1]
                    Pickstate2 = re.sub("\d", "", pickState1)
                    spaceremove1 =re.sub("\s+$", "", Pickstate2)
                    pickState = re.sub("^\s", "", spaceremove1)
                    try:
                        time_object = datetime.datetime.strptime(pickDate, '%m/%d/%Y')
                    except ValueError as e:
                        print('ValueError:', e)    
                elif Drop.match(line):
                    title, *placeName, dropDate = line.split()
                    dropPlace = " ".join(placeName)
                    DropTown, *DropSt = dropPlace.split(",")
                    DropState1 = "".join(DropSt).strip()
                    zipcode2 = (DropState1.split()[-1])
                    Dropstate2 = re.sub("\d", "", DropState1)
                    spaceremove2 =re.sub("\s+$", "", Dropstate2)
                    DropState = re.sub("^\s", "", spaceremove2)

                    try:
                        drop_time = datetime.datetime.strptime(dropDate, '%m/%d/%Y')
                    except ValueError as e:
                        print('ValueError:', e) 
                elif Invoice_No.match(line):
                    Invoice = line.split()[-1]
                elif company.search(line):
                    spaceless =(line.strip())
                    # print(spaceless)
                    if not dubai.search(spaceless) and not address.search(spaceless) and not box.match(spaceless) and not street.match(spaceless) and not streets.match(spaceless):
                        billing = spaceless
                        # print(billing)
                elif Amount.match(line):
                    rateAmount = line.split()[-2]
                    amounts = re.sub("\\$", "", rateAmount)
                    line_items.append(Inv(DriveName,TruckNumber,time_object,drop_time,PickTown,pickState,zipcode1,DropTown,DropState,zipcode2,amounts, billing, Invoice, Refference))
        df = pd.DataFrame(line_items)
        print(df.head)
        df.to_csv(f"CSV/{shortf}.csv", index=False)
textToCsv() 