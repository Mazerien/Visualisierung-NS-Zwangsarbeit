# geo_map.py
import folium
import requests
import random
import math
from folium.plugins import PolyLineTextPath
from geo_cache import get_city_coords
from draw_arrow import add_arrow

WORLD_1938 = "https://raw.githubusercontent.com/aourednik/historical-basemaps/refs/heads/master/geojson/world_1938.geojson"

COUNTRY_COLORS = {}
COLOR_ONE = ["Germany", "USSR", "Spain", "United Kingdom", "Turkey", "Hungary"]
COLOR_TWO = ["Italy", "Finland", "Yugoslavia", "Netherlands", "Czechoslovakia", "Portugal", "Bulgaria", "Libya"]
COLOR_THREE = ["Poland", "Romania", "Greece", "France", "Norway", "Estonia", "Iran", "Syria", "Tunisia"]
COLOR_FOUR = ["Sweden", "Switzerland", "Belgium", "Ireland", "Lithuania", "Algeria"]
COLOR_FIVE = ["Denmark", "Latvia", "Iraq", "Luxembourg", "Armenia", "Albania", "Morocco", "Mesopotamia"]

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


class OSMGeoMap:
    def __init__(self, tileset="Esri.WorldPhysical", zoom_level=0, geo_json_url=WORLD_1938, arrows=None):
        self.tileset = tileset
        self.geo_json = requests.get(geo_json_url).json()
        self.zoom_level = zoom_level
        self.arrows = arrows or []

    def get_map(self) -> str:
        location = [53, 9]
        zoom_start = 5
        if self.zoom_level == 1:
            zoom_start = 6
        elif self.zoom_level == 2:
            zoom_start = 20
            location = [48.1, 9]

        m = folium.Map(
            tiles=self.tileset,
            location=location,
            zoom_start=zoom_start,
            zoom_control=True,
            scrollWheelZoom=True,
            dragging=True
        )

        def style_function(feature):
            country_name = feature["properties"].get("NAME")
            fill_color = COUNTRY_COLORS.get(country_name, f'#{random.randint(0, 0xFFFFFF):06x}')
            return {
                "fillColor": fill_color,
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            }

        tooltip = folium.GeoJsonTooltip(
            fields=["NAME"],
            aliases=["Country:"],
            localize=True,
            sticky=True,
            labels=True
        )

        folium.GeoJson(
            self.geo_json,
            name="Countries 1938",
            style_function=style_function,
            tooltip=tooltip
        ).add_to(m)

        # Add arrows using the imported function
        for start_city, start_country, end_city, end_country, color, width, dash, opacity in self.arrows:
            start_coords = get_city_coords(start_city, country=start_country)
            end_coords = get_city_coords(end_city, country=end_country)
            if start_coords and end_coords:
                add_arrow(
                    m,
                    start_coords,
                    end_coords,
                    color=color,
                    weight=width,
                    arrow_size=0.5,
                    opacity=opacity,
                    dash=dash
                )

        folium.LayerControl().add_to(m)
        return m.get_root()._repr_html_()