
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




def extractText():    
    text_output = open("ExtractedData.txt", "w", encoding="utf-8")
    
    for PDF_Path in glob.glob("Library/**/*.pdf", recursive=True):
        filename = PDF_Path
        
        spacelesss = re.sub("\s", "", PDF_Path)
        extensionless = re.sub(".pdf", "", spacelesss)
        slashless = re.sub('\W', "_", extensionless )
        shortf = re.sub('PDFLibrary_', "", slashless )
        Output_pdf = open(f"Output/{shortf}.txt", "w", encoding="utf-8")   
        with pdfplumber.open(PDF_Path) as doc:
            for page in doc.pages:
                dataz = page.extract_text()
                Output_pdf.write(str(dataz))

extractText()