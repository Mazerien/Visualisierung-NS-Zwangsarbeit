import osmnx as ox
import networkx as nx
import folium
from datetime import datetime

from map_drawer import create_map, add_marker, SCHWENNINGEN, CENTRAL_EUROPE

def get_folium_map():
    """Create a base folium map with a sample marker."""
    m = create_map(location=[50, 15], zoom_start=4, tiles="Esri.WorldPhysical")

    html = """
    <h1>Schwenningen</h1>
    <p><img src="https://www.leo-bw.de/media/labw_wappen/current/generated/fromurl/13957_2010_1030.jpg.tm.png" style="width: 50%"/>
    <ul>
        <li>Dolor Sit Amet</li>
        <li>Lorem Ipsum</li>
    </ul>
    """
    add_marker(m, location=[48, 10], html_content=html, tooltip="Test")

    folium.LayerControl().add_to(m)

    # Build OSMnx graph (roads)
    graph = ox.graph_from_place("Schwenningen, Villingen-Schwenningen, Germany")
    return m, graph

def draw_figure(graph: nx.MultiDiGraph, filename="app/static/images/map.png"):
    """Render and save a static plot of the graph."""
    fig, _ = ox.plot_graph(
        graph,
        node_size=0,
        figsize=(27, 40),
        dpi=100,
        bgcolor="#101813",
        edge_color="#a6a6a6",
        edge_linewidth=0.5,
        edge_alpha=1,
        save=False
    )
    fig.tight_layout(pad=0)
    fig.savefig(filename, dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor())
    print(f"Saved map image to {filename}")

def draw_map_from_place(place="Schwenningen, Villingen-Schwenningen, Germany"):
    graph = ox.graph_from_place(place, retain_all=True, simplify=True, network_type='all')
    draw_figure(graph)