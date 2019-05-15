import json
from collections import defaultdict

# Define earth (planet 18) and b3-r7-r4nd7 (planet 246)
startPlanet = 18
destinationPlanet = 246
filePath = 'json.txt'


def main():
    """ Executes the algorithm with the predefined settings """
    graph = Graph()

    # Read in file and parse data to graph
    with open(filePath) as json_file:
        data = json.load(json_file)
        for p in data['edges']:
            cost = p['cost']
            source = p['source']
            target = p['target']

            graph.add_edge(source, target, cost)

    path, distance = dijkstra(graph, startPlanet, destinationPlanet)

    print(path)
    print(distance)


# Define a class that represents the universe -> graph: has edges between nodes with weights assigned to it
class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    # edges are bi-directional, therefore added twice
    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


def dijkstra(graph, start, end):
    """return the shortest path from start to end planet and the travelled distance"""

    # shortest paths is a dict of nodes whose value is a tuple of (previous node, weight)
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()
    distance = 0

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]
        # iterate through 'neighbours'
        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        if current_node is not None and next_node is not None:
            distance += graph.weights[(current_node, next_node)]
        current_node = next_node

    # Reverse path
    path = path[::-1]
    return path, distance


if __name__ == "__main__":
    main()
