from graph import Graph
from exceptions import VertexError, EdgeError


def lowest_cost_walk(graph, start_vertex, end_vertex):
    """
    Find the lowest cost walk between two vertices
    """
    if not graph.is_vertex(start_vertex) or not graph.is_vertex(end_vertex):
        raise VertexError("Start or end vertex does not exist")

    INF = float('inf')
    n = graph.count_vertices()

    # Distance matrix for dynamic programming
    d = [[INF] * (n + 1) for _ in range(n)]
    d[start_vertex][0] = 0

    # Dynamic Programming to find lowest cost walk
    for k in range(1, n + 1):
        for v in graph.vertices_iterator():
            d[v][k] = d[v][k - 1]

        for u in graph.vertices_iterator():
            for v in graph.outbound_edges_iterator(u):
                if d[u][k - 1] != INF:
                    current_cost = d[u][k - 1] + graph.get_edge_cost(u, v)
                    if current_cost < d[v][k]:
                        d[v][k] = current_cost

    # Check for negative cost cycles
    for v in graph.vertices_iterator():
        if d[v][n] < d[v][n - 1]:
            raise EdgeError("Negative cost cycle detected")

    # Find minimum cost
    min_cost = min(d[end_vertex])

    return min_cost if min_cost != INF else None


def find_connected_components(graph):
    """
    Find all connected components in an undirected graph
    Returns a list of Graph objects, each representing a connected component

    Note: For this function, we treat the directed graph as undirected by considering
    an edge in either direction as a connection.
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


def floyd_warshall_lowest_cost_walk(graph, start_vertex, end_vertex):
    """
    Find the lowest cost walk between two vertices using Floyd-Warshall algorithm

    Assumes no negative cost cycles.

    Returns the lowest cost of walk between start and end vertices,
    or None if no path exists.
    """
    if not graph.is_vertex(start_vertex) or not graph.is_vertex(end_vertex):
        raise VertexError("Start or end vertex does not exist")

    n = graph.count_vertices()
    INF = float('inf')

    # Initialize distance matrix
    dist = [[INF] * n for _ in range(n)]

    # Set diagonal to 0
    for v in graph.vertices_iterator():
        dist[v][v] = 0

    # Add direct edges
    for v in graph.vertices_iterator():
        for u in graph.outbound_edges_iterator(v):
            dist[v][u] = graph.get_edge_cost(v, u)

    # Floyd-Warshall algorithm
    for k in graph.vertices_iterator():
        for i in graph.vertices_iterator():
            for j in graph.vertices_iterator():
                if dist[i][k] != INF and dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # Return the cost between start and end vertices
    return dist[start_vertex][end_vertex] if dist[start_vertex][end_vertex] != INF else None


def prim_minimal_spanning_tree(graph):
    """
    Finds the minimal spanning tree of an undirected weighted graph using Prim's algorithm

    Requires an undirected graph (bidirectional edges with same cost)

    Returns a new Graph object representing the minimal spanning tree
    """
    # Validate graph is connected first
    components = find_connected_components(graph)
    if len(components) > 1:
        raise ValueError("Graph must be connected to create a minimal spanning tree")

    # Choose first vertex as starting point
    vertices = list(graph.vertices_iterator())
    if not vertices:
        return Graph()  # Empty graph case

    start_vertex = vertices[0]

    # Track vertices in the minimum spanning tree
    mst = Graph()
    mst.add_vertex(start_vertex)

    # Track edges to consider
    candidate_edges = []
    visited = {start_vertex}

    # Add initial edges from start vertex
    for neighbor in graph.outbound_edges_iterator(start_vertex):
        candidate_edges.append((start_vertex, neighbor, graph.get_edge_cost(start_vertex, neighbor)))

    # Iterate until all vertices are included
    while candidate_edges:
        # Find the minimum cost edge connecting to an unvisited vertex
        min_edge = min(candidate_edges, key=lambda x: x[2])
        source, target, cost = min_edge

        # Skip if target already in MST
        if target in visited:
            candidate_edges.remove(min_edge)
            continue

        # Add vertex and edge to MST
        if not mst.is_vertex(target):
            mst.add_vertex(target)
        mst.add_edge(source, target, cost)
        visited.add(target)

        # Remove used edge
        candidate_edges.remove(min_edge)

        # Add new candidate edges from the new vertex
        for neighbor in graph.outbound_edges_iterator(target):
            if neighbor not in visited:
                candidate_edges.append((target, neighbor, graph.get_edge_cost(target, neighbor)))

    return mst