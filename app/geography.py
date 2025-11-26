"""
Right now, it is possible to either render a map or create a dynamic web map of a pre-set place.

"""
import osmnx as ox
import networkx as nx


from folium.plugins import VectorGridProtobuf
import folium
from datetime import datetime


def get_folium_map():
    """
    TODO: Docstring
    """
    pass
    # NOTE: This is VERY WIP!
    # Convert date to decimal year
    d = datetime(1945, 4, 14)
    next_new_year = datetime(d.year + 1, 1, 1)
    last_new_year = datetime(d.year, 1, 1)
    year_len = next_new_year.toordinal() - last_new_year.toordinal()
    dec_date = int(d.year) + (d.toordinal() - last_new_year.toordinal()) / year_len
    print(dec_date)

    options = f'''{{
        "vectorTileLayerStyles": {{
            "land_ohm_lines": function(f) {{
                if ((!f.start_decdate || f.start_decdate <= {dec_date}) && (!f.end_decdate || f.end_decdate >= {dec_date})) {{
                    return {{
                        "weight": 1,
                        "fillColor": "pink",
                        "color": "pink",
                        "fillOpacity": 0.2,
                        "opacity": 0.4
                    }};
                }}
            }}
        }}
    }}'''

    m = folium.Map(tiles="Esri.WorldPhysical", location=[50, 15], zoom_start=4, attr="OpenHistoricalMap")
    #url = "https://vtiles.openhistoricalmap.org/maps/osm/{z}/{x}/{y}.pbf"
    
    html=f"""
        <h1> Schwenningen </h1>
        <p><img src="https://www.leo-bw.de/media/labw_wappen/current/generated/fromurl/13957_2010_1030.jpg.tm.png" style="width: 50%"/> 
        <p>Lorem Ipsum:
        <ul>
            <li>Dolor Sit Amet</li>
            <li>Lorem Ipsum</li>
        </ul>
        </p>
        """
    iframe = folium.IFrame(html=html, width=400, height=200)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(
        location=[48, 10],
        popup=popup,
        tooltip="Test"
    ).add_to(m)

    graph = ox.graph_from_place("Schwenningen, Villingen-Schwenningen, Germany")
    folium.LayerControl().add_to(m)
    #VectorGridProtobuf("folium_layer_name").add_to(m)
    return m


def get_place_features(place: str = "Schwenningen, Villingen-Schwenningen, Germany"):
    """
    TODO: Docstring
    """
    return ox.features_from_place(place, tags={"tourism": ["museum"]})


def web_map(place: str = "Schwenningen, Villingen-Schwenningen, Germany"):
    """
    Returns a web map of a place.
    It can be turned into an iframe of an HTML template.
    """
    graph = ox.graph.graph_from_place(place)
    #ox.settings.nominatim_url = 
    #graph = ox.features_from_xml("app/sample.xml")
    # TODO: Figure out how to display routes interactively?
    #return ox.convert.graph_to_gdfs(graph, nodes=False).explore()
    return graph.explore(attr="© OpenHistoricalMap contributors")


def draw_map_from_place(place: str = "Schwenningen, Villingen-Schwenningen, Germany"):
    """
    Renders a static map of a place and saves it.
    """
    graph: nx.MultiDiGraph = ox.graph_from_place(
        place,  retain_all=True, simplify=True, network_type='all')
    draw_figure(graph)


def draw_figure(graph: nx.MultiDiGraph):
    """
    TODO: Docstring
    """
    u = []
    v = []
    key = []
    data = []
    graph = nx.MultiDiGraph(graph)
    for uu, vv, kkey, ddata in graph.edges(keys=True, data=True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)
        bgcolor = "#101813"
    fig, _ = ox.plot_graph(graph, node_size=0, figsize=(27, 40),
                           dpi=100, bgcolor=bgcolor,
                           save=False, edge_color="#a6a6a6",
                           edge_linewidth=0.5, edge_alpha=1)
    fig.tight_layout(pad=0)
    # TODO: Make output more dynamic, maybe dynamically pass drawing to Flask instead of saving?
    print("Image made. Saving...")
    fig.savefig("app/static/images/map.png", dpi=300, bbox_inches='tight',
                format="png", facecolor=fig.get_facecolor(), transparent=False)
