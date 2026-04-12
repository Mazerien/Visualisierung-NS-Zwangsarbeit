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

    def _fetch_ohm_streets(self, bbox):
        """
        Fetch streets from OHM via Overpass API within a bounding box
        bbox = [south, west, north, east]
        """
        overpass_url = "https://overpass-api.openhistoricalmap.org/api/interpreter"

        # Overpass query: get all highways in the bounding box
        query = f"""
        [out:json][timeout:25];
        (
          way["highway"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out body;
        >;
        out skel qt;
        """
        response = requests.post(overpass_url, data=query)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching OHM data:", response.status_code)
            return None

    def _add_ohm_layer(self, m, bbox):
        """Render streets from OHM as Polylines"""
        data = self._fetch_ohm_streets(bbox)
        if not data:
            return

        # Convert Overpass ways to PolyLines
        elements = data.get("elements", [])
        ways = [e for e in elements if e["type"] == "way" and "geometry" in e]

        for way in ways:
            coords = [(point['lat'], point['lon']) for point in way['geometry']]
            highway = way.get('tags', {}).get('highway', '')
            # simple styling: primary roads thick black, residential thin gray
            if highway in ['primary', 'secondary', 'tertiary', 'trunk']:
                color = 'black'
                weight = 3
            else:
                color = 'gray'
                weight = 1
            folium.PolyLine(coords, color=color, weight=weight, opacity=0.7).add_to(m)

    def get_map(self) -> str:
        # Default location
        location = [44, 9]
        zoom_start = 5

        if self.zoom_level == 1:
            location = [48, 9]
            zoom_start = 6
        elif self.zoom_level == 2:
            # Schwenningen: [48.0636961, 8.536548]
            location = [48.060, 8.536548]
            zoom_start = 15

        if self.zoom_level == 2:
            # Base tiles
            m = folium.Map(location=location, zoom_start=zoom_start, tiles="OpenStreetMap")
        else:
            m = folium.Map(location=location, zoom_start=zoom_start, tiles=self.tileset)

        if self.zoom_level < 2:

            def style_function(feature):
                country_name = feature["properties"].get("NAME")
                fill_color = COUNTRY_COLORS.get(
                    country_name,
                    f'#{random.randint(0, 0xFFFFFF):06x}'
                )
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

        elif self.zoom_level == 2:
            # Define bounding box around city (approx ±0.01°)
            lat, lon = location
            bbox = [lat - 0.01, lon - 0.01, lat + 0.01, lon + 0.01]
            self._add_ohm_layer(m, bbox)

        # Arrows
        if self.zoom_level < 2:
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