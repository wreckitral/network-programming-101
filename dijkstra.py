import sys
import json
import math  # If you want to use math.inf for infinity
from netfuncs import find_router_for_ip, ips_same_subnet

def get_closest_unvisited_node(unvisited, distances):
    min_dist = float('inf')
    closest_node = None

    for node in unvisited:
        if distances[node] <= min_dist:
            min_dist = distances[node]
            closest_node = node

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    start_router = find_router_for_ip(routers, src_ip)
    end_router = find_router_for_ip(routers, dest_ip)

    if not start_router or not end_router:
        return []

    if start_router == end_router:
        return []

    distances = {}
    previous_nodes = {}
    unvisited = []

    for router_ip in routers:
        distances[router_ip] = float('inf')
        previous_nodes[router_ip] = None
        unvisited.append(router_ip)

    distances[start_router] = 0

    while len(unvisited) > 0:
        min_dist = float('inf')
        current_node = None

        for node in unvisited:
            if distances[node] < min_dist:
                min_dist = distances[node]
                current_node = node

        if current_node is None:
            break

        if current_node == end_router:
            break

        unvisited.remove(current_node)

        connections = routers[current_node].get("connections", {})

        for neighbor_ip, neighbor_info in connections.items():
            if neighbor_ip in unvisited:
                weight = neighbor_info["ad"]
                tentative_distance = distances[current_node] + weight

                if tentative_distance < distances[neighbor_ip]:
                    distances[neighbor_ip] = tentative_distance
                    previous_nodes[neighbor_ip] = current_node

    path = []
    current = end_router

    if previous_nodes[end_router] is None:
        return []

    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path


#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

