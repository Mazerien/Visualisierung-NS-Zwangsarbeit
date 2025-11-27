"""
Script for the data migration from Excel to the MySQL database.
"""
import pandas as pd
import numpy as np
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

    def clean_nan():
        """
        TODO: Docstring
        """
        pass


def main():
    """
    TODO: Docstring
    """
    # NOTE: skiprows and usecols attempt to fix the weird header/data structure of the given Excel file.
    # Should the Excel file change, this probably won't be needed any more.
    file: pd.DataFrame = pd.read_excel(
        "app/data/Gefangenenbuch.xlsx", skiprows=4, usecols="F:N,P:R,AD,AF,AK:AN")
    file = file.replace({np.nan: None})

    file = file.head(1)
    file = file.iloc[0]
    # file = file[0]

    # TODO: Clean and normalize Excel data
    # TODO: Convert cleaned data into CSV file
    # TODO: Insert data into MySQL DB

    # print(file)
    # print(file.dtypes)
    # print(file["Nachname"])
    # for item in file:
    #     print(item)
    #     print(type(item))
    #     # print(item)

    #     dict = {
    #         "last_name": item,
    #         "name": item["Vorname"],
    #         "maiden_name": item["Geburtsname"],
    #         "gender": item["Geschlecht"],
    #         "date_of_birth": item["Geburtsdatum"],
    #         "place_of_birth": item["Geburtsort (aktuell/korrigiert)"],
    #         "place_of_death": item["Sterbeort"],
    #         "date_of_death": item["Sterbedatum"],
    #         "nationality": item["Nationalität"],
    #         "last_place_of_residence": item["Letzter Wohnort (Land)"],
    #         "marriage": "Maria",
    #         "father": item["Name Vater"],
    #         "mother": item["Name Mutter"],
    #         "religion": item["Religion"],
    #         "profession": item["Berufsangabe"]
    #     }
    #     for key, value in dict:
    #         if np.isnan(value):
    #             dict[key] = None

#     print(
#     "DEBUG: Inserting person with values:\n"
#     f"  last_name: {file['Nachname'][0]!r} ({type(file['Nachname'][0])})\n"
#     f"  name: {file['Vorname']!r} ({type(file['Vorname'])})\n"
#     f"  maiden_name: {file['Geburtsname']!r} ({type(file['Geburtsname'])})\n"
#     f"  gender: {file['Geschlecht']!r} ({type(file['Geschlecht'])})\n"
#     f"  date_of_birth: {file['Geburtsdatum']!r} ({type(file['Geburtsdatum'])})\n"
#     f"  place_of_birth: {file['Geburtsort (aktuell/korrigiert)']!r} ({type(file['Geburtsort (aktuell/korrigiert)'])})\n"
#     f"  place_of_death: {file['Sterbeort']!r} ({type(file['Sterbeort'])})\n"
#     f"  date_of_death: {file['Sterbedatum']!r} ({type(file['Sterbedatum'])})\n"
#     f"  nationality: {file['Nationalität']!r} ({type(file['Nationalität'])})\n"
#     f"  last_place_of_residence: {file['Letzter Wohnort (Land)']!r} ({type(file['Letzter Wohnort (Land)'])})\n"
#     f"  marriage: {'Maria'!r}\n"
#     f"  father: {file['Name Vater']!r} ({type(file['Name Vater'])})\n"
#     f"  mother: {file['Name Mutter']!r} ({type(file['Name Mutter'])})\n"
#     f"  religion: {file['Religion']!r} ({type(file['Religion'])})\n"
#     f"  profession: {file['Berufsangabe']!r} ({type(file['Berufsangabe'])})"
# )

    load_dotenv()
    SQL_DB = getenv("SQL_DB")
    SQL_USER = getenv("SQL_USER")
    SQL_PASSWORD = getenv("SQL_PASSWORD")
    SQL_HOST = getenv("SQL_HOST")
    database = MySQL(
        user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST, db=SQL_DB
    )
    database.insert_person(last_name=file["Nachname"], name=file["Vorname"], maiden_name=file["Geburtsname"], gender=file["Geschlecht"],
                           date_of_birth=file["Geburtsdatum"], place_of_birth=file[
                               "Geburtsort (aktuell/korrigiert)"], place_of_death=file["Sterbeort"],
                           date_of_death=file["Sterbeort"], nationality=file[
        "Nationalität"], last_place_of_residence=file["Letzter Wohnort (Land)"],
        marriage="Maria", father=file["Name Vater"], mother=file["Name Mutter"], religion=file["Religion"],
        profession=file["Berufsangabe"])


if __name__ == "__main__":
    main()
