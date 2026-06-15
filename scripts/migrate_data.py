"""Script for the data migration from Excel to Directus collections."""
import datetime as dt
import pandas as pd
from sql_migration import MySQL


class NormalizeData:
    """Helper class for migrating xlsx data by transforming and normalizing data."""

    def replace_string(self, s: str, replacement: dict[str]) -> str:
        """Replaces all given substrings with the given dict."""
        if not isinstance(s, str):
            return
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
            "m/w": "Other",
            "m/f": "Other",
            "w": "Female",
            "m": "Male",
            None: "Other",
            "": "Other"
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

    def insert_person(self, row: pd.Series, database: MySQL,
                      is_gefangenenbuch: bool):
        """
        Inserts a person from a given DataFrame row into the database.
        Also returns the Person within the DB.
        """
        row = row.where(pd.notna(row), other=None)
        try:
            maiden_name = row["Geburtsname"].title()
        except (KeyError, AttributeError, TypeError):
            maiden_name = ""
        try:
            gender = self.normalize_data.gender(row["Geschlecht"])
        except (KeyError, AttributeError, TypeError):
            gender = "Other"
        if is_gefangenenbuch:
            # Is this horrible spaghetti code?
            # Absolutely. But I was told to rewrite it so many times,
            # that I simply lost track.
            # Proceed with caution.
            last_name = row["Nachname (korrigiert)"].title()
            first_name = row["Vorname (korrigiert)"]
            try:
                geburtsort = row["Geburtsort"]
            except KeyError:
                try:
                    geburtsort = row['Geburt']
                except KeyError:
                    geburtsort = ""
            place_birth = geburtsort
            try:
                place_death = row["Sterbeort"].replace("nan", "")
            except AttributeError:
                place_death = None
            nationality = self.normalize_data.country(row["Nationalität"])
            father = None
            mother = None
            marriage = None
            profession = row["Berufsangabe"]
            last_place_residence = row["Letzter Wohnort (Land)"]
            religion = row["Religion"]
        else:
            last_name = row["Nachname"].title()
            if last_name == "Nachname":
                return
            first_name = row["Vorname"].title()
            place_birth = ""
            place_death = ""
            nationality = ""
            father = ""
            mother = ""
            profession = None
            last_place_residence = None
            religion = None
            marriage = None
            # if is_imi_liste:
            #     source = "IMIliste"
            # else:
            #     source = "Ostarbeiterliste"
        birthday = self.normalize_data.date(row["Geburtsdatum"])
        
        try:
            database.insert_person(last_name, first_name, maiden_name, gender, place_birth,
                                   birthday, place_death, nationality, last_place_residence,
                                   marriage, father, mother, religion, profession)
            return database.get_person_by_name(first_name, maiden_name, last_name)[0]
        except Exception as e:
            print(e)
            pass

    def insert_company(self, row: pd.Series, database: MySQL):
        """Inserts into the Company table."""
        companies: list[str] = [row["Unternehmen"], row["Unternehmen2"]]
        companies_corrected: list[str] = []

        # Checks if either Company have a string in the Excel; discards if it is empty or erroneous.
        for c in companies:
            if c is not None and isinstance(c, str) and len(c) > 0 and c != "?":
                replacement = {
                    "... Ziegelwerk Mühlacker u.a.": "Ziegelwerk Mühlacker"
                }
                c = self.normalize_data.replace_string(c, replacement)
                companies_corrected.append(c)
        if len(companies_corrected) == 0:
            return

        # Checks if either Company is already in the DB. Creates an entry if not.
        companies = []
        for c in companies_corrected:
            company = database.get_company_by_name(c)
            if company is not None and len(company) == 0:
                print(f"New Company {c} added to DB.")
                database.insert_company(c)
                companies.append(database.get_company_by_name(c)[0])
        if len(companies) > 0:
            return companies[0]
        return None

    def insert_housing(self, row: pd.Series, database: MySQL):
        """Inserts a house with its respective housing type."""
        housing: list[str] = [
            row["Unterkunft (Adresse Kriegszeit)"], row["Unterkunft2"]]
        housing_corrected: list[str] = []
        for h in housing:
            if h is not None and isinstance(h, str) and len(h) > 0 and h != "?":
                h = h.replace("Wohnsitz unbek.", "")
                housing_corrected.append(h)
        if len(housing_corrected) == 0:
            return

        housing = []
        for h in housing_corrected:
            house = database.get_housing_by_adress(h)
            if isinstance(h, str) and len(house) == 0:
                database.insert_housing(name_place=h, location="Schwenningen")
                house = database.get_housing_by_adress(h)
                print(f"Housing {h} added to DB.")
                housing.append(house)
        return housing

    def insert_employment(self, occupation: str, company_id: tuple, person_id: tuple, database: MySQL):
        """Inserts employment"""
        if company_id is None or person_id is None:
            return
        employment = database.get_employment_by_id(company_id=company_id, person_id=person_id)
        if len(employment) == 0:
            database.insert_employment(occupation=occupation,
                                           company_id=company_id, person_id=person_id)


def main():
    """Do the migration."""
    files = [pd.read_excel("IMIs.xlsx", usecols="B:V"), pd.read_excel(
        "Gefangenenbuch.xlsx", skiprows=4, usecols="D,F:N,P:T,X:AD,AF,AB:AN,AT"),
        pd.read_excel(
        "Ostarbeitendenliste.xlsx", usecols="B:V"
    )
    ]
    database = MySQL("mysql", "mysql", "localhost", "mysql")
    database.drop_tables(reset_db=True)
    insert_data = InsertData()

    i = 0
    for file in files:
        for _, row in file.iterrows():
            row = row.where(pd.notna(row), other=None)
            is_gefangenenbuch = i == 1
            person = insert_data.insert_person(row=row, database=database,
                                      is_gefangenenbuch=is_gefangenenbuch)
            if person and is_gefangenenbuch:
                person_id = person[0]
                company = insert_data.insert_company(row=row, database=database)
                if company:
                    company_id = company[0]
                    insert_data.insert_employment(occupation=row["Berufsangabe"], company_id=company_id, person_id=person_id, database=database)
                insert_data.insert_housing(row=row, database=database)    
        i += 1


if __name__ == "__main__":
    main()
