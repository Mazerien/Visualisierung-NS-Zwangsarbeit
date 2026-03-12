"""Script for the data migration from Excel to Directus collections."""
import datetime as dt
import json
import numpy as np
import pandas as pd
import requests
from __init__ import URL, ADMIN_TOKEN, AUTH_HEADER


class NormalizeData:
    """Helper class for migrating xlsx data by transforming and normalizing data."""
    def replace_string(s: str, replacement: dict[str]) -> str:
        """Replaces all given substrings with the given dict."""
        s = s.replace("(", "").replace(")", "")
        for old, new in replacement.items():
            s = s.replace(old, new)
        return s

    def date(d: str) -> dt.date:
        """Checks if given date is in DD.MM.JJJJ, MM/DD/YYYY, or YYYY-MM-DD format. Returns date object."""
        d = str(d).split()[0]
        for format in ("%d.%m.%Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(d, format).date()
            except ValueError:
                continue

    def gender(g: str) -> chr:
        """Converts gender markers to an international standard."""
        dict = {
            "m/w": "x",
            "m/f": "x",
            "w": "f"
        }
        return NormalizeData.replace_string(g, dict)

    def country(c: str) -> str:
        """Standardizes and cleans country names or codes."""
        if c is None or c == "?":
            return "Unknown"

        dict = {
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
        return NormalizeData.replace_string(c, dict)

    def place_of_birth(uncorrected: str, corrected: str) -> str:
        """Returns the most accurate data available from two city strings."""
        if corrected and corrected != "?":
            return corrected.title()
        if uncorrected and not corrected:
            return uncorrected.title()
        return "Unknown"

    def age_at_date(birth_date: dt.date, target_date: dt.date) -> int:
        """Calculates age at a given date based on birth date."""
        if birth_date is None or target_date is None:
            return None
        age = target_date.year - birth_date.year
        if (target_date.month, target_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age


class MigrateData:
    """Helper class for inserting data into Directus."""
    file: pd.DataFrame = pd.read_excel(
        "Gefangenenbuch.xlsx", skiprows=4, usecols="D,F:N,P:T,X:AD,AF,AB:AN,AT")
    file = file.replace({np.nan: None})
    # TODO: Refactor this class. This is hell, but it *does* work.

    def migrate():
        """Main function for migrating Excel data into Directus."""
        for _, row in MigrateData.file.iterrows():
            person = MigrateData.person(row)
            company = MigrateData.company(row)
            housing = MigrateData.housing(row)
            tenancy = MigrateData.tenancy(row)
            imprisonment = MigrateData.imprisonment(row)

    def company(row: pd.Series) -> requests.Response:
        """Inserts one or more companies from a given DataFrame row into Directus."""
        companies: list[str] = [row["Unternehmen"], row["Unternehmen2"]]
        companies_corrected: list[str] = []

        # Checks if either Company have a string in the Excel; discards if it is empty or erroneous.
        for c in companies:
            if c is not None and len(c) > 0 and c != "?":
                # TODO: Think of a unified algorithm for correcting these human data insertion errors?
                replacement = {
                    "... Ziegelwerk Mühlacker u.a.": "Ziegelwerk Mühlacker"
                }
                c = NormalizeData.replace_string(c, replacement)
                companies_corrected.append(c)
        if len(companies_corrected) == 0:
            return

        # Checks if either Company is already in the DB. Creates an entry if not.
        companies = []
        for c in companies_corrected:
            req = requests.get(
                f"{URL}/items/Company", params={"filter[Name][_eq]": c}, headers=AUTH_HEADER)
            req = json.loads(req.content)
            if len(req["data"]) == 0:
                print(f"New Company {c} added to Directus.")
                payload = {
                    "Name": c
                }
                req = requests.post(
                    f"{URL}/items/Company", json=payload, headers=AUTH_HEADER)

    def housing(row: pd.Series):
        """Inserts new housing data. If no housing data is given, returns."""
        houses = [
            row["Unterkunft (Adresse Kriegszeit)"], row["Unterkunft2"]]
        houses_corrected = []

        for h in houses:
            if h is not None and len(h) > 0 and h != "?":
                h = h.replace("Wohnsitz unbek.", "")
                houses_corrected.append(h)
        if len(houses_corrected) == 0:
            return

        houses = []
        for h in houses_corrected:
            req = requests.get(
                f"{URL}/items/Housing", params={"filter[Adress][_eq]": h}, headers=AUTH_HEADER)
            req = json.loads(req.content)
            if h and len(req["data"]) == 0:
                print(f"New Housing Adress {h} added to Directus.")
                payload = {
                    "Adress": h,
                    "Type": "Schwenningen"
                }
                req = requests.post(
                    f"{URL}/items/Housing", json=payload, headers=AUTH_HEADER)
    
    def imprisonment(row: pd.Series):
        # TODO
        pass

    def person(row: pd.Series) -> requests.Response:
        """Inserts a person from a given DataFrame row into Directus."""
        # TODO: Check if person already exists in DB. If they do, skips it to avoid duplicate entries.
        # TODO: Maybe fuzzy matching?
        try:
            maiden_name = row["Geburtsname"].title()
        except AttributeError:
            maiden_name = None

        payload = {
            "LastName": row["Nachname (korrigiert)"].title(),
            "FirstName": row["Vorname (korrigiert)"],
            "MaidenName": maiden_name,
            "Gender": NormalizeData.gender(row["Geschlecht"]),
            "DateOfBirth": str(NormalizeData.date(row["Geburtsdatum"])),
            "PlaceOfBirth": NormalizeData.place_of_birth(
                uncorrected=row["Geburt‏sort"], corrected=row["Geburtsort (aktuell/korrigiert)"]),
            "PlaceOfDeath": row["Sterbeort"],
            "Nationality": NormalizeData.country(row["Nationalität"]),
            "LastPlaceOfResidence": row["Letzter Wohnort (Land)"],
            "Marriage": None,   # TODO
            "Father": row["Name Vater"],    # TODO
            "Mother": row["Name Mutter"],   # TODO
            "Religion": row["Religion"],
            "Profession": row["Berufsangabe"]
        }
        return requests.post(f"{URL}/items/Person",
                             json=payload, headers=AUTH_HEADER)
    
    def tenancy(row: pd.Series):
        # TODO
        pass