"""
TODO: Docstring
"""
from enum import Enum
import folium

# Lat/Ion of either EU or VS.
CENTRAL_EUROPE = [53.0, 9.0]
SCHWENNINGEN = [48.1, 9.0]


class ZoomLevel(Enum):
    """
    TODO: Docstring
    """
    MINIMUM = 0
    MEDIUM = 1
    MAXIMUM = 2


class OpenStreetMap:
    """
    An OpenStreetMap map with the given zoom parameters.
    """
    _location = CENTRAL_EUROPE
    _tileset = "Esri.WorldPhysical"
    _zoom_level = ZoomLevel.MINIMUM
    _zoom_start = 5

    def __init__(self, zoom_level: ZoomLevel):
        self.zoom_level = zoom_level

    def __str__(self) -> str:
        m = folium.Map(
            tiles=self._tileset,
            location=self._location,
            zoom_start=self._zoom_start,
            zoom_control=False,
            scrollWheelZoom=False,
            dragging=False
        )
        return m.get_root()._repr_html_()

    @property
    def zoom_level(self) -> ZoomLevel:
        """
        TODO: Docstring
        """
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, i: int):
        """
        Sets the zoom level as well as the zoom start and location in one.
        """
        try:
            z = ZoomLevel(int(i))
        except TypeError:
            z = 0
        self._zoom_level = z

        match self.zoom_level:
            case ZoomLevel.MINIMUM:
                self._zoom_start = 5
            case ZoomLevel.MEDIUM:
                self._zoom_start = 6
            case ZoomLevel.MAXIMUM:
                self._zoom_start = 20
        self._location = SCHWENNINGEN if self.zoom_level == ZoomLevel.MAXIMUM else CENTRAL_EUROPE
