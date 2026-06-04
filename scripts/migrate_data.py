"""Script for the data migration from Excel to Directus collections."""
import datetime as dt
import pandas as pd
from sql_migration import MySQL


class NormalizeData:
    """Helper class for migrating xlsx data by transforming and normalizing data."""
    def replace_string(self, s: str, replacement: dict[str]) -> str:
        """Replaces all given substrings with the given dict."""
        s = s.replace("(", "").replace(")", "")
        for old, new in replacement.items():
            s = s.replace(old, new)
        return s

    def date(self, d: str) -> dt.date:
        """
        Checks if given date is in DD.MM.JJJJ, MM/DD/YYYY, or YYYY-MM-DD format. 
        Returns date object.
        """
        d = str(d).split()[0]
        for frm in ("%d.%m.%Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(d, frm).date()
            except ValueError:
                continue

    def gender(self, g: str) -> chr:
        """Converts gender markers to an international standard."""
        codes = {
            "m/w": "x",
            "m/f": "x",
            "w": "f"
        }
        return self.replace_string(g, codes)

    def country(self, c: str) -> str:
        """Standardizes and cleans country names or codes."""
        if c is None or c == "?":
            return "Unknown"

        codes = {
            "Kroatien": "Croatia",
            "PL": "Poland",
            "NL": "The Netherlands",
            "CZ": "Czechia",
            "FRA": "France",
            "OST": "Soviet Union",
            "BEL": "Belgium",
            "ESP": "Spain",
            "GB": "United Kingdom"
        }
        return self.replace_string(c, codes)

    def place_birth(self, uncorrected: str, corrected: str) -> str:
        """Returns the most accurate data available from two city strings."""
        if corrected and corrected != "?":
            return corrected.title()
        if uncorrected and not corrected:
            return uncorrected.title()
        return "Unknown"

    def age_at_date(self, birth_date: dt.date, target_date: dt.date) -> int:
        """Calculates age at a given date based on birth date."""
        if birth_date is None or target_date is None:
            return None
        age = target_date.year - birth_date.year
        if (target_date.month, target_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

class InsertData:
    """
    Helper class for inserting data into the MySQL database.
    """
    normalize_data = NormalizeData()

    def insert_person(self, row: pd.Series, database: MySQL, is_gefangenenbuch: bool, is_imi_liste: bool):
        """
        Inserts a person from a given DataFrame row into the database.
        Also returns the Person within the DB.
        """
        last_name = row["Nachname (korrigiert)"].title()
        first_name = row["Vorname (korrigiert)"]
        maiden_name = maiden_name=row["Geburtsname"]
        gender = self.normalize_data.gender(row["Geschlecht"])
        birthday = self.normalize_data.date(row["Geburtsdatum"])
        nationality = self.normalize_data.country(row["Nationalität"])
        place_birth = self.normalize_data.place_birth(uncorrected=row["Geburtsort"],
            corrected=row["Geburtsort (aktuell/korrigiert)"])
        place_death = row["Sterbeort"]
        last_place_residence = row["Letzter Wohnort (Land)"]
        marriage = None #TODO
        father = None
        mother = None
        religion = row["Religion"]
        profession = row["Berufsangabe"]

        database.insert_person(last_name, first_name, maiden_name, gender, place_birth,
                               birthday, place_death, nationality, last_place_residence,
                               marriage, father, mother, religion, profession)



def main():
    files = [pd.read_excel(
        "Ostarbeitendenliste.xlsx", usecols="B:V"
    ), pd.read_excel(
        "Gefangenenbuch.xlsx", skiprows=4, usecols="D,F:N,P:T,X:AD,AF,AB:AN,AT"),
        pd.read_excel("IMIs.xlsx", usecols="B:V"
                      )
    ]
    database = MySQL("mysql", "mysql", "localhost", "mysql")
    insert_data = InsertData()


    i = 0
    for file in files:
        for _, row in file.iterrows():
            is_gefangenenbuch = i == 1
            is_imi_liste = i == 1
            insert_data.insert_person(row=row, database=database, is_gefangenenbuch, is_imi_liste)
        i += 1

if __name__ == "__main__":
    main()
