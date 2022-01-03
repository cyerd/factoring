
import pandas as pd
import numpy as np

main_excel_path = "DUBAI EXPRESS.xlsx"
Drivers_workbook = pd.read_excel(main_excel_path, sheet_name="Driver")
StateAbbr_workbook = pd.read_excel(main_excel_path, sheet_name="ABBR")
DatesCoordinate_Workbook = pd.read_excel(main_excel_path, sheet_name="Dates")
Main_workbook = pd.read_excel(main_excel_path, sheet_name="Main")

merged = pd.merge(Main_workbook, Drivers_workbook[["TRUCKNUMBER", "NameMap"]], on="TRUCKNUMBER", how="left")
print(merged)