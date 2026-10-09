from exceptions import VertexError, EdgeError
from graph import Graph, write_graph_to_file, read_graph_from_file


def find_connected_components(graph):
    """
    Find all connected components in an undirected graph
    Returns a list of Graph objects, each representing a connected component
    """
    # Create an undirected version of the graph adjacency structure
    undirected_connections = {}
    for v in graph.vertices_iterator():
        undirected_connections[v] = set()

    # Add all connections (both directions)
    for v in graph.vertices_iterator():
        for neighbor in graph.outbound_edges_iterator(v):
            undirected_connections[v].add(neighbor)
            undirected_connections[neighbor].add(v)

    # DFS to find connected components
    def dfs(vertex, component):
        visited[vertex] = True
        component.add(vertex)
        for neighbor in undirected_connections[vertex]:
            if not visited[neighbor]:
                dfs(neighbor, component)

    visited = {v: False for v in graph.vertices_iterator()}
    components = []

    for vertex in graph.vertices_iterator():
        if not visited[vertex]:
            component = set()
            dfs(vertex, component)
            components.append(component)

    # Create Graph objects for each component
    component_graphs = []
    for component_vertices in components:
        component_graph = Graph()

        # Add vertices
        for vertex in component_vertices:
            component_graph.add_vertex(vertex)

        # Add edges (only those within the component)
        for vertex in component_vertices:
            for neighbor in graph.outbound_edges_iterator(vertex):
                if neighbor in component_vertices:
                    try:
                        cost = graph.get_edge_cost(vertex, neighbor)
                        component_graph.add_edge(vertex, neighbor, cost)
                    except EdgeError:
                        # Edge might already be added
                        pass

        component_graphs.append(component_graph)

    return component_graphs


def create_example_graph_2():
    """
    Creates a graph with 5 vertices, 8 edges, and 1 connected component
    """
    graph = Graph(5)  # Create a graph with 5 vertices (0-4)

    # Create a cycle 0->1->2->3->4->0
    graph.add_edge(0, 1, 2)
    graph.add_edge(1, 2, 3)
    graph.add_edge(2, 3, 4)
    graph.add_edge(3, 4, 5)
    graph.add_edge(4, 0, 6)

    # Add more edges to reach 8 edges total
    graph.add_edge(0, 2, 7)
    graph.add_edge(1, 4, 8)
    graph.add_edge(2, 4, 9)

    return graph


def print_component_info(component, index):
    """
    Print information about a component
    """
    vertices = list(component.vertices_iterator())
    edges_count = component.count_edges()
    print(f"\nComponent {index}:")
    print(f"  Vertices ({len(vertices)}): {vertices}")
    print(f"  Edges: {edges_count}")

    # Display edges
    print("  Edge list:")
    for v in component.vertices_iterator():
        for neighbor in component.outbound_edges_iterator(v):
            cost = component.get_edge_cost(v, neighbor)
            print(f"    {v} -> {neighbor} (cost: {cost})")


# Main execution
def main():
    print("===== Example 2: Graph with 1 Connected Component =====")

    # Create the example graph
    graph = create_example_graph_2()

    # Save graph to file
    filename = "graph_1component.txt"
    write_graph_to_file(graph, filename)
    print(f"Graph saved to {filename}")

    # Display graph info
    print(f"\nGraph information:")
    print(f"  Vertices: {graph.count_vertices()}")
    print(f"  Edges: {graph.count_edges()}")
    print(f"  Vertices list: {list(graph.vertices_iterator())}")

    # Find connected components
    print("\nFinding connected components...")
    components = find_connected_components(graph)
    print(f"Found {len(components)} connected components")

    # Display component info
    for i, component in enumerate(components, 1):
        print_component_info(component, i)

    # Verify that we have one connected component with all vertices
    if len(components) == 1 and components[0].count_vertices() == graph.count_vertices():
        print("\nVerified: Graph has exactly one connected component containing all vertices")


if __name__ == "__main__":
    main()