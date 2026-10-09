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


def create_example_graph_1():
    """
    Creates a graph with 8 vertices and 3 connected components (one isolated vertex)
    """
    graph = Graph(8)  # Create a graph with 8 vertices (0-7)

    # Component 1: vertices 0, 1, 2
    graph.add_edge(0, 1, 5)
    graph.add_edge(1, 2, 3)
    graph.add_edge(2, 0, 4)

    # Component 2: vertices 3, 4, 5, 6
    graph.add_edge(3, 4, 2)
    graph.add_edge(4, 5, 7)
    graph.add_edge(5, 6, 1)
    graph.add_edge(6, 3, 6)
    graph.add_edge(4, 6, 9)

    # Component 3: isolated vertex 7
    # No edges needed for an isolated vertex

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
    print("===== Example 1: Graph with 3 Connected Components =====")

    # Create the example graph
    graph = create_example_graph_1()

    # Save graph to file
    filename = "graph_3components.txt"
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

    # Verify that we have one isolated vertex
    for component in components:
        if component.count_vertices() == 1 and component.count_edges() == 0:
            vertex = next(component.vertices_iterator())
            print(f"\nVerified: Component contains isolated vertex {vertex}")


if __name__ == "__main__":
    main()