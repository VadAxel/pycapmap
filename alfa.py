import pyshark
import networkx as nx
import matplotlib.pyplot as plt

# Open the pcap file for reading
capture = pyshark.FileCapture('kingen.pcap')

# Initialize dictionaries to keep track of the IP addresses and ports
protocols = {}
file_count = 0
source_ips = {}
dest_ips = {}
source_ports = {}
dest_ports = {}
conversation_lengths = {}

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
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        src_port = None
        dst_port = None
        if 'tcp' in packet:
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
        elif 'udp' in packet:
            src_port = packet.udp.srcport
            dst_port = packet.udp.dstport

        # Calculate the size of the data payload
        payload_size = int(packet.captured_length)

        # Check the direction of the traffic and increment the appropriate entry in the conversation_lengths dictionary
        if (src_ip, dst_ip, src_port, dst_port) in conversation_lengths:
            conversation_lengths[(src_ip, dst_ip, src_port, dst_port)][0] += payload_size
        else:
            conversation_lengths[(src_ip, dst_ip, src_port, dst_port)] = [payload_size, 0]

        if (dst_ip, src_ip, dst_port, src_port) in conversation_lengths:
            conversation_lengths[(dst_ip, src_ip, dst_port, src_port)][1] += payload_size
        else:
            conversation_lengths[(dst_ip, src_ip, dst_port, src_port)] = [0, payload_size]

# Create a directed graph to represent the network traffic
G = nx.DiGraph()

# Add nodes for each unique IP address
for ip in set(list(source_ips.keys()) + list(dest_ips.keys())):
    G.add_node(ip)

# Add edges for each conversation between two hosts
for (src_ip, dst_ip, src_port, dst_port), (outgoing_data, incoming_data) in conversation_lengths.items():
    G.add_edge(src_ip, dst_ip, weight=outgoing_data)
    G.add_edge(dst_ip, src_ip, weight=incoming_data)

# Define incoming and outgoing edges
incoming_edges = []
outgoing_edges = []
for (src_ip, dst_ip, src_port, dst_port), (outgoing_data, incoming_data) in conversation_lengths.items():
    if incoming_data > outgoing_data:
        incoming_edges.append((src_ip, dst_ip))
    else:
        outgoing_edges.append((src_ip, dst_ip))


# Draw the network map
pos = nx.circular_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)
nx.draw_networkx_edges(G, pos, edgelist=outgoing_edges, edge_color='red', alpha=0.5, width=2, arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=incoming_edges, edge_color='blue', alpha=0.5, width=2, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
flow_labels = {(u, v): f'{int(d["weight"])/1:.2f} MB' for (u, v, d) in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=flow_labels, label_pos=0.3, font_size=8)
plt.axis('off')
plt.show()



