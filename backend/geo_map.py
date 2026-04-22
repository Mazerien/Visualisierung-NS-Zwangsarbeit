# geo_map.py
import folium
import requests
import random
import math
from folium.plugins import PolyLineTextPath
from geo_cache import get_city_coords
from geojson_cache import get_geojson
from draw_arrow import add_arrow
from draw_circle import add_circle
from api.person_data import get_nationality_counts

MAP_CACHE = {}

WORLD_BY_YEAR = {
    1938: "https://raw.githubusercontent.com/aourednik/historical-basemaps/refs/heads/master/geojson/world_1938.geojson",
    2020: "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson",
    2025: "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
}

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
    def __init__(self, tileset="Esri.WorldPhysical", zoom_level=0, year=1938, arrows=None):
        self.tileset = tileset
        self.zoom_level = zoom_level
        self.year = year
        url = WORLD_BY_YEAR.get(year, WORLD_BY_YEAR[1938])
        self.geo_json = get_geojson(year, url)
        self.arrows = arrows or []

    def _fetch_ohm_streets(self, bbox):
        """
        Fetch streets from OHM via Overpass API within a bounding box
        bbox = [south, west, north, east]
        """
        overpass_url = "https://overpass-api.openhistoricalmap.org/api/interpreter"

        # Overpass query: get all highways in the bounding box
        query = f"""
        [out:json][timeout:25][date:"{self.year}-01-01T00:00:00Z"];
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

        cache_key = (self.zoom_level, self.year)

        if cache_key in MAP_CACHE:
            print(" Using cached map:", cache_key)
            return MAP_CACHE[cache_key]

        print(" Generating map:", cache_key)
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
            m = folium.Map(
                location=location, 
                zoom_start=zoom_start, 
                tiles="OpenStreetMap",zoom_control=False,
                scrollWheelZoom=False,
                dragging=False,
                doubleClickZoom=False,
                box_zoom=False,
                keyboard=False)
        else:
            m = folium.Map(
                location=location, 
                zoom_start=zoom_start, 
                tiles=self.tileset,zoom_control=False,
                scrollWheelZoom=False,
                dragging=False,
                doubleClickZoom=False,
                box_zoom=False,
                keyboard=False)

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
                name=f"Countries {self.year}",
                style_function=style_function,
                tooltip=tooltip
            ).add_to(m)

        elif self.zoom_level == 2:
            # Define bounding box around city (approx ±0.01°)
            lat, lon = location
            bbox = [lat - 0.01, lon - 0.01, lat + 0.01, lon + 0.01]
            # self._add_ohm_layer(m, bbox)

        # Arrows
        if self.zoom_level < 2:
            persons = get_nationality_counts()
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
                        size=0.5,
                        opacity=opacity,
                        dash=dash
                    )
                    people_count = persons.get(start_city, 0)
                    add_circle(
                        m,
                        start_coords,
                        color,
                        size = max(10000, math.sqrt(people_count) * 10000),
                        opacity=0.8,
                    )

        folium.LayerControl().add_to(m)

        html = m.get_root()._repr_html_()

        MAP_CACHE[cache_key] = html

        return html