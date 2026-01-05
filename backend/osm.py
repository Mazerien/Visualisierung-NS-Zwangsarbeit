"""
TODO
"""
import json
from enum import Enum
import folium
import requests
import pandas as pd
import random

WORLD_1938: str = "https://raw.githubusercontent.com/aourednik/historical-basemaps/refs/heads/master/geojson/world_1938.geojson"
WORLD_2026: str = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"

# TODO: Make this code less bad.
COUNTRY_COLORS = {
}
COLOR_ONE = ["Germany", "USSR", "Spain", "United Kingdom", "Turkey", "Hungary"]
COLOR_TWO = ["Italy", "Finland", "Yugoslavia", "Netherlands",
             "Czechoslovakia", "Portugal", "Bulgaria", "Libya"]
COLOR_THREE = ["Poland", "Romania", "Greece", "France", "Norway",
               "Estonia", "Iran", "Estonia", "Syria (France)", "Tunisia"]
COLOR_FOUR = ["Sweden", "Switzerland", "Belgium",
              "Ireland", "Lithuania", "Algeria (France)"]
COLOR_FIVE = ["Denmark", "Latvia", "Iraq", "Luxembourg",
              "Armenia", "Albania", "Morocco (France)", "Mesopotamia"]
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


class ZoomLevel(Enum):
    MINIMUM = 0
    MEDIUM = 1
    MAXIMUM = 2


class OSM:
    """
    An OpenStreetMap map with the given zoom parameters.
    TODO Zoom parameters
    """
    _tileset: str = "Esri.WorldPhysical"
    _geo_json: folium.GeoJson = requests.get(WORLD_1938)
    _zoom_level: ZoomLevel

    def __init__(self, tileset: str, zoom_level: ZoomLevel, geo_json: str = WORLD_1938):
        self.tileset = tileset
        self.zoom_level = zoom_level
        self.geo_json = geo_json

    @property
    def tileset(self) -> str:
        """The tileset; OSM has many tilesets to use."""
        return self._tileset

    @tileset.setter
    def tileset(self, val: str):
        self._tileset = val

    @property
    def zoom_level(self) -> ZoomLevel:
        """Three zoom levels."""
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, val: int):
        z = ZoomLevel(int(val))
        self._zoom_level = z

    @property
    def geo_json(self) -> folium.GeoJson:
        return self._geo_json

    @geo_json.setter
    def geo_json(self, val: str = WORLD_1938):
        self._geo_json = requests.get(val).json()

    def get_map(self):
        zoom_start: int = 5
        location: list[float, int] = [53, 9]    # Lat/Lon of central Europe

        match self.zoom_level:
            case ZoomLevel.MINIMUM:
                zoom_start = 5
            case ZoomLevel.MEDIUM:
                zoom_start = 6
            case ZoomLevel.MAXIMUM:
                zoom_start = 20
                location = [48.1, 9]    # Lat/Lon of Schwenningen
            case _:
                zoom_start = 5

        m = folium.Map(tiles=self.tileset, location=location, zoom_start=zoom_start,
                       zoom_control=False, scrollWheelZoom=False, dragging=False)

        # TODO: Make this more modular
        # TODO: Add given colours for the countries; not randomized.
        def style_function(feature):
            country = feature["properties"]["NAME"]
            fill_color = f"#5BCEFA"
            color = "black"
            weight = 1
            fill_opacity = 0.75

            if country in COUNTRY_COLORS:
                return {
                    "fillColor": COUNTRY_COLORS[country],
                    "color": color,
                    "weight": weight,
                    "fillOpacity": fill_opacity,
                }
            #if country is not None:
            #    print(country)
            return {
                "fillColor": f'#{random.randint(0, 0xFFFFFF):06x}',
                "color": color,
                "weight": weight,
                "fillOpacity": fill_opacity,
            }

        # tooltip = folium.GeoJsonTooltip(
        #     fields=["NAME"],
        #     aliases=["Country:"],
        #     localize=True,
        #     sticky=True,
        #     labels=True,
        #     style="""
        #     background-color: #F0EFEF;
        #     border: 2px solid black;
        #     border-radius: 3px;
        #     box-shadow: 3px;
        #     """,
        #     max_width=800,
        # )

        # TODO: Properly add country names to the map. Right now the title is weirdly placed.
        # for feature in self.geo_json["features"]:
        #     name = feature["properties"]["NAME"]
        #     if not name == "None" or name is not None:
        #         coords = feature["geometry"]["coordinates"][0][0][0]
        #         folium.Marker(
        #             location=[coords[1], coords[0]],
        #             icon=folium.features.DivIcon(
        #                 # TODO: Make this more modular
        #                 html=f'<div style="font-size: 12pt; color: black; text-shadow: white 0.1em 0.1em 0.1em;">{name}</div>'
        #             )
        #         ).add_to(m)

        # folium.GeoJson(self.geo_json, name="1938", style_function=style_function, tooltip=tooltip).add_to(m)
        folium.GeoJson(self.geo_json, name="1938",
                       style_function=style_function).add_to(m)
        folium.LayerControl().add_to(m)

        return m.get_root()._repr_html_()
