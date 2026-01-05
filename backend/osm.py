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


class ZoomLevel(Enum):
    MINIMUM = 0
    MEDIUM = 1
    MAXIMUM = 2

# TODO: Figure out how to do read the GeoJSON to make a Chloropeth map out of it
# country_borders = pd.read_json(
#     requests.get(
#         "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json").text
# )
# print(country_borders)


# def style_function(feature):
#     country_name = feature["properties"]["NAME"]
#     return {
#         "fillColor": country_borders.get(country_name, "gray")
#     }


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
        def style_function(_):
            return {
                "fillColor": f'#{random.randint(0, 0xFFFFFF):06x}',
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.25,
            }

        folium.GeoJson(self.geo_json, name="1938", style_function=style_function).add_to(m)
        folium.LayerControl().add_to(m)

        #self.geo_json = "https://raw.githubusercontent.com/aourednik/historical-basemaps/refs/heads/master/geojson/world_1938.geojson"
        #folium.GeoJson(self.geo_json, name="2025").add_to(m)
        return m.get_root()._repr_html_()
