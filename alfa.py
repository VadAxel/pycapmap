import pyshark
import networkx as nx
import matplotlib.pyplot as plt
from termcolor import colored

# Open the pcap file for reading
capture = pyshark.FileCapture('shark1.pcap', display_filter='http or smb')

# Initialize dictionaries to keep track of the IP addresses and ports
source_ips = {}
dest_ips = {}
source_ports = {}
dest_ports = {}
protocols = {}
file_count = 0

# Create an empty graph to store the network map
G = nx.Graph()

# Loop through the packets in the capture file
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

        # Add an edge to the graph to represent the data flow
        G.add_edge(packet.ip.src, packet.ip.dst, weight=packet.length)

# Print the analysis results with colors
print(colored('Protocol Counts:', 'green'))
for protocol, count in protocols.items():
    print(colored(f'{protocol}: {count}', 'yellow'))

print(colored('\nIP Address Counts:', 'green'))
print(colored('Source IPs:', 'yellow'))
for ip, count in source_ips.items():
    print(colored(f'{ip}: {count}', 'cyan'))

print(colored('Destination IPs:', 'yellow'))
for ip, count in dest_ips.items():
    print(colored(f'{ip}: {count}', 'cyan'))

print(colored('\nPort Counts:', 'green'))
print(colored('Source Ports:', 'yellow'))
for port, count in source_ports.items():
    print(colored(f'{port}: {count}', 'magenta'))

print(colored('Destination Ports:', 'yellow'))
for port, count in dest_ports.items():
    print(colored(f'{port}: {count}', 'magenta'))

print(colored(f'\nNumber of Files Transferred: {file_count}', 'green'))
talking_edges = [(u, v) for u, v, d in G.edges(data=True)]
# Draw the network map
pos = nx.spring_layout(G, k=8, seed=42)
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)
nx.draw_networkx_edges(G, pos, edgelist=talking_edges, edge_color='black', alpha=0.5, width=2)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
flow_labels = {(u, v): f'{int(d["weight"])/1000000:.2f} MB' for (u, v, d) in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=flow_labels, label_pos=0.3, font_size=8)
plt.axis('off')
plt.show()
