from math import radians, sin, cos, acos


class _Node:
    def __init__(self, nodeid, latitude, longitude):
        self.id = nodeid
        self.lat = latitude
        self.lon = longitude

    def __str__(self):
        return f"Node {self.id} ({self.lat} {self.lon})"


class _Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.distance = None

    def __str__(self):
        return f"Edge {self.source} -> {self.target}"


class Graph:
    def __init__(self, gmlfile):
        self.nodes = []
        self.edges = []
        self.__parse_graph(gmlfile)
        self.__distances()

    def __parse_graph(self, gmlfile):
        with open(gmlfile, "r") as reader:
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

                    self.nodes.append(_Node(nodeid, latitude, longitude))

                elif "edge" in line:
                    while "]" not in line:
                        line = reader.readline()
                        line = line.strip()
                        line = line.split(" ")
                        if line[0] == "source":
                            source = int(line[1])
                        elif line[0] == "target":
                            target = int(line[1])

                    self.edges.append(_Edge(source, target))

                line = reader.readline()

    def __distances(self):
        for edge in self.edges:
            edge.distance = \
                self.get_distance(edge.source, edge.target)

    def get_node(self, nodeid):
        for node in self.nodes:
            if nodeid == node.id:
                return node

    @staticmethod
    def __great_circle_distance(node1, node2):
        lat1, lon1, lat2, lon2 = \
            map(radians, [node1.lat, node1.lon, node2.lat, node2.lon])

        delta = acos(
            sin(lat1) * sin(lat2) +
            cos(lat1) * cos(lat2) * cos(abs(lon1 - lon2))
        )
        return 6371 * delta

    def get_distance(self, nid1, nid2):
        node1 = self.get_node(nid1)
        node2 = self.get_node(nid2)
        return self.__great_circle_distance(node1, node2)

    def most_southern_node(self):
        return min(self.nodes, key=lambda node: node.lat)

    def most_northern_node(self):
        return max(self.nodes, key=lambda node: node.lat)

    def most_western_node(self):
        return min(self.nodes, key=lambda node: node.lon)

    def most_eastern_node(self):
        return max(self.nodes, key=lambda node: node.lon)

    def max_distance(self):
        return max(self.edges, key=lambda edge: edge.distance)


if __name__ == "__main__":
    geo = Graph("Bbnplanet.gml")

    for node in geo.nodes:
        print(node)

    for edge in geo.edges:
        print(edge)

    print()
    print(geo.max_distance())
    print(geo.most_eastern_node())
    print(geo.most_northern_node())
    print(geo.most_southern_node())
    print(geo.most_western_node())
