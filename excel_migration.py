"""
Script for the data migration from Excel to the MySQL database.
"""
import pandas as pd
import numpy as np
import datetime as dt
from app.database import MySQL
from dotenv import load_dotenv
from os import getenv


class NormalizeData:
    """
    Heloer class for migrating xlsx data into MySQL by transforming the data.
    """
    def set_date(d: str) -> dt.date:
        """
        Checks if given date is in MM/DD/YYYY or DD.MM.JJJJ format.
        Returns a date object.
        """
        d = str(d)

        for fmt in ("%d.%m.%Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(d, fmt).date()
            except ValueError:
                continue

    def set_gender(s: str) -> chr:
        """
        TODO: Docstring
        """
        s = s.replace("w", "f")
        s = s.replace("m/w", "x")
        s = s.replace("m/f", "x")
        return s


def main():
    """
    TODO: Docstring
    """
    # NOTE: skiprows and usecols attempt to fix the weird header/data structure of the given Excel file.
    # Should the Excel file change, this probably won't be needed any more.
    file: pd.DataFrame = pd.read_excel(
        "app/data/Gefangenenbuch.xlsx", skiprows=4, usecols="F:N,P:R,AD,AF,AK:AN")
    file = file.replace({np.nan: None})

    # TODO: Clean and normalize Excel data

    load_dotenv()
    SQL_DB = getenv("SQL_DB")
    SQL_USER = getenv("SQL_USER")
    SQL_PASSWORD = getenv("SQL_PASSWORD")
    SQL_HOST = getenv("SQL_HOST")
    database = MySQL(
        user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST, db=SQL_DB
    )
    database.check_tables()

    # TODO: Convert dates
    # TODO: Figure out marriage
    for _, row in file.iterrows():
        gender = NormalizeData.set_gender(row["Geschlecht"])
        birthday = NormalizeData.set_date(row["Geburtsdatum"])

        database.insert_person(last_name=row["Nachname"], name=row["Vorname"], maiden_name=row["Geburtsname"], gender=gender,
                               date_of_birth=birthday, place_of_birth=row[
            "Geburtsort (aktuell/korrigiert)"], place_of_death=row["Sterbeort"],
            date_of_death=row["Sterbeort"], nationality=row[
            "Nationalität"], last_place_of_residence=row["Letzter Wohnort (Land)"],
            marriage="Maria", father=row["Name Vater"], mother=row["Name Mutter"], religion=row["Religion"],
            profession=row["Berufsangabe"])


if __name__ == "__main__":
    main()
