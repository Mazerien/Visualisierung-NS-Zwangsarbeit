"""Script for the data migration from Excel to Directus collections."""
import datetime as dt


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
        return chr(NormalizeData.replace_string(g, dict))

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
    pass
