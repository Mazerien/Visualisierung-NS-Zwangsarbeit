"""
TODO: Docstring
"""
import folium

def add_circle(
    m,
    start,
    color,
    size=0.5,
    opacity=0.8,
):
    """
    Draw a line with an arrow from start to end on a folium map.
    start and end are [lat, lon] lists.
    """
    # Main line
    folium.Circle(
        location= start,
        radius= size,  # meters
        color= color,
        fill= True,
        fill_opacity= opacity
    ).add_to(m)
