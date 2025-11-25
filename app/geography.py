"""
Right now, it is possible to either render a map or create a dynamic web map of a pre-set place.

"""
import osmnx as ox
import networkx as nx


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
    # TODO: Figure out how to display routes interactively?
    return ox.convert.graph_to_gdfs(graph, nodes=False).explore()


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
