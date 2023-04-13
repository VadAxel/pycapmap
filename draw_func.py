########################################
# imports
########################################

import networkx as nx
import matplotlib.pyplot as plt

########################################
# func
########################################

def draw_func(G, incoming_edges, outgoing_edges):
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)
    nx.draw_networkx_edges(G, pos, edgelist=outgoing_edges, edge_color='red', alpha=0.5, width=2, arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=incoming_edges, edge_color='blue', alpha=0.5, width=2, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    flow_labels = {(u, v): f'{int(d["weight"])/1:.2f} MB' for (u, v, d) in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=flow_labels, label_pos=0.3, font_size=8)
    plt.axis('off')
    plt.show()