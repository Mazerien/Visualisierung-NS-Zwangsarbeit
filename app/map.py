"""
TODO: Docstring
"""
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# TODO: Messy, but works.
places = ["Schwenningen, Villingen-Schwenningen, Germany"]
G = ox.graph_from_place(places,  retain_all=True, simplify = True, network_type='all')
#G1 = ox.graph_from_place(places, network_type='all', 
#                         simplify=True, retain_all=True, truncate_by_edge=False, 
#                         custom_filter='["natural"~"water"]')

#G2 = ox.graph_from_place(places, dist=15000, dist_type='bbox', network_type='all', 
#                         simplify=True, retain_all=True, truncate_by_edge=False, 
#                         clean_periphery=False, custom_filter='["waterway"~"river"]')
#Gwater = nx.compose(G1, G2)
#G = nx.compose(G1, G)

u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata)    

# List to store colors
roadColors = []
roadWidths = []

for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            linewidth = 0.10
            color = "#a6a6a6" 
            
        elif item["length"] > 100 and item["length"] <= 200:
            linewidth = 0.15
            color = "#676767"
            
        elif item["length"] > 200 and item["length"] <= 400:
            linewidth = 0.25
            color = "#454545"
            
        elif item["length"] > 400 and item["length"] <= 800:
            color = "#d5d5d5"
            linewidth = 0.35
        else:
            color = "#ededed"
            linewidth = 0.45
    # else:
    #color = "#ffffff"
    linewidth = 0.5
            
    roadColors.append(color)
    roadWidths.append(linewidth)
            

# Center of map
latitude = 40.4381311
longitude = -3.8196194



bgcolor = "#101813"

fig, ax = ox.plot_graph(G, node_size=0,figsize=(27, 40), 
                        dpi = 300,bgcolor = bgcolor,
                        save = False, edge_color=roadColors,
                        edge_linewidth=roadWidths, edge_alpha=1)

fig.tight_layout(pad=0)
fig.savefig("schwenningen.png", dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False)