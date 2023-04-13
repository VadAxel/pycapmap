########################################
# imports
########################################

import pyshark
import networkx as nx
import matplotlib.pyplot as plt
from main_func import *
from draw_func import *
from graph_func import * 

########################################
# config
########################################

capture = pyshark.FileCapture('kingen.pcap')

protocols = {}
file_count = 0
source_ips = {}
dest_ips = {}
source_ports = {}
dest_ports = {}
conversation_lengths = {}

########################################
# main
########################################

main_func(capture, protocols, file_count, conversation_lengths)

########################################
# graph
########################################

G, incoming_edges, outgoing_edges = graph_func(source_ips, dest_ips, conversation_lengths)

########################################
# draw map
########################################

draw_func(G, incoming_edges, outgoing_edges)



