
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




def extractText():
    PDF_Path = "document.pdf"
    text_output = open("ExtractedData.txt", "w", encoding="utf-8")
    with pdfplumber.open(PDF_Path) as doc:
        for page in doc.pages:
            dataz = page.extract_text()
            text_output.write(str(dataz))

extractText()