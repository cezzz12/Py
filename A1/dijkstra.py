import heapq
from exceptions import VertexError, EdgeError


def dijkstra(graph, start_vertex, end_vertex):
    """
    Find the minimum cost path between two vertices using Dijkstra's algorithm

    Args:
        graph: Graph object
        start_vertex: Starting vertex
        end_vertex: Target vertex

    Returns:
        tuple: (path, cost) where path is a list of vertices and cost is the total cost
        or (None, None) if no path exists

    Note:
        This implementation assumes all edge weights are non-negative.
        Dijkstra's algorithm does not work correctly with negative edge weights.
    """
    if not graph.is_vertex(start_vertex) or not graph.is_vertex(end_vertex):
        raise VertexError("Start or end vertex does not exist")

    if start_vertex == end_vertex:
        return [start_vertex], 0

    distances = {vertex: float('inf') for vertex in graph.vertices_iterator()}
    distances[start_vertex] = 0

    previous = {vertex: None for vertex in graph.vertices_iterator()}

    priority_queue = [(0, start_vertex)]

    visited = set()

    while priority_queue and end_vertex not in visited:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        if current_vertex == end_vertex:
            break

        for neighbor in graph.outbound_edges_iterator(current_vertex):
            if neighbor in visited:
                continue

            edge_cost = graph.get_edge_cost(current_vertex, neighbor)
            distance = current_distance + edge_cost

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    if distances[end_vertex] == float('inf'):
        return None, None

    path = []
    current = end_vertex
    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[end_vertex]