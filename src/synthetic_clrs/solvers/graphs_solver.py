from queue import Queue, LifoQueue
import heapq

class GraphsSolver:
    @staticmethod
    def _construct_graph_from_input(edge_list, num_vertices, keep_weights=True):
        """
        Vertices are list(range(num_vertices)).
        Edge list is a list of tuples of the form:
        (u, v, w), which denotes an edge from u
        to v with weight w.
        
        Returns an adjacency list matching the graph,
        where u -> (v, w) indicates edge (u, v) with
        weight w. If keep_weights is False, mapping is
        just u -> v.
        """
        graph = [[] for _ in range(num_vertices)]
        for u, v, w in edge_list:  
            graph[u].append(((v, w) if keep_weights else v))

        return graph



    @staticmethod
    def _compute_topological_ordering(edge_list, num_vertices):
        """
        Returns topological ordering if one exists, otherwise
        returns -1.
        """
        graph = GraphsSolver._construct_graph_from_input(edge_list, num_vertices, keep_weights=False)

        indegrees = [0] * num_vertices
        for u, v, _ in edge_list:
            indegrees[v] += 1

        visited = [False] * num_vertices
        topo_order = [v for v in range(num_vertices) if indegrees[v] == 0]

        queue = Queue(maxsize=0)
        for v in topo_order:
            queue.put(v)
            visited[v] = True

        while not queue.empty():
            u = queue.get()
            for v in graph[u]:
                indegrees[v] -= 1
                if indegrees[v] == 0:
                    topo_order.append(v)
                    queue.put(v)
                    visited[v] = True

        if any(indegrees):
            # topological ordering doesnt exist
            return -1 
        
        return topo_order


    @staticmethod
    def articulation_points(edge_list, num_vertices, **_):
        raise NotImplementedError("omitting this algorithm for now...")


    @staticmethod
    def bellman_ford(edge_list, num_vertices, src, **_):
        """
        Compute shortest path distances to vertices from
        src if reachable. Output is list d, where 
        d[v] = min path distance from src to v (float('inf')
        if v is not reachable).
        If there is a negative cycle, return -1. Otherwise,
        return d.

        Note: Prefer graphs without negative cycles to
        avoid issues with encoding infinite
        distances
        """
        d = [float('inf')] * num_vertices
        d[src] = 0

        # num_vertices-1 rounds of edge relaxation
        for _ in range(1, num_vertices):
            for u, v, w in edge_list:
                d[v] = min(d[u] + w, d[v])

        for u, v, w in edge_list:
            if d[v] > d[u] + w:
                # negative cycle detected
                return -1
        
        return d


    def bfs(edge_list, num_vertices, src, **_):
        """
        For deteministic traversal, input graph
        should be a tree.
        """
        graph = GraphsSolver._construct_graph_from_input(edge_list, num_vertices, keep_weights=False)

        visited = [False] * num_vertices
        parents = [-1] * num_vertices

        visited[src] = True
        parents[src] = src
        
        # initialize queue with sorce
        queue = Queue(maxsize=0)
        queue.put(src)

        while not queue.empty():
            u = queue.get()
            for v in graph[u]:
                if visited[v]:
                    continue
                parents[v] = u
                visited[v] = True
                queue.put(v)
        
        return parents


    def bridges(edges, num_vertices, **_):
        raise NotImplementedError("omitting this algorithm for now...")


    def dag_shortest_paths(edge_list, num_vertices, src, **_):
        """
        Input graph must be a directed, acyclic graph (dag).
        For dataset generation, src must be able to reach all other
        vertices in graph to avoid infinite distances in output.
        """
        graph = GraphsSolver._construct_graph_from_input(edge_list, num_vertices)
        topo_order = GraphsSolver._compute_topological_ordering(edge_list, num_vertices)

        if topo_order == -1:
            raise ValueError("Input graph is not a directed, acyclic graph (dag)")

        d = [float('inf')] * num_vertices
        d[src] = 0

        # move pointer to src index in topo_order
        start = next((i for i in range(len(topo_order)) if topo_order[i] == src))
        
        for i in range(start, num_vertices): 
            u = topo_order[i]
            for v, w in graph[u]:
                # relax edge (u, v)
                d[v] = min(d[u] + w, d[v])

        return d


    def dfs(edge_list, num_vertices, src, **_):
        """
        For deterministic traversal, input graph
        should be a tree.
        """
        graph = GraphsSolver._construct_graph_from_input(edge_list, num_vertices, keep_weights=False)

        visited = [False] * num_vertices
        parents = [-1] * num_vertices

        visited[src] = True
        parents[src] = src
        
        # initialize stack with src
        stack = LifoQueue(maxsize=0)
        stack.put(src)

        while not stack.empty():
            u = stack.get()
            for v in graph[u]:
                if visited[v]:
                    continue
                parents[v] = u
                visited[v] = True
                stack.put(v)
        
        return parents


    def dijkstra(edge_list, num_vertices, src, **_):
        """
        Prefer graphs where src can reach all other
        vertices to avoid issues with encoding infinite
        distances
        """
        graph = GraphsSolver._construct_graph_from_input(edge_list, num_vertices)

        d = [float('inf')] * num_vertices
        d[src] = 0

        # put w in front so that it is used for ordering
        # in heap, i.e. lowest edge weight is at top of heap 
        edges = [(w, (src, v)) for v, w in graph[src]]
        heapq.heapify(edges)        
        while edges:
            w, (u, v) = heapq.heappop(edges)
            d[v] = min(d[u] + w, d[v])
            for child, w in graph[v]:
                if d[child] != float('inf'):
                    # already found shortest path to child
                    continue
                heapq.heappush(edges, (w, (v, child)))
        
        return d


    def floyd_warshall(edge_list, num_vertices, **_):
        raise NotImplementedError("omitting this algorithm for now...")


    def mst_kruskal(edge_list, num_vertices, **_):
        raise NotImplementedError("omitting this algorithm for now...")


    def mst_prim(edge_list, num_vertices, **_):
        raise NotImplementedError("omitting this algorithm for now...")


    def scc(edge_list, num_vertices, **_):
        raise NotImplementedError("omitting this algorithm for now...")


    def topological_sort(edge_list, num_vertices, **_):
        """
        Returns a topological ordering of vertices if one exists, otherwise
        returns -1.
        """
        return GraphsSolver._compute_topological_ordering(edge_list, num_vertices)
