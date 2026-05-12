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
    popup_html=None,
    tooltip_text=None,
):
    """
    Interactive circle with optional popup + tooltip.
    """

    popup = folium.Popup(popup_html, max_width=300) if popup_html else None
    
    folium.CircleMarker(
        location=start,
        radius=max(3, min(size / 20000, 15)),  # scale down
        color=color,
        fill=True,
        fill_opacity=opacity,
        popup=popup,
    ).add_to(m)
