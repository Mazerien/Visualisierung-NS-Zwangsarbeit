"""
Script for the data migration from Excel to the MySQL database.
"""
import pandas as pd
from app.database import MySQL
from datetime import date
from dotenv import load_dotenv
from os import getenv


class NormalizeData:
    """
    TODO: Docstring
    """
    def date_conversion(dt: str) -> date:
        """
        TODO: Docstring
        """
        pass
        return None


def main():
    """
    TODO: Docstring
    """
    # NOTE: skiprows skips the weird header of the Excel file.
    # Should the Excel file change, this probably won't be needed any more.
    file: pd.DataFrame = pd.read_excel(
        "app/data/Gefangenenbuch.xlsx", skiprows=4)

    file = file.head(1)
    #file = file[0]

    # TODO: Clean and normalize Excel data
    # TODO: Convert cleaned data into CSV file
    # TODO: Insert data into MySQL DB

    print(file)
    print(file.dtypes)
    print(file["Nachname"])

    load_dotenv()
    SQL_DB = getenv("SQL_DB")
    SQL_USER = getenv("SQL_USER")
    SQL_PASSWORD = getenv("SQL_PASSWORD")
    SQL_HOST = getenv("SQL_HOST")
    database = MySQL(
        user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST, db=SQL_DB
    )
    database.insert_person(last_name=file["Nachname"][0], name=file["Vorname"], maiden_name=file["Geburtsname"], gender=file["Geschlecht"],
                           date_of_birth=file["Geburtsdatum"], place_of_birth=file["Geburtsort (aktuell/korrigiert)"], place_of_death=file["Sterbeort"],
                           date_of_death=file["Sterbeort"], nationality=file[
                               "Nationalität"], last_place_of_residence=file["Letzter Wohnort (Land)"],
                           marriage="Maria", father=file["Name Vater"], mother=file["Name Mutter"], religion=file["Religion"],
                           profession=file["Berufsangabe"])


if __name__ == "__main__":
    main()
