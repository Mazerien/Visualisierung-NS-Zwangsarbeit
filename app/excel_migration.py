"""
Script for the data migration from Excel to the MySQL database.
"""
import pandas as pd
import csv
from database import MySQL

# NOTE: skiprows skips the weird header of the Excel file.
# Should the Excel file change, this probably won't be needed any more.
file: pd.DataFrame = pd.read_excel("app/data/Gefangenenbuch.xlsx", skiprows=4)

# TODO: Clean and normalize Excel data
# TODO: Convert cleaned data into CSV file
# TODO: Insert data into MySQL DB

print(file)
