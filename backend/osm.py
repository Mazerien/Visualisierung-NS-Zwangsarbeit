"""
TODO
"""
from enum import Enum
import folium
import requests
import asyncio

class ZoomLevel(Enum):
    MINIMUM = 0
    MEDIUM = 1
    MAXIMUM = 2

zoom_level = {
    ZoomLevel.MINIMUM: {"location": [53, 9], "zoom_start": 5},
    ZoomLevel.MEDIUM: {"location": [48, 9], "zoom_start": 7},
    ZoomLevel.MAXIMUM: {"location": [48, 9], "zoom_start": 9}
}

class OSM:
    """
    An OpenStreetMap map with the given zoom parameters.
    TODO Zoom parameters
    """
    _tileset: str = "Esri.WorldPhysical"
    _geo_json: folium.GeoJson = requests.get("https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json")
    _zoom_level: ZoomLevel

    def __init__(self, tileset: str, zoom_level: ZoomLevel):
        self.tileset = tileset
        self.zoom_level = zoom_level

    @property
    def tileset(self) -> str:
        return self._tileset

    @tileset.setter
    def tileset(self, val: str):
        self._tileset = val

    @property
    def zoom_level(self) -> ZoomLevel:
        return self._zoom_level
    
    @zoom_level.setter
    def zoom_level(self, val: int):
        z = ZoomLevel(int(val))
        self._zoom_level = z
    
    @property
    def geo_json(self) -> folium.GeoJson:
        return self._geo_json
    
    @geo_json.setter
    def geo_json(self, val: str = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"):
        self._geo_json = requests.get(val)

    def get_map(self):
        zoom_start: int = 5
        location: list[float, int] = [53, 9]    # Lat/Lon of central Europe

        match self.zoom_level:
            case ZoomLevel.MINIMUM:
                zoom_start = 5
            case ZoomLevel.MEDIUM:
                zoom_start = 6
            case ZoomLevel.MAXIMUM:
                zoom_start = 16
                location = [48.1, 9]    # Lat/Lon of Schwenningen
            case _:
                zoom_start = 5

        m = folium.Map(tiles=self.tileset, location=location, zoom_start=zoom_start, zoom_control=False, scrollWheelZoom=False, dragging=False)
        #geojson_data = requests.get(
        #    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json").json()
        #folium.GeoJson(geojson_data, name="hello, world").add_to(m)
        #folium.LayerControl().add_to(m)
        return m.get_root()._repr_html_()