########################################
# imports
########################################

import networkx as nx
import matplotlib.pyplot as plt
from . import pcapfile 
from . import dns
import os

########################################
# layout
########################################

def draw_func(G, incoming_edges, outgoing_edges):
    
    d = dict(G.degree)
    pos = nx.circular_layout(G)
    node_labels = {node: node for node in G.nodes}

    for node in G.nodes:
        
        # CC IP Geolocation by DB-IP https://db-ip.com

        script_directory = os.path.dirname(os.path.abspath(__file__))
        db_mmdb_path = os.path.join(script_directory, '..', 'database', 'db.mmdb')

        dns_country = dns.DNSCountry(db_mmdb_path)
        result = dns_country.lookup(node)

        if result == node:
            node_labels[node] = f'{node}'
        else:
            node_labels[node] = f'{node} \n {result}' 

        script_directory = os.path.dirname(os.path.abspath(__file__))
        txt_file_path = os.path.join(script_directory, '..', 'database', 'badip.txt')

        with open(txt_file_path, 'r') as file:
            ip_addresses = [line.strip() for line in file]

        for ip in ip_addresses:
            if ip == node:
                node_labels[node] = f'{node} \n {result} \n "Known bad ip"'
            else:
                node_labels[node] = f'{node} \n {result} \n "Not blacklisted"'
                
    # Styling
                
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=[0.5 * v * 300 for v in d.values()])

    nx.draw_networkx_edges(G, pos, edgelist=incoming_edges, edge_color='blue', alpha=0.5, width=2, arrows=True)
    
    nx.draw_networkx_edges(G, pos, edgelist=outgoing_edges, edge_color='blue', alpha=0.5, width=2, arrows=True)
    nx.draw_networkx_labels(G, pos,labels=node_labels, font_size=10, font_family='sans-serif')

    flow_labels = {(v, u): f'{int(d["weight"])/1:} B' for (u, v, d) in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=flow_labels, label_pos=0.3, font_size=5)

########################################
# data
########################################

    capture = pcapfile.capture

    num_nodes = G.number_of_nodes()

    source_ips = {}
    dest_ips = {}
    source_ports = {}
    dest_ports = {}
    protocols = {}
    file_count = 0

########################################
# func
########################################

    for packet in capture:
        if packet.highest_layer in protocols:
            protocols[packet.highest_layer] += 1
        else:
            protocols[packet.highest_layer] = 1

        if 'http' in packet and packet.http.get_field('response_for_uri') is not None:
            file_count += 1

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

