import pyshark

# Path to your PCAP file
pcap_file = "shark.pcapng"

# Create a dictionary to store statistics
statistics = {}

# Open the PCAP file with pyshark
cap = pyshark.FileCapture(pcap_file)

# Loop through each packet in the PCAP file
for packet in cap:

    # Extract source and destination IP addresses
    src_ip = packet.ip.src
    dst_ip = packet.ip.dst

    # Extract source and destination ports
    src_port = packet[packet.transport_layer].srcport
    dst_port = packet[packet.transport_layer].dstport

    # Extract protocol name
    protocol = packet.transport_layer

    # Extract file name if the packet contains a file
    if 'http' in packet:
        if 'file_data' in packet.http:
            file_name = packet.http.file_data.get('filename', '')
            if file_name:
                if file_name in statistics:
                    statistics[file_name] += 1
                else:
                    statistics[file_name] = 1

    # Update statistics for IPs, ports, and protocols
    if src_ip in statistics:
        statistics[src_ip]['outgoing'] += 1
        statistics[src_ip]['protocols'][protocol] += 1
        statistics[src_ip]['ports'][src_port] += 1
    else:
        statistics[src_ip] = {'outgoing': 1, 'incoming': 0, 'protocols': {protocol: 1}, 'ports': {src_port: 1}}

    if dst_ip in statistics:
        statistics[dst_ip]['incoming'] += 1
        statistics[dst_ip]['protocols'][protocol] += 1
        statistics[dst_ip]['ports'][dst_port] += 1
    else:
        statistics[dst_ip] = {'outgoing': 0, 'incoming': 1, 'protocols': {protocol: 1}, 'ports': {dst_port: 1}}

# Print statistics for IPs, ports, and protocols
print("\nStatistics for IPs:\n")
for ip, data in statistics.items():
    print(f"IP: {ip}")
    print(f"\tIncoming packets: {data['incoming']}")
    print(f"\tOutgoing packets: {data['outgoing']}")
    print(f"\tProtocols: {data['protocols']}")
    print(f"\tPorts: {data['ports']}")

print("\nStatistics for Files:\n")
for file, count in statistics.items():
    print(f"File: {file}, Count: {count}")
