from exceptions import VertexError, EdgeError
from copy import deepcopy
from random import randrange,random


class Graph:
    def __init__(self, n=0):
        self._vertices = {}
        self._outbound_edges = {}
        self._inbound_edges = {}
        self._edge_costs = {}

        for i in range(n):
            self.add_vertex(i)

    def count_vertices(self):
        return len(self._vertices)

    def count_edges(self):
        return len(self._edge_costs)

    def vertices_iterator(self):
        return iter(self._vertices)

    def is_vertex(self, vertex):
        return vertex in self._vertices

    def add_vertex(self, vertex):
        if vertex in self._vertices:
            raise VertexError(f"Vertex {vertex} already exists")

        self._vertices[vertex] = True
        self._outbound_edges[vertex] = set()
        self._inbound_edges[vertex] = set()

    def remove_vertex(self, vertex):
        if vertex not in self._vertices:
            raise VertexError(f"Vertex {vertex} does not exist")

        # Remove all outbound edges
        outbound_copy = list(self._outbound_edges[vertex])
        for neighbor in outbound_copy:
            self.remove_edge(vertex, neighbor)

        # Remove all inbound edges
        inbound_copy = list(self._inbound_edges[vertex])
        for source in inbound_copy:
            self.remove_edge(source, vertex)

        # Remove vertex from vertices and edge tracking
        del self._vertices[vertex]
        del self._outbound_edges[vertex]
        del self._inbound_edges[vertex]

    def is_edge(self, source, target):
        return target in self._outbound_edges[source]

    def add_edge(self, source, target, cost=0):
        if source not in self._vertices or target not in self._vertices:
            raise VertexError("Vertices must exist before adding an edge")

        if self.is_edge(source, target):
            raise EdgeError(f"Edge from {source} to {target} already exists")

        self._outbound_edges[source].add(target)
        self._inbound_edges[target].add(source)
        self._edge_costs[(source, target)] = cost

    def remove_edge(self, source, target):
        if not self.is_edge(source, target):
            raise EdgeError(f"Edge from {source} to {target} does not exist")

        self._outbound_edges[source].remove(target)
        self._inbound_edges[target].remove(source)
        del self._edge_costs[(source, target)]

    def get_edge_cost(self, source, target):
        if not self.is_edge(source, target):
            raise EdgeError(f"Edge from {source} to {target} does not exist")

        return self._edge_costs[(source, target)]

    def set_edge_cost(self, source, target, new_cost):
        if not self.is_edge(source, target):
            raise EdgeError(f"Edge from {source} to {target} does not exist")

        self._edge_costs[(source, target)] = new_cost

    def out_degree(self, vertex):
        if vertex not in self._vertices:
            raise VertexError(f"Vertex {vertex} does not exist")

        return len(self._outbound_edges[vertex])

    def in_degree(self, vertex):
        if vertex not in self._vertices:
            raise VertexError(f"Vertex {vertex} does not exist")

        return len(self._inbound_edges[vertex])

    def outbound_edges_iterator(self, vertex):
        if vertex not in self._vertices:
            raise VertexError(f"Vertex {vertex} does not exist")

        return iter(self._outbound_edges[vertex])

    def inbound_edges_iterator(self, vertex):
        if vertex not in self._vertices:
            raise VertexError(f"Vertex {vertex} does not exist")

        return iter(self._inbound_edges[vertex])

    def copy(self):
        return deepcopy(self)


def read_graph_from_file(filename):
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().split())
        graph = Graph(n)
        for _ in range(m):
            source, target, cost = map(int, f.readline().split())
            graph.add_edge(source, target, cost)

    return graph

def write_graph_to_file(graph, filename):
    with open(filename, 'w') as f:
        f.write(f"{graph.count_vertices()} {graph.count_edges()}\n")

        for source in graph.vertices_iterator():
            for target in graph.outbound_edges_iterator(source):
                cost = graph.get_edge_cost(source, target)
                f.write(f"{source} {target} {cost}\n")


def create_random_graph(vertices, edges):
    graph = Graph(vertices)

    for _ in range(edges):
        source = randrange(vertices)
        target = randrange(vertices)

        while source == target or graph.is_edge(source, target):
            source = randrange(vertices)
            target = randrange(vertices)

        cost = randrange(1, 100)  # Random cost between 1 and 99
        graph.add_edge(source, target, cost)

    return graph

def advanced_random_graph_generation(self):
        while True:
            try:
                # Get basic graph parameters
                vertices = int(input("Number of vertices (1-1000): "))
                if vertices < 1 or vertices > 1000:
                    print("Vertices must be between 1 and 1000.")
                    continue

                # Determine maximum possible edges
                max_edges = vertices * (vertices - 1)

                # Get edge count with validation
                edges = int(input(f"Number of edges (1-{max_edges}): "))
                if edges < 1 or edges > max_edges:
                    print(f"Edges must be between 1 and {max_edges}.")
                    continue

                # Cost range options
                print("\nChoose cost range:")
                print("1. Small range (1-10)")
                print("2. Medium range (1-100)")
                print("3. Large range (1-1000)")
                print("4. Custom range")

                cost_choice = input("Enter cost range option: ")

                # Determine cost range
                if cost_choice == '1':
                    min_cost, max_cost = 1, 10
                elif cost_choice == '2':
                    min_cost, max_cost = 1, 100
                elif cost_choice == '3':
                    min_cost, max_cost = 1, 1000
                elif cost_choice == '4':
                    min_cost = int(input("Minimum cost: "))
                    max_cost = int(input("Maximum cost: "))
                    if min_cost > max_cost:
                        print("Minimum cost cannot be greater than maximum cost.")
                        continue
                else:
                    print("Invalid option. Using default medium range.")
                    min_cost, max_cost = 1, 100

                # Generate advanced random graph
                graph = Graph(vertices)

                # Ensure graph is connected
                # First, create a spanning tree
                for i in range(1, vertices):
                    source = random.randint(0, i - 1)
                    cost = random.randint(min_cost, max_cost)
                    graph.add_edge(source, i, cost)

                # Add remaining edges
                remaining_edges = edges - (vertices - 1)
                attempts = 0
                max_attempts = vertices * vertices  # Prevent infinite loop

                while remaining_edges > 0 and attempts < max_attempts:
                    source = random.randint(0, vertices - 1)
                    target = random.randint(0, vertices - 1)

                    if source != target and not graph.is_edge(source, target):
                        cost = random.randint(min_cost, max_cost)
                        graph.add_edge(source, target, cost)
                        remaining_edges -= 1

                    attempts += 1

                self.graph = graph
                print(f"\nRandom graph generated successfully!")
                print(f"Vertices: {graph.count_vertices()}")
                print(f"Edges: {graph.count_edges()}")
                print(f"Cost range: {min_cost}-{max_cost}")
                break

            except ValueError:
                print("Please enter valid integer values.")
            except Exception as e:
                print(f"An error occurred: {e}")