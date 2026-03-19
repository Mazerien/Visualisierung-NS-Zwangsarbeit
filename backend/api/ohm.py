import sys
import requests

OVERPASS_URL = "https://overpass-api.openhistoricalmap.org/api/interpreter"


def get_city(city_name, year=None):

    # Base query
    if year is None:
        query = f'[out:json][timeout:25];nwr["place"~"city|town|village"]["name"="{city_name}"];out geom;'
    else:
        # Historical filtering based on OHM documentation
        query = f'[out:json][timeout:25];nwr["place"~"city|town|village"]["name"="{city_name}"];out geom;'

    params = {"data": query}

    headers = {
        "User-Agent": "OHM-Python-Script/1.0"
    }

    response = requests.post(
    OVERPASS_URL,
    data={"data": query},
    headers=headers,
    timeout=60
    )   

    # Debug info
    print("Request URL:")
    print(response.url)
    print()

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return

    data = response.json()

    if not data["elements"]:
        print("No results found.")
        return

    for element in data["elements"]:
        tags = element.get("tags", {})

        print("Name:", tags.get("name"))

        if "lat" in element and "lon" in element:
            print("Coordinates:", element["lat"], element["lon"])

        if "start_date" in tags:
            print("Start date:", tags["start_date"])

        if "end_date" in tags:
            print("End date:", tags["end_date"])

        print("-" * 40)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python OHM.py <city>")
        print("python OHM.py <city> <year>")
        sys.exit(1)

    city = sys.argv[1]

    if len(sys.argv) >= 3:
        year = sys.argv[2]
        get_city(city, year)
    else:
        get_city(city)