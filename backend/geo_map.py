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


# -------------------------
# CACHE
# -------------------------

MAP_CACHE = {}

WORLD_BY_YEAR = {
    1938: "https://raw.githubusercontent.com/aourednik/historical-basemaps/refs/heads/master/geojson/world_1938.geojson",
    2020: "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson",
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


    def get_map(self) -> str:
        """
        TODO: Docstring
        """
        cache_key = (self.zoom_level, self.year)

        if cache_key in MAP_CACHE:
            print("Using cached map:", cache_key)
            return MAP_CACHE[cache_key]

        print("Generating map:", cache_key)

        # -------------------------
        # BASE LOCATION
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
        # MAP INIT
        # -------------------------

        m = folium.Map(
            location=location,
            zoom_start=zoom_start,
            tiles=self.tileset if self.zoom_level < 2 else "OpenStreetMap",
            zoom_control=False,
            scrollWheelZoom=False,
            dragging=False,
            doubleClickZoom=False,
            box_zoom=False,
            keyboard=False
        )

        # -------------------------
        # COUNTRY LAYER
        # -------------------------

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

        # -------------------------
        # CITY DATA
        # -------------------------

        city_counts = get_city_dataset()
        city_marker_data = {}

        for city, count in city_counts.items():

            result = get_city_coords(city)

            # skip invalid results
            if not result or not isinstance(result, dict):
                continue

            coords = result.get("coords")

            if not coords:
                continue

            if not isinstance(coords, (list, tuple)) or len(coords) != 2:
                continue

            if isinstance(count, dict):
                count = sum(v for v in count.values() if isinstance(v, (int, float)))

            city_marker_data[city] = {
                "coords": coords,
                "count": int(count)
            }

        # -------------------------
        # ARROWS (UNCHANGED)
        # -------------------------

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
                        size=0.5,
                        opacity=opacity,
                        dash=dash
                    )

        # -------------------------
        # CIRCLES (RESTORED COLOR LOGIC)
        # -------------------------

        for city, data in city_marker_data.items():

            # ALWAYS extract safely
            coords = data.get("coords")

            if not coords:
                continue

            # validate structure
            if not isinstance(coords, (list, tuple)):
                continue

            if len(coords) != 2:
                continue

            count = data.get("count", 0)

            if not isinstance(count, (int, float)):
                continue

            popup_html = f"""
            <div style="font-family: Arial; width: 220px;">
                <h4 style="margin-bottom: 5px;">{city}</h4>
                <hr>
                <b>Count:</b> {count}<br>
                <b>Radius:</b> {int(max(5000, math.sqrt(count) * 8000))} m
            </div>
            """

            add_circle(
                m,
                coords,
                color="#3388ff",
                size=max(5000, math.sqrt(count) * 8000),
                opacity=0.8,
                popup_html=popup_html,
                tooltip_text=f"{city} ({count})"
            )

        # -------------------------
        # FINALIZE
        # -------------------------

        folium.LayerControl().add_to(m)

        html = m.get_root()._repr_html_()

        MAP_CACHE[cache_key] = html

        return html
