import folium

CENTRAL_EUROPE = [53.0, 9.0]
SCHWENNINGEN = [48.1, 9.0]

def create_map(location=CENTRAL_EUROPE, zoom_start=5, tiles="CartoDB Positron"):
    m = folium.Map(
        location=location,
        zoom_start=zoom_start,
        tiles=tiles,
        zoom_control=True,
        scrollWheelZoom=True,
        dragging=True
    )
    return m

def add_marker(m, location, html_content, tooltip=None):
    iframe = folium.IFrame(html=html_content, width=400, height=200)
    popup = folium.Popup(iframe)
    folium.Marker(location=location, popup=popup, tooltip=tooltip).add_to(m)
    return m