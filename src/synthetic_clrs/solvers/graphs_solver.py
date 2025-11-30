from collections import defaultdict
from queue import Queue, LifoQueue
import heapq

class GraphsSolver:
    @staticmethod
    def _construct_graph_from_input(edges, num_vertices, keep_weights=True):
        """
        Vertices are list(range(num_vertices)).
        Edges is a list of tuples of the form:
        ((u, v), w), which denotes an edge from u
        to v with weight w.
        
        Returns an adjacency list matching the graph,
        where u -> (v, w) indicates edge (u, v) with
        weight w. If keep_weights is False, mapping is
        just u -> v.
        """
        graph = [[] for _ in range(num_vertices)]
        for (u, v), w in edges:  
            graph[u].append(((v, w) if keep_weights else v))

        return graph


    def _compute_topological_ordering(edges, num_vertices):
        """
        Returns topological ordering if one exists, otherwise
        returns -1.
        """
        graph = GraphsSolver._construct_graph_from_input(edges, num_vertices, keep_weights=False)

        indegrees = [0] * num_vertices
        for (u, v), _ in edges:
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
    def _articulation_points_solver(edges, num_vertices):
        raise NotImplementedError("omitting this algorithm for now...")


    @staticmethod
    def _bellman_ford_solver(edges, num_vertices, src):
        """
        Prefer graphs without negative cycles to
        avoid issues with encoding infinite
        distances
        """
        d = [float('inf')] * num_vertices
        d[src] = 0

        # num_vertices roundes of edge relaxation
        for _ in range(1, num_vertices):
            for (u, v), w in edges:
                d[v] = min(d[u] + w, d[v])

        # make sure no negative cycles occur
        # otherwise return "-inf"
        for (u, v), w in edges:
            if d[v] > d[u] + w:
                # negative cycle detected
                d[v] = float("-inf") 
        
        return d


    def _bfs_solver(edges, num_vertices, src):
        """
        For deteministic traversal, input graph
        should be a tree.
        """
        graph = GraphsSolver._construct_graph_from_input(edges, num_vertices, keep_weights=False)

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


    def _bridges_solver(edges, num_vertices):
        raise NotImplementedError("omitting this algorithm for now...")


    def _dag_shortest_paths_solver(edges, num_vertices, src):
        """
        Input graph must be a directed, acyclic graph (dag).
        """
        graph = GraphsSolver._construct_graph_from_input(edges, num_vertices)
        topo_order = GraphsSolver._compute_topological_ordering(edges, num_vertices)

        d = [float('inf')] * num_vertices
        d[src] = 0

        # move pointer to src
        start = next((v for v in topo_order if v == src))
        
        for i in range(start, num_vertices): 
            u = topo_order[i]
            for v, w in graph[u]:
                # relax edge (u, v)
                d[v] = min(d[u] + w, d[v])

        return d


    def _dfs_solver(edges, num_vertices, src):
        """
        For deterministic traversal, input graph
        should be a tree.
        """
        graph = GraphsSolver._construct_graph_from_input(edges, num_vertices, keep_weights=False)

        visited = [False] * num_vertices
        parents = [-1] * num_vertices

        visited[src] = True
        parents[src] = src
        
        # initialize queue with sorce
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


    def _dijkstra_solver(edges, num_vertices, src):
        """
        Prefer graphs where src can reach all other
        vertices to avoid issues with encoding infinite
        distances
        """
        graph = GraphsSolver._construct_graph_from_input(edges, num_vertices)

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
                heapq.heappush(edges, (w, (v, child)))
        
        return d


    def _floyd_warshall_solver(edges, num_vertices):
        raise NotImplementedError("omitting this algorithm for now...")


    def _mst_kruskal_solver(edges, num_vertices):
        raise NotImplementedError("omitting this algorithm for now...")


    def _mst_prim_solver(edges, num_vertices):
        raise NotImplementedError("omitting this algorithm for now...")


    def _scc_solver(edges, num_vertices):
        raise NotImplementedError("omitting this algorithm for now...")


    def _topological_sort_solver(edges, num_vertices):
        return GraphsSolver._compute_topological_ordering(edges, num_vertices)


    def solve(id, **kwargs):
        solvers = [
            GraphsSolver._articulation_points_solver,
            GraphsSolver._bellman_ford_solver,
            GraphsSolver._bfs_solver,
            GraphsSolver._bridges_solver,
            GraphsSolver._dag_shortest_paths_solver,
            GraphsSolver._dfs_solver,
            GraphsSolver._dijkstra_solver,
            GraphsSolver._floyd_warshall_solver,
            GraphsSolver._mst_kruskal_solver,
            GraphsSolver._mst_prim_solver,
            GraphsSolver._scc_solver,
            GraphsSolver._topological_sort_solver,
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[id](**kwargs)
