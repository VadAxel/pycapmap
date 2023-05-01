########################################
# imports
########################################

import networkx as nx
import matplotlib.pyplot as plt
import pyshark
from . import pcapfile
########################################
# layout
########################################

def draw_func(G, incoming_edges, outgoing_edges):
    d = dict(G.degree)
    pos = nx.cirucular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', nodelist=d.keys(), node_size=[0.5 * v * 300 for v in d.values()])
    nx.draw_networkx_edges(G, pos, edgelist=outgoing_edges, edge_color='red', alpha=0.5, width=2, arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=incoming_edges, edge_color='blue', alpha=0.5, width=2, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    flow_labels = {(u, v): f'{int(d["weight"])/1:.2f} B' for (u, v, d) in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=flow_labels, label_pos=0.3, font_size=8)
########################################
# data
########################################

    num_nodes = G.number_of_nodes()

    num_edges = G.number_of_edges()  

    source_ips = {}
    dest_ips = {}
    source_ports = {}
    dest_ports = {}
    protocols = {}
    file_count = 0

    capture = pcapfile.capture


########################################
# func
########################################

    for packet in capture:
        # Increment the count for the protocol used in this packet
        if packet.highest_layer in protocols:
            protocols[packet.highest_layer] += 1
        else:
            protocols[packet.highest_layer] = 1

        # Check if this packet has a file attached to it
        if 'http' in packet and packet.http.get_field('response_for_uri') is not None:
            # Increment the file count
            file_count += 1

        # Increment the count for the source and destination IP addresses and ports
        if 'ip' in packet:
            if packet.ip.src in source_ips:
                source_ips[packet.ip.src] += 1
            else:
                source_ips[packet.ip.src] = 1

            if packet.ip.dst in dest_ips:
                dest_ips[packet.ip.dst] += 1
            else:
                dest_ips[packet.ip.dst] = 1

        if 'tcp' in packet:
            if packet.tcp.srcport:
                if packet.tcp.srcport in source_ports:
                    source_ports[packet.tcp.srcport] += 1
                else:
                    source_ports[packet.tcp.srcport] = 1

            if packet.tcp.dstport:
                if packet.tcp.dstport in dest_ports:
                    dest_ports[packet.tcp.dstport] += 1
                else:
                    dest_ports[packet.tcp.dstport] = 1

########################################
# results
########################################

    result_string = ""
    for protocol, count in protocols.items():
        result_string += f'{protocol}: {count}\n'

    http = ((f'\nNumber of http files Transferred: {file_count}'))

    stats = f"Nodes: {num_nodes}\n{http}\n\nProtocols:\n\n{result_string}"

    plt.text(-1, 1, stats, fontsize=8)
    
    plt.axis('off')
    plt.show()
