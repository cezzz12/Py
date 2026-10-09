from collections import deque


def bfs_shortest_path(graph, start_vertex, end_vertex):
    """
    Find the shortest path between two vertices using BFS
    """
    q = deque([start_vertex])
    visited = {start_vertex}
    parent = {start_vertex: None}

    while q:
        current_vertex = q.popleft()

        for neighbor in graph.outbound_edges_iterator(current_vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_vertex
                q.append(neighbor)

                if neighbor == end_vertex:
                    # Reconstruct path
                    path = []
                    while neighbor is not None:
                        path.append(neighbor)
                        neighbor = parent[neighbor]
                    return path[::-1]

    return None