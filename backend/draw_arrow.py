# arrows.py
import folium
import math

def add_arrow(
    m,
    start,
    end,
    color="red",
    weight=3,
    size=0.5,
    opacity=0.8,
    dash=None
):
    """
    Draw a line with an arrow from start to end on a folium map.
    start and end are [lat, lon] lists.
    """
    # Main line
    folium.PolyLine(
        locations=[start, end],
        color=color,
        weight=weight,
        opacity=opacity,
        dash_array=dash
    ).add_to(m)

    # Arrowhead
    lat1, lon1 = start
    lat2, lon2 = end
    angle = math.atan2(lat2 - lat1, lon2 - lon1)
    angle1 = angle + math.pi / 8
    angle2 = angle - math.pi / 8

    arrow1 = [lat2 - size * math.sin(angle1), lon2 - size * math.cos(angle1)]
    arrow2 = [lat2 - size * math.sin(angle2), lon2 - size * math.cos(angle2)]

    folium.PolyLine(locations=[arrow1, [lat2, lon2]], color=color, weight=weight, opacity=opacity).add_to(m)
    folium.PolyLine(locations=[arrow2, [lat2, lon2]], color=color, weight=weight, opacity=opacity).add_to(m)