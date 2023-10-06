# -*- coding: utf-8 -*-
"""
CSCI 6212 Project 2
Author: Le Sun
"""
import time, random

class WeightedGraph:
    def __init__(self):
        self.vertices = set()
        self.edges = set()

    def add_vertex(self, vertex):
        self.vertices.add(vertex)

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.vertices:
            self.add_vertex(vertex1)
        if vertex2 not in self.vertices:
            self.add_vertex(vertex2)
        if (vertex1, vertex2, weight) not in self.edges and (vertex2, vertex1, weight) not in self.edges:
            self.edges.add((vertex1, vertex2, weight))

    def get_vertices(self):
        return list(self.vertices)

    def get_edges(self):
        return list(self.edges)

    def __str__(self):
        return f"Vertices: {self.get_vertices()}\nEdges: {self.get_edges()}"

# generate random weighted graph
def random_weighted_graph(num_vertices, num_edges):
    # Create a new graph
    graph = WeightedGraph()

    # Generate random vertices
    vertices = [i for i in range(num_vertices)]
    
    # I use the following two sections to make sure all vertices are connected by an edge 
    # add initial vertex to graph
    initial_vertex = random.choice(vertices)
    graph.add_vertex(initial_vertex)
    vertices.remove(initial_vertex)
    
    # add vertex in vertices to graph one by one
    while len(vertices) > 0:
        vertex1 = random.choice(graph.get_vertices())
        vertex2 = random.choice(vertices)
        # connect a vertex from graph with a vertex not yet added to graph
        weight = random.randint(1, 20)
        graph.add_edge(vertex1, vertex2, weight)
        graph.add_vertex(vertex2)
        vertices.remove(vertex2)
    
    # Generate random edges with weights to meet the numbers of edges requirements
    while len(graph.get_edges()) < num_edges:
        vertex1 = random.choice(graph.get_vertices())
        vertex2 = random.choice(graph.get_vertices())
        if vertex1 != vertex2:
            weight = random.randint(1, 20)
            graph.add_edge(vertex1, vertex2, weight)

    return graph

# use union find to check if two vertices are connected and connect vertices added to the mst
class UnionFind(object):
    def __init__(self, size):
        self.root = [i for i in range(size)]
        self.rank = [1] * size
        self.count = size
    def find(self, x):
        if self.root[x] == x:
            return x
        else:
            self.root[x] = self.find(self.root[x])
            return self.root[x]
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            self.count -= 1
            
    def connected(self, x, y):
        return self.find(x) == self.find(y)

graphs = [] # this list saves all test cases
# all test cases have 500 vertices, and the edge number varies from 600 - 9600
for i in range(600, 9900, 500):
    graph = random_weighted_graph(500, i)
    graphs.append(graph)

test_case = 0

for graph in graphs:
    start_time = time.time()
    test_case += 1
    edges = sorted(graph.get_edges(), key=lambda x: x[-1]) # sort all edges by weight
    vertices = graph.get_vertices()
    mst = []
    uf = UnionFind(len(vertices)) # initialize a unionfind data structure of size len(vertices)
    for edge in edges:
        if uf.count == 1: # uf.count == 1 means all vertices are connected, mst found
            break
        if not uf.connected(edge[0], edge[1]): # if the two vertices are connected in union find, adding this edge will create a cycle
            mst.append(edge)
            uf.union(edge[0], edge[1])
    end_time = time.time()
    print("Test case ", test_case, "finished, component number:", uf.count,"edge number:", 
           len(edges), ", time spend:", end_time - start_time)
    
    
    
    
    
