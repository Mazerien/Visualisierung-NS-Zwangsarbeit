"""
TODO: Docstring
"""
import osmnx as ox

# TODO: Messy, but works.
def draw_map_from_place(place: str="Schwenningen, Villingen-Schwenningen, Germany"):
    """
    TODO: Docstring
    """
    graph = ox.graph_from_place(place,  retain_all=True, simplify = True, network_type='all')
    u = []
    v = []
    key = []
    data = []
    for uu, vv, kkey, ddata in graph.edges(keys=True, data=True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)

    bgcolor = "#101813"
    fig, ax = ox.plot_graph(graph, node_size=0,figsize=(27, 40), 
                            dpi = 300,bgcolor = bgcolor,
                            save = False, edge_color="#a6a6a6",
                            edge_linewidth=0.5, edge_alpha=1)
    fig.tight_layout(pad=0)
    # TODO: Make output more dynamic, maybe dynamically pass drawing to Flask?
    fig.savefig("schwenningen.png", dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False)