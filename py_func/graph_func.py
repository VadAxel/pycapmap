########################################
# imports
########################################

import networkx as nx

########################################
# func
########################################

def graph_func(source_ips, dest_ips, conversation_lengths):
    G = nx.DiGraph()

# Add nodes for each unique IP address
    for ip in set(list(source_ips.keys()) + list(dest_ips.keys())):
        G.add_node(ip)

    incoming_edges = []
    outgoing_edges = []
    for (src_ip, dst_ip, src_port, dst_port), (outgoing_data, incoming_data) in conversation_lengths.items():
        G.add_edge(src_ip, dst_ip, weight=outgoing_data)
        G.add_edge(dst_ip, src_ip, weight=incoming_data)
        if incoming_data > outgoing_data:
            incoming_edges.append((src_ip, dst_ip))
        else:
            outgoing_edges.append((src_ip, dst_ip))
    return G,incoming_edges,outgoing_edges
