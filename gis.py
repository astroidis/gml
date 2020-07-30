from math import radians, sin, cos, acos, sqrt, asin


class Node:
    def __init__(self, nodeid, latitude, longitude):
        self.id = nodeid
        self.lat = latitude
        self.lon = longitude


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.distance = None


def find_node(nodelist, nodeid):
    for node in nodelist:
        if nodeid == node.id:
            return node


def great_circle_distance(node1, node2):
    lat1, lon1, lat2, lon2 = \
        map(radians, [node1.lat, node1.lon, node2.lat, node2.lon])

    delta = acos(
       sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(abs(lon1 - lon2))
    )
    return 6371 * delta


def haversine_distance(node1, node2):
    lat1, lon1, lat2, lon2 = \
        map(radians, [node1.lat, node1.lon, node2.lat, node2.lon])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * 6371 * asin(sqrt(a))


def most_southern_node(nodelist):
    return min(nodelist, key=lambda node: node.lat)


def most_northern_node(nodelist):
    return max(nodelist, key=lambda node: node.lat)


def most_western_node(nodelist):
    return min(nodelist, key=lambda node: node.lon)


def most_eastern_node(nodelist):
    return max(nodelist, key=lambda node: node.lon)


def max_distance(edgelist):
    return max(edgelist, key=lambda edge: edge.distance)


def nearest_node(node, edgelist, nodelist):
    connections = [edge for edge in edgelist
                   if node.id == edge.source or node.id == edge.target]

    nearest = min(connections, key=lambda edge: edge.distance)
    if node.id == nearest.source:
        return find_node(nodelist, nearest.target)
    else:
        return find_node(nodelist, nearest.source)


def objects_in_area(position, raduis, nodelist):
    """ position: tuple - (latitude, longitude) """
    in_area = []
    pos = Node(None, position[0], position[1])
    for node in nodelist:
        dist = great_circle_distance(pos, node)
        if dist < raduis:
            in_area.append(node)

    return in_area


nodes = []
edges = []
with open("Bbnplanet.gml", "r") as reader:
    line = reader.readline()
    while line:
        if "node" in line:
            while "]" not in line:
                line = reader.readline()
                line = line.strip()
                line = line.split(" ")
                if "id" in line:
                    nodeid = int(line[1])
                elif "Longitude" in line:
                    longitude = float(line[1])
                elif "Latitude" in line:
                    latitude = float(line[1])

            nodes.append(Node(nodeid, latitude, longitude))

        elif "edge" in line:
            while "]" not in line:
                line = reader.readline()
                line = line.strip()
                line = line.split(" ")
                if line[0] == "source":
                    source = int(line[1])
                elif line[0] == "target":
                    target = int(line[1])

            edges.append(Edge(source, target))

        line = reader.readline()

# for edge in edges:
#     node1 = find_node(nodes, edge.source)
#     node2 = find_node(nodes, edge.target)

#     edge.distance = great_circle_distance(node1, node2)


for edge in edges:
    node1 = find_node(nodes, edge.source)
    node2 = find_node(nodes, edge.target)
    gcd = great_circle_distance(node1, node2)
    hsd = haversine_distance(node1, node2)
    print(f"{edge.source} => {edge.target}")
    print(f"GCD: {gcd}\nHSD: {hsd}\n")


# node = most_southern_node(nodes)
# print(f"Most southern {node.id} ({node.lat}; {node.lon})")

# node = most_northern_node(nodes)
# print(f"Most northen {node.id} ({node.lat}; {node.lon})")

# node = most_western_node(nodes)
# print(f"Most western {node.id} ({node.lat}; {node.lon})")

# node = most_eastern_node(nodes)
# print(f"Most eastern {node.id} ({node.lat}; {node.lon})")

# print(f"Nearest to {nodes[7].id} is {nearest_node(nodes[7], edges, nodes).id}")

# edge = max_distance(edges)
# print(f"Max distance is {edge.distance} ({edge.source} => {edge.target})")

# position = (41.4995, -81.69541)
# d = 150
# area = objects_in_area(position, d, nodes)
# print(f"Objects in less than {d}km from {position}:")
# if area != []:
#     for obj in area:
#         print(f"{obj.id} ({obj.lat}; {obj.lon})")
# else:
#     print(f"No objects found in {d}km from {position}")
