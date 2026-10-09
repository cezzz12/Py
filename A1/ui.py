from graph import Graph, read_graph_from_file, write_graph_to_file, create_random_graph
from exceptions import VertexError, EdgeError
from service import lowest_cost_walk,floyd_warshall_lowest_cost_walk,prim_minimal_spanning_tree,find_connected_components
from bfs import bfs_shortest_path
from dijkstra import dijkstra
import random


class UI:
    def __init__(self):
        self.graph = Graph()
        self.copied_graph = None

    def print_menu(self):
        print("\n--- Graph Management System ---")
        print("1. Create a new graph")
        print("2. Add vertex")
        print("3. Remove vertex")
        print("4. Add edge")
        print("5. Remove edge")
        print("6. Get edge cost")
        print("7. Set edge cost")
        print("8. Count vertices")
        print("9. Count edges")
        print("10. Check if vertex exists")
        print("11. Check if edge exists")
        print("12. Get vertex in-degree")
        print("13. Get vertex out-degree")
        print("14. List vertices")
        print("15. List outbound edges")
        print("16. List inbound edges")
        print("17. Read graph from file")
        print("18. Write graph to file")
        print("19. Create random graph")
        print("20. Find shortest path")
        print("21. Find lowest cost walk")
        print("22. Copy current graph")
        print("23. Advanced random graph generation")
        print("24. Find Connected Components")
        print("25. Floyd-Warshall Lowest Cost Walk")
        print("26. Prim's Minimal Spanning Tree")
        print("27. Create undirected graph")
        print("28.  Calculate Hamiltonian Cycle")
        print("0. Exit")

    def copy_graph(self):
        self.copied_graph = self.graph.copy()
        print("Current graph has been copied.")
        print(
            f"Copied graph has {self.copied_graph.count_vertices()} vertices and {self.copied_graph.count_edges()} edges.")

    def create_new_graph(self):
        self.graph = Graph()
        print("A new empty graph has been created.")

    def add_vertex(self):
        try:
            vertex = int(input("Enter vertex to add: "))
            self.graph.add_vertex(vertex)
            print(f"Vertex {vertex} added successfully.")
        except VertexError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter a valid integer vertex.")

    def remove_vertex(self):
        try:
            vertex = int(input("Enter vertex to remove: "))
            self.graph.remove_vertex(vertex)
            print(f"Vertex {vertex} removed successfully.")
        except VertexError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter a valid integer vertex.")

    def add_edge(self):
        try:
            source = int(input("Enter source vertex: "))
            target = int(input("Enter target vertex: "))
            cost = int(input("Enter edge cost (default 0): ") or 0)
            self.graph.add_edge(source, target, cost)
            print(f"Edge from {source} to {target} with cost {cost} added successfully.")
        except (VertexError, EdgeError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def remove_edge(self):
        try:
            source = int(input("Enter source vertex: "))
            target = int(input("Enter target vertex: "))
            self.graph.remove_edge(source, target)
            print(f"Edge from {source} to {target} removed successfully.")
        except EdgeError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def get_edge_cost(self):
        try:
            source = int(input("Enter source vertex: "))
            target = int(input("Enter target vertex: "))
            cost = self.graph.get_edge_cost(source, target)
            print(f"Edge cost from {source} to {target}: {cost}")
        except EdgeError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def set_edge_cost(self):
        """
        Set the cost of an edge
        """
        try:
            source = int(input("Enter source vertex: "))
            target = int(input("Enter target vertex: "))
            new_cost = int(input("Enter new edge cost: "))
            self.graph.set_edge_cost(source, target, new_cost)
            print(f"Edge cost from {source} to {target} set to {new_cost}.")
        except EdgeError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def create_undirected_random_graph(self):
        """
        Generate a random undirected graph
        """
        while True:
            try:
                # Get basic graph parameters
                vertices = int(input("Number of vertices (1-1000): "))
                if vertices < 1 or vertices > 1000:
                    print("Vertices must be between 1 and 1000.")
                    continue

                # Determine maximum possible edges for an undirected graph
                max_edges = (vertices * (vertices - 1)) // 2

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

                # Generate undirected graph
                graph = Graph(vertices)

                # Ensure graph is connected
                # First, create a spanning tree
                for i in range(1, vertices):
                    source = random.randint(0, i - 1)
                    cost = random.randint(min_cost, max_cost)
                    # Add edges in both directions to make it undirected
                    graph.add_edge(source, i, cost)
                    graph.add_edge(i, source, cost)

                # Add remaining edges
                remaining_edges = edges - (vertices - 1)
                attempts = 0
                max_attempts = vertices * vertices  # Prevent infinite loop

                while remaining_edges > 0 and attempts < max_attempts:
                    source = random.randint(0, vertices - 1)
                    target = random.randint(0, vertices - 1)

                    if source != target and not graph.is_edge(source, target):
                        cost = random.randint(min_cost, max_cost)
                        # Add edges in both directions to make it undirected
                        graph.add_edge(source, target, cost)
                        graph.add_edge(target, source, cost)
                        remaining_edges -= 1

                    attempts += 1

                self.graph = graph
                print(f"\nUndirected random graph generated successfully!")
                print(f"Vertices: {graph.count_vertices()}")
                print(f"Edges: {graph.count_edges()}")
                print(f"Cost range: {min_cost}-{max_cost}")
                break

            except ValueError:
                print("Please enter valid integer values.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def find_shortest_path(self):
        try:
            start = int(input("Enter start vertex: "))
            end = int(input("Enter end vertex: "))
            path = bfs_shortest_path(self.graph, start, end)

            if path:
                print("Shortest path:", ' -> '.join(map(str, path)))
            else:
                print("No path found between the vertices.")
        except VertexError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def find_lowest_cost_walk(self):
        try:
            start = int(input("Enter start vertex: "))
            end = int(input("Enter end vertex: "))
            cost = lowest_cost_walk(self.graph, start, end)

            if cost is not None:
                print(f"Lowest cost walk from {start} to {end}: {cost}")
            else:
                print("No path found between the vertices.")
        except (VertexError, EdgeError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def display_connected_components(self):
        """
        Display all connected components of the graph as separate Graph objects
        """
        from service import find_connected_components

        try:
            components = find_connected_components(self.graph)

            if not components:
                print("No components found. Graph may be empty.")
                return

            print(f"\nFound {len(components)} connected component(s):")

            for i, component in enumerate(components, 1):
                vertices = list(component.vertices_iterator())
                edges_count = component.count_edges()
                print(f"\nComponent {i}:")
                print(f"  Vertices ({len(vertices)}): {vertices}")
                print(f"  Edges: {edges_count}")

                # Display edges if not too many
                if edges_count <= 20:  # Limit the number of edges displayed to avoid cluttering
                    print("  Edge list:")
                    for v in component.vertices_iterator():
                        for neighbor in component.outbound_edges_iterator(v):
                            cost = component.get_edge_cost(v, neighbor)
                            print(f"    {v} -> {neighbor} (cost: {cost})")
                else:
                    print("  (Too many edges to display)")

            # Ask if user wants to save any component to a file
            save_option = input("\nDo you want to save any component to a file? (y/n): ")
            if save_option.lower() == 'y':
                comp_num = int(input(f"Enter component number to save (1-{len(components)}): "))
                if 1 <= comp_num <= len(components):
                    filename = input("Enter filename to save to: ")
                    from graph import write_graph_to_file
                    write_graph_to_file(components[comp_num - 1], filename)
                    print(f"Component {comp_num} saved to {filename}")
                else:
                    print("Invalid component number.")

        except Exception as e:
            print(f"An error occurred: {e}")

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

    def find_connected_components(self):
        """
        Find and display connected components of the graph
        """
        try:
            components = find_connected_components(self.graph)

            if not components:
                print("No components found. Graph may be empty.")
                return

            print(f"\nFound {len(components)} connected component(s):")

            for i, component in enumerate(components, 1):
                vertices = list(component.vertices_iterator())
                edges_count = component.count_edges()
                print(f"\nComponent {i}:")
                print(f"  Vertices ({len(vertices)}): {vertices}")
                print(f"  Edges: {edges_count}")

                # Display edges if not too many
                if edges_count <= 20:  # Limit the number of edges displayed to avoid cluttering
                    print("  Edge list:")
                    for v in component.vertices_iterator():
                        for neighbor in component.outbound_edges_iterator(v):
                            cost = component.get_edge_cost(v, neighbor)
                            print(f"    {v} <-> {neighbor} (cost: {cost})")
                else:
                    print("  (Too many edges to display)")

            # Ask if user wants to save any component to a file
            save_option = input("\nDo you want to save any component to a file? (y/n): ")
            if save_option.lower() == 'y':
                comp_num = int(input(f"Enter component number to save (1-{len(components)}): "))
                if 1 <= comp_num <= len(components):
                    filename = input("Enter filename to save to: ")
                    write_graph_to_file(components[comp_num - 1], filename)
                    print(f"Component {comp_num} saved to {filename}")
                else:
                    print("Invalid component number.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def floyd_warshall_lowest_cost_walk(self):
        """
        Find the lowest cost walk using Floyd-Warshall algorithm
        """
        try:
            start = int(input("Enter start vertex: "))
            end = int(input("Enter end vertex: "))
            cost = floyd_warshall_lowest_cost_walk(self.graph, start, end)

            if cost is not None:
                print(f"Lowest cost walk from {start} to {end} using Floyd-Warshall: {cost}")
            else:
                print("No path found between the vertices.")
        except (VertexError, EdgeError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Please enter valid integer values.")

    def prim_minimal_spanning_tree(self):
        """
        Construct Minimal Spanning Tree using Prim's algorithm
        """
        try:
            mst = prim_minimal_spanning_tree(self.graph)

            print("\nMinimal Spanning Tree:")
            print(f"Vertices: {list(mst.vertices_iterator())}")
            print(f"Edges: {mst.count_edges()}")

            print("\nEdge list:")
            total_cost = 0
            for v in mst.vertices_iterator():
                for neighbor in mst.outbound_edges_iterator(v):
                    cost = mst.get_edge_cost(v, neighbor)
                    total_cost += cost
                    print(f"  {v} <-> {neighbor} (cost: {cost})")

            print(f"\nTotal MST cost: {total_cost}")

            # Option to save MST to a file
            save_option = input("\nDo you want to save the Minimal Spanning Tree to a file? (y/n): ")
            if save_option.lower() == 'y':
                filename = input("Enter filename to save to: ")
                write_graph_to_file(mst, filename)
                print(f"Minimal Spanning Tree saved to {filename}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def calc_hamiltonian_cycle(self):
        try:
            n = self.graph.count_vertices()
            if n < 3:
                return
            # Start from vertex 0 or first available
            vertices = list(self.graph.vertices_iterator())
            if not vertices:
                print("Graph is empty.")
                return
            start_vertex = vertices[0] #start
            current_vertex = start_vertex
            path = [current_vertex] #path
            visited = {current_vertex} #visited
            total_cost = 0
            print(f"Starting  from vertex {start_vertex}")
            print(f"Total vertices to visit: {n}")

            while len(path) < n:
                # Get all possible next vertices with their costs
                candidates = []
                for neighbor in self.graph.outbound_edges_iterator(current_vertex):
                    if neighbor not in visited:
                        cost = self.graph.get_edge_cost(current_vertex, neighbor)
                        candidates.append((cost, neighbor))

                if not candidates:
                    print("No more unvisited vertices reachable. Cannot form Hamiltonian cycle.")
                    return

                # Sort by cost to get minimum cost edges first
                candidates.sort()

                #  check if it would create a <n cycle
                next_vertex = None
                next_cost = None

                for cost, candidate in candidates:
                    # Check if adding this vertex would create a cycle of length < n
                    would_create_shorter_cycle = False

                    if len(path) < n - 1:  # Not the last vertex to add
                        # Check if candidate connects back to start or any vertex
                        for vertex_in_path in path[:-1]:  # exclude current
                            if self.graph.is_edge(candidate, vertex_in_path):
                                would_create_shorter_cycle = True
                                break

                    if not would_create_shorter_cycle:
                        next_vertex = candidate
                        next_cost = cost
                        break

                if next_vertex is None:
                    print("Cannot find next vertex without creating shorter cycle.")
                    return

                # Add the vertex to our path
                path.append(next_vertex)
                visited.add(next_vertex)
                total_cost += next_cost
                current_vertex = next_vertex

                print(f"Step {len(path) - 1}: {path[-2]} -> {path[-1]} (cost: {next_cost})")

            # Try to complete the cycle by returning to start
            if self.graph.is_edge(current_vertex, start_vertex):
                final_cost = self.graph.get_edge_cost(current_vertex, start_vertex)
                total_cost += final_cost
                path.append(start_vertex)  # Complete the cycle

                print(f"\nHamiltonian cycle found!")
                print(f"Path: {' -> '.join(map(str, path))}")
                print(f"Total cost: {total_cost}")
            else:
                print(f"\nCannot complete Hamiltonian cycle - no edge from {current_vertex} back to {start_vertex}")
                print(f"Partial path: {' -> '.join(map(str, path))}")
                print(f"Partial cost: {total_cost}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def start(self):
        while True:
            self.print_menu()
            choice = input("Choose an option: ")

            try:
                choice = int(choice)

                if choice == 0:
                    break
                elif choice == 1:
                    self.create_new_graph()
                elif choice == 2:
                    self.add_vertex()
                elif choice == 3:
                    self.remove_vertex()
                elif choice == 4:
                    self.add_edge()
                elif choice == 5:
                    self.remove_edge()
                elif choice == 6:
                    self.get_edge_cost()
                elif choice == 7:
                    self.set_edge_cost()
                elif choice == 8:
                    print(f"Total vertices: {self.graph.count_vertices()}")
                elif choice == 9:
                    print(f"Total edges: {self.graph.count_edges()}")
                elif choice == 10:
                    vertex = int(input("Vertex to check: "))
                    print(f"Vertex exists: {self.graph.is_vertex(vertex)}")
                elif choice == 11:
                    source = int(input("Source vertex: "))
                    target = int(input("Target vertex: "))
                    print(f"Edge exists: {self.graph.is_edge(source, target)}")
                elif choice == 12:
                    vertex = int(input("Vertex: "))
                    print(f"In-degree: {self.graph.in_degree(vertex)}")
                elif choice == 13:
                    vertex = int(input("Vertex: "))
                    print(f"Out-degree: {self.graph.out_degree(vertex)}")
                elif choice == 14:
                    print("Vertices:", list(self.graph.vertices_iterator()))
                elif choice == 15:
                    vertex = int(input("Vertex: "))
                    print("Outbound edges:", list(self.graph.outbound_edges_iterator(vertex)))
                elif choice == 16:
                    vertex = int(input("Vertex: "))
                    print("Inbound edges:", list(self.graph.inbound_edges_iterator(vertex)))
                elif choice == 17:
                    filename = input("File path: ")
                    self.graph = read_graph_from_file(filename)
                    print("Graph read from file successfully.")
                elif choice == 18:
                    filename = input("File path: ")
                    write_graph_to_file(self.graph, filename)
                    print("Graph written to file successfully.")
                elif choice == 19:
                    vertices = int(input("Number of vertices: "))
                    edges = int(input("Number of edges: "))
                    self.graph = create_random_graph(vertices, edges)
                    print("Random graph created.")
                elif choice == 20:
                    self.find_shortest_path()
                elif choice == 21:
                    self.find_lowest_cost_walk()
                elif choice == 22:
                    self.copy_graph()
                elif choice == 23:
                    self.advanced_random_graph_generation()
                elif choice == 24:
                    self.find_connected_components()
                elif choice == 25:
                    self.floyd_warshall_lowest_cost_walk()
                elif choice == 26:
                    self.prim_minimal_spanning_tree()
                elif choice == 27:
                    self.create_undirected_random_graph()
                elif choice ==28:
                    self. calc_hamiltonian_cycle()
                else:
                    print("Invalid option!")

            except ValueError:
                print("Please enter a valid integer.")
            except Exception as e:
                print(f"An error occurred: {e}")


def main():
    ui = UI()
    ui.start()


if __name__ == "__main__":
    main()