########################################
# func
########################################

def main_func(capture, protocols, file_count, conversation_lengths):
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
            elif 'icmp' in packet:
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst

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