"""
This file is called by a Slurm script .sh file
"""
import os
import sys

sys.path.append("../../")
from optimizer.device_topo.intra_node_bandwidth import get_device_bandwidth
from optimizer.model.graph import DeviceGraph

import warnings

warnings.filterwarnings("ignore")


# Function to get a key that includes a specific substring
def get_key_including_substring(d, substring):
    for key in d:
        if substring in key:
            return key
    return None  # Return None if no such key is found


def get_intra_node_topo() -> DeviceGraph:
    G = DeviceGraph()
    bandwidths, devices = get_device_bandwidth()
    for (name, attributes) in devices.items():
        G.add_new_node(name, attributes["memory_limit"])
    for (direction, band) in bandwidths.items():
        if direction == "H2D":
            from_device = get_key_including_substring(G.nodes, "CPU:0")
            to_device = get_key_including_substring(G.nodes, "GPU:0")
        elif direction == "D2H":
            from_device = get_key_including_substring(G.nodes, "GPU:0")
            to_device = get_key_including_substring(G.nodes, "CPU:0")
        else:
            continue
        if not from_device or not to_device:
            raise ValueError("device not found")
        G.update_link_bandwidth(from_device, to_device, band)
    print("INFO ROW: ", os.environ.get("SLURMD_NODENAME"), G.edges.data())
    return G


get_intra_node_topo()
