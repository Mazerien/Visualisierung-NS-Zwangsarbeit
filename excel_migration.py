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
    Helper class for migrating xlsx data into MySQL by transforming the data.
    """
    def get_replaced_string(s: str, replacement: dict[str]) -> str:
        """
        Replaces all given substrings with a given dict.
        """
        s = s.replace("(", "").replace(")", "")
        for old, new in replacement.items():
            s = s.replace(old, new)
        return s

    def set_date(d: str) -> dt.date:
        """
        Checks if given date is in YYYY-MM-DD, MM/DD/YYYY, or DD.MM.JJJJ format.
        Returns a date object.
        """
        d = str(d).split()[0]

        for format in ("%d.%m.%Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(d, format).date()
            except ValueError:
                continue

    def set_gender(g: str) -> chr:
        """
        Converts gender markers to an international standard.
        """
        g = g.replace("m/w", "x")
        g = g.replace("m/f", "x")
        g = g.replace("w", "f")
        return g

    def set_country(c: str) -> str:
        """
        Standardizes and cleans country names or codes.
        """
        if c is None or c == "?":
            return "Unknown"

        replacement = {
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
        return NormalizeData.get_replaced_string(c, replacement)

    def set_place_of_birth(uncorrected: str, corrected: str) -> str:
        """
        Returns the most accurate data available from two city strings.
        """
        if corrected and corrected != "?":
            return corrected.title()
        if uncorrected and not corrected:
            return uncorrected.title()
        return "Unknown"

    def set_age_at_date(birth_date: dt.date, target_date: dt.date) -> int:
        """
        Calculates age at a given date based on birth date.
        """
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
    def insert_person(row: pd.Series, database: MySQL):
        """
        Inserts a person from a given DataFrame row into the database.
        Also returns the Person within the DB.
        """
        last_name = row["Nachname (korrigiert)"].title()
        gender = NormalizeData.set_gender(row["Geschlecht"])
        birthday = NormalizeData.set_date(row["Geburtsdatum"])
        nationality = NormalizeData.set_country(row["Nationalität"])
        place_of_birth = NormalizeData.set_place_of_birth(
            uncorrected=row["Geburt‏sort"], corrected=row["Geburtsort (aktuell/korrigiert)"])

        # Checks if person already exists in DB. If they do, skips it to avoid duplicate entries.
        # people: list[tuple] = database.get_person_by_name(
        #    first_name=row["Vorname (korrigiert)"], maiden_name=row["Geburtsname"], last_name=last_name)
        # TODO: Maybe fuzzy matching?
        # if len(people) > 0:
        #    print(people)

        database.insert_person(last_name=last_name, name=row["Vorname (korrigiert)"], maiden_name=row["Geburtsname"], gender=gender,
                               date_of_birth=birthday, place_of_birth=place_of_birth, place_of_death=row[
                                   "Sterbeort"],
                               date_of_death=row["Sterbeort"], nationality=nationality, last_place_of_residence=row[
            "Letzter Wohnort (Land)"],
            marriage="None", father=row["Name Vater"], mother=row["Name Mutter"], religion=row["Religion"],
            profession=row["Berufsangabe"])
        return database.get_person_by_name(first_name=row["Vorname (korrigiert)"], maiden_name=row["Geburtsname"], last_name=last_name)

    def insert_company(row: pd.Series, database: MySQL):
        """
        Inserts one or more companies from a given DataFrame row into the database.
        Also returns the company within the DB.
        """
        companies: list[str] = [row["Unternehmen"], row["Unternehmen2"]]
        companies_corrected: list[str] = []

        # Checks if either Company have a string in the Excel; discards if it is empty or erroneous.
        for c in companies:
            if c is not None and len(c) > 0 and c != "?":
                # TODO: Think of a unified algorithm for correcting these human data insertion errors?
                replacement = {
                    "... Ziegelwerk Mühlacker u.a.": "Ziegelwerk Mühlacker"
                }
                c = NormalizeData.get_replaced_string(c, replacement)
                companies_corrected.append(c)
        if len(companies_corrected) == 0:
            return

        # Checks if either Company is already in the DB. Creates an entry if not.
        companies = []
        for c in companies_corrected:
            company = database.get_company_by_name(c)
            if len(company) == 0:
                print(f"New Company {c} added to DB.")
                database.insert_company(c)
            companies.append(database.get_company_by_name(c)[0])
        return companies

    def insert_employment(name: str, companies: tuple, person: tuple, database: MySQL):
        """
        Inserts employment data from a given DataFrame row into the database.
        If no employment data is given, returns.
        """
        for company in companies:
            employment = database.get_employment_by_id(
                company_id=company[0], person_id=person[0])
            if len(employment) == 0:
                employment = database.insert_employment(
                    name=name, company_id=company[0], person_id=person[0])

    def insert_housing(row: pd.Series, database: MySQL):
        """
        Inserts new housing data.
        If no housing data is given, returns.
        """
        housing: list[str] = [
            row["Unterkunft (Adresse Kriegszeit)"], row["Unterkunft2"]]
        housing_corrected: list[str] = []
        for h in housing:
            if h is not None and len(h) > 0 and h != "?":
                h = h.replace("Wohnsitz unbek.", "")
                housing_corrected.append(h)
        if len(housing_corrected) == 0:
            return

        housing = []
        for h in housing_corrected:
            house = database.get_housing_by_adress(h)
            if h and len(house) == 0:
                database.insert_housing(
                    adress=h, housing_type="Schwenningen")
                house = database.get_housing_by_adress(h)
                print(f"Housing {h} added to DB.")
                housing.append(house)
        return housing

    def insert_tenancy(housing: tuple, person: tuple, start_date: dt.date, end_date: dt.date, database: MySQL):
        """
        Inserts tenancy data linking housing and person with start and end dates.
        If no housing data is given, returns.
        """
        if not housing:
            return
        # TODO: Maybe do pre-processing in another function for the tuples if len(tuple) == 1?
        housing = housing[0][0]
        person = person[0][0]
        database.insert_tenancy(
            housing_id=housing[0], person_id=person, start_date=start_date, end_date=end_date)
        return database.get_tenancy_by_id(housing_id=housing[0], person_id=person)

    def insert_imprisonment(person: int, prisoner_id: int, start_date: dt.date, end_date: dt.date,
                            prisoner_of_war: bool, court_of_law: str, database: MySQL):
        """
        Inserts imprisonment data into the database.
        """
        person = person[0]
        date_of_birth = person[6]
        age = NormalizeData.set_age_at_date(
            birth_date=date_of_birth, target_date=start_date)
        if type(prisoner_id) is not int:
            prisoner_id = None

        database.insert_imprisonment(
            person_id=person[0],
            prisoner_id=prisoner_id,
            start_date=start_date,
            end_date=end_date,
            age_at_imprisonment=age,
            prisoner_of_war=prisoner_of_war,
            court_of_law=court_of_law
        )


def main():
    """
    Main function for migrating Excel data into the MySQL database.
    """
    # NOTE: skiprows and usecols attempt to fix the weird header/data structure of the given Excel file.
    # Should the Excel file change, this probably won't be needed any more.
    file: pd.DataFrame = pd.read_excel(
        "app/data/Gefangenenbuch.xlsx", skiprows=4, usecols="D,F:N,P:T,X:AD,AF,AB:AN,AT")
    file = file.replace({np.nan: None})

    load_dotenv()
    SQL_DB = getenv("SQL_DB")
    SQL_USER = getenv("SQL_USER")
    SQL_PASSWORD = getenv("SQL_PASSWORD")
    SQL_HOST = getenv("SQL_HOST")
    database = MySQL(
        user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST, db=SQL_DB
    )
    database.check_tables()

    # TODO: Figure out marriage for Person
    # dict = {"Person": 0, "Company": 0, "Employment": 0, "Housing": 0, "Tenancy": 0}
    for _, row in file.iterrows():
        person = InsertData.insert_person(row=row, database=database)
        companies = InsertData.insert_company(row=row, database=database)
        housing = InsertData.insert_housing(row=row, database=database)
        tenancy = InsertData.insert_tenancy(
            housing, person, start_date=NormalizeData.set_date(row["Aufenthalt ab"]), end_date=NormalizeData.set_date(row["Aufenthalt bis"]), database=database)

        imprisonment_start_date = NormalizeData.set_date(
            row["Aufenthalt (von)"])
        imprisonment_end_date = NormalizeData.set_date(row["Aufenthalt (bis)"])

        imprisonment = InsertData.insert_imprisonment(
            person=person,
            prisoner_id=row["lfd.Nr."],
            start_date=imprisonment_start_date,
            end_date=imprisonment_end_date,
            prisoner_of_war=row["Kgf./ex-Kgf./DV?"] == "Kgf.",
            court_of_law=row["Gericht"],
            database=database
        )
        if companies is not None:
            # print(
            #    f"Inserted Person {person[0][:4]} with Employment Data at Company/Companies {companies}.")
            InsertData.insert_employment(
                name=row["Berufsangabe"], companies=companies, person=person[0], database=database)
        else:
            # print(f"Inserted Person {person[0][:4]} without Employment Data.")
            pass


if __name__ == "__main__":
    main()
