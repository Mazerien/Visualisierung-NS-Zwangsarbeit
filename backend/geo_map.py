"""
TODO: Docstring
"""
import math
import random
import folium

from geo_cache import get_city_coords
from geojson_cache import get_geojson
from draw_arrow import add_arrow
from draw_circle import add_circle

from api.person_data_cities import get_city_dataset
from folium import Element


# -------------------------
# CACHE
# -------------------------

MAP_CACHE = {}

#2020: "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson",
WORLD_BY_YEAR = {
    1938: "https://raw.githubusercontent.com/aourednik/historical-basemaps/refs/heads/master/geojson/world_1938.geojson",
    1945: "https://raw.githubusercontent.com/aourednik/historical-basemaps/master/geojson/world_1945.geojson",
    2025: "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
}


# -------------------------
# COLORS
# -------------------------

COUNTRY_COLORS = {}

COLOR_ONE = ["Germany", "USSR", "Spain", "United Kingdom", "Turkey", "Hungary"]
COLOR_TWO = ["Italy", "Finland", "Yugoslavia", "Netherlands", "Czechoslovakia",
             "Portugal", "Bulgaria", "Libya"
             ]
COLOR_THREE = ["Poland", "Romania", "Greece", "France", "Norway", "Estonia",
               "Iran", "Syria", "Tunisia"
               ]
COLOR_FOUR = ["Sweden", "Switzerland", "Belgium", "Ireland", "Lithuania", "Algeria"
              ]
COLOR_FIVE = ["Denmark", "Latvia", "Iraq", "Luxembourg", "Armenia", "Albania",
              "Morocco", "Mesopotamia"
              ]

for s in COLOR_ONE:
    COUNTRY_COLORS[s] = "#fffdc1"
for s in COLOR_TWO:
    COUNTRY_COLORS[s] = "#ffcdcd"
for s in COLOR_THREE:
    COUNTRY_COLORS[s] = "#e9f2ae"
for s in COLOR_FOUR:
    COUNTRY_COLORS[s] = "#ffdfaa"
for s in COLOR_FIVE:
    COUNTRY_COLORS[s] = "#eccff2"


# -------------------------
# MAP CLASS
# -------------------------

class OSMGeoMap:
    """
    TODO: Docstring
    """
    def __init__(self, tileset="Esri.WorldPhysical", zoom_level=0, year=1938, arrows=None):
        self.tileset = tileset
        self.zoom_level = zoom_level
        self.year = year
        self.arrows = arrows or []

        url = WORLD_BY_YEAR.get(year, WORLD_BY_YEAR[1938])
        self.geo_json = get_geojson(year, url)


    def get_map(self):
        """
        TODO: Docstring
        """
        cache_key = (self.zoom_level, self.year)

        if cache_key in MAP_CACHE:
            return MAP_CACHE[cache_key]

        # -------------------------
        # LOCATION LOGIC (KEEP)
        # -------------------------

        location = [44, 9]
        zoom_start = 5

        if self.zoom_level == 1:
            location = [48, 9]
            zoom_start = 6
        elif self.zoom_level == 2:
            location = [48.060, 8.536548]
            zoom_start = 15

        # -------------------------
        # CITY DATA (KEEP)
        # -------------------------

        city_counts = get_city_dataset()
        city_marker_data = {}

        for city, count in city_counts.items():
            result = get_city_coords(city)

            if not result or not isinstance(result, dict):
                continue

            coords = result.get("coords")

            if not coords or len(coords) != 2:
                continue

            if isinstance(count, dict):
                count = sum(v for v in count.values() if isinstance(v, (int, float)))

            city_marker_data[city] = {
                "coords": coords,
                "count": int(count)
            }

        # -------------------------
        # ARROWS → RETURN DATA
        # -------------------------

        arrows_data = []

        for start_city, start_country, end_city, end_country, color, width, dash, opacity in self.arrows:
            start_coords = get_city_coords(start_city, country=start_country)
            end_coords = get_city_coords(end_city, country=end_country)

            if start_coords and end_coords:
                arrows_data.append({
                    "start": start_coords,
                    "end": end_coords,
                    "color": color,
                    "width": width,
                    "dash": dash,
                    "opacity": opacity
                })

        result = {
            "countries": self.geo_json,
            "cities": city_marker_data,
            "arrows": arrows_data,
            "view": {
                "center": location,
                "zoom": zoom_start
            }
        }

        MAP_CACHE[cache_key] = result
        return result
