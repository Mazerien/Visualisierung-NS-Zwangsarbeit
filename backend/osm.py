from enum import Enum
import folium
from map_drawer import create_map, add_marker, SCHWENNINGEN, CENTRAL_EUROPE

# Lat/Ion of either EU or VS.
CENTRAL_EUROPE = [53.0, 9.0]
SCHWENNINGEN = [48.1, 9.0]


class ZoomLevel(Enum):
    MINIMUM = 0
    MEDIUM = 1
    MAXIMUM = 2


class OpenStreetMap:
    _location = CENTRAL_EUROPE
    _zoom_start = 5
    _tileset = "CartoDB Positron"

    def __init__(self, zoom_level: int):
        self.zoom_level = zoom_level

    def render(self) -> str:
        # Create the base map
        m = create_map(location=self._location, zoom_start=self._zoom_start, tiles=self._tileset)

        # Example: Add marker
        html = "<b>Schwenningen</b>"
        add_marker(m, location=SCHWENNINGEN, html_content=html, tooltip="Click me!")

        return m.get_root().render()

    @property
    def zoom_level(self):
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, value):
        from enum import Enum

        class ZoomLevel(Enum):
            MINIMUM = 0
            MEDIUM = 1
            MAXIMUM = 2

        try:
            z = ZoomLevel(int(value))
        except:
            z = ZoomLevel.MINIMUM

        self._zoom_level = z

        match self._zoom_level:
            case ZoomLevel.MINIMUM:
                self._zoom_start = 5
                self._location = CENTRAL_EUROPE
            case ZoomLevel.MEDIUM:
                self._zoom_start = 6
                self._location = CENTRAL_EUROPE
            case ZoomLevel.MAXIMUM:
                self._zoom_start = 20
                self._location = SCHWENNINGEN
