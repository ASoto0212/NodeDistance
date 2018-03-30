import sys

#This file takes in a directed graph in the format  <vertex> <vertex> <weight>
#and finds the shortest distance between two given vertices


# Graph definition, connects all nodes
class Graph:
    def __init__(self):
        self.nodes = set()  # set of all nodes for easy searching
        self.vertices = {}  # map of node(name) to it's corresponding vertex(object)
        self.distances = {}  # map of all nodes and weights

    def add_node(self, newNode):
        newVertex = Vertex(newNode)
        self.nodes.add(newNode)
        self.vertices[newNode] = newVertex
        self.distances[newNode] = {}

    def add_edge(self, start, end, weight):
        if start not in self.vertices.keys():
            self.add_node(start)
        if end not in self.vertices.keys():
            self.add_node(end)
        self.vertices[start].add_neighbor(self.vertices[end], weight)  # creating edges
        self.distances[start][end] = weight

    def get_node(self, vertex):
        if vertex in self.vertices:
            return self.vertices[vertex]

    def get_nodes(self):
        return self.vertices.keys()

    def get_distance(self, start, end):
        return start.get_distance() + end.get_distance()


class Vertex:
    def __init__(self, start):
        self.id = start  # name of each vertex
        self.neighbors = {}  # vertices that extend from this vertex(this->neighbor)
        self.visited = False  # if vertex has been visited by search
        self.distance = sys.maxsize  # initial distance set to max int size
        self.prev = None  # predecessor of current node for easy backtracking the shortest path

    def get_id(self):
        return self.id

    def add_neighbor(self, next, weight):
        self.neighbors[next] = weight

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_weight(self, neighbor):
        return self.neighbors[neighbor]

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.prev = prev

    def set_distance(self, dist):
        self.distance = dist

    def set_visited(self):
        self.visited = True


def Shortest_Distance(graph, start, goal):
    goal_path = []
    unvisited = set(graph.nodes)
    curr = start
    curr.set_distance(0)
    while unvisited:
        if curr.visited:  # checks if current vertex has already been visited and finds a connection that hasn't been visited
            for next in curr.get_neighbors():
                if not next.visited:
                    curr = next
        if curr == goal:
            goal_path.clear()
            goal_path.append(curr)  # adds the current vertex to the beginning of
            while curr.prev != None:  # the goal path. Adds predecessor nodes until
                goal_path.append(curr.prev)  # the first is reached
                curr = curr.prev
            return goal_path[
                   ::-1]  # return the list in the order it was traversed, becuase vertices were added backwards
        min_v = {}  # min_v keeps track of current nodes/vertex children
        for next in curr.get_neighbors():
            new_dist = curr.get_distance() + curr.get_weight(next)
            min_v[new_dist] = next
            if new_dist < next.distance:  # comparison to see if moving to the next node reduces is beneficial
                next.set_distance(new_dist)
                next.set_previous(curr)

        min_w = min(min_v.keys())
        if curr.get_id() in unvisited:  # removes a visited node from the set, if it exists
            unvisited.remove(curr.get_id())
        curr.visited = True
        curr = min_v.get(min_w)


"""***************Begin Main Function******************"""
file_name = input("Input the text file name: ")
if ".txt" not in file_name:  # adds extension just in case it was not included
    file_name += ".txt"
with open(file_name) as f:
    data = []
    for line in f:
        data.append([int(i) for i in line.split()])  # adds information line by line and store it in data[]
graph = Graph()

for row in data:
    if row[0] not in graph.nodes:  # for every row, adds the first int (start_vertex) to node list
        graph.add_node(row[0])
    elif row[1] not in graph.nodes:
        graph.add_node(row[1])  # adds second int(end_vertex) if first doesn't exist
    graph.add_edge(row[0], row[1], row[2])
    print("Start: %d , End: %d , Weight: %d" % (row[0], row[1], row[2]))

print("Graph Created. Vertices: %s" % (graph.vertices.keys()))
start_vertex = None
end_vertex = None

while start_vertex not in graph.nodes or end_vertex not in graph.nodes:  # loop checks to make sure input vertices are in set
    start_vertex = int(input("Enter a starting vertex: "))
    end_vertex = int(input("Enter an ending vertex: "))
    if (start_vertex not in graph.nodes or end_vertex not in graph.nodes):
        print("Vertex not in graph. Try again.")
path = Shortest_Distance(graph, graph.get_node(start_vertex), graph.get_node(end_vertex))

if path != None:
    for i in range(len(path)):
        print("Vertex: %d, Distance to vertex: %d" % (path[i].get_id(), path[i].get_distance()))

else:
    print("No Path Found")  # prints only if path return none(aka there was no link between nodes)
