import itertools
import random
from ..utils import Rng
from ..algorithms import Algorithm

class GraphsGenerator:
    def __init__(self, rng=None, min_vertices=3, max_vertices=7, min_weight=-3, max_weight=10, seed=None):
        # skew towards positive weights to avoid negative cycles in Bellman-Ford
        self.rng = rng if rng is not None else Rng(seed)
        self.min_vertices = min_vertices
        self.max_vertices = max_vertices
        self.min_weight = min_weight
        self.max_weight = max_weight


    @staticmethod
    def copy_bottom_left_tri_to_top_right_tri(grid):
        symmetric_grid = grid[::]
        m, n = len(grid), len(grid[0])
        for r in range(m):
            for c in range(0, min(n, r)):
                symmetric_grid[m-r-1][n-c-1] = grid[r][c]
        return symmetric_grid


    @staticmethod
    def _has_negative_cycle(edge_list, num_vertices, src):
        d = [float("inf")] * num_vertices
        d[src] = 0

        for _ in range(1, num_vertices):
            for u, v, w in edge_list:
                d[v] = min(d[u] + w, d[v])

        return any(
            d[v] > d[u] + w
            for u, v, w in edge_list
        )


    @staticmethod
    def _unreachable_vertices_from_src(edge_list, num_vertices, src):
        graph = [[] for _ in range(num_vertices)]
        for u, v, _ in edge_list:
            graph[u].append(v)

        visited = [False] * num_vertices
        visited[src] = True

        def dfs(u):
            for v in graph[u]:
                if visited[v]:
                    continue
                visited[v] = True
                dfs(v)

        # mark all reachable nodes
        # from src as visited
        dfs(src)

        return [
            v for v in range(num_vertices)
            if not visited[v]
        ]

    
    @staticmethod
    def _get_dag_source(edge_list, num_vertices):
        indegrees = [0 for _ in range(num_vertices)]
        for _, v, _ in edge_list:
            indegrees[v] += 1
        
        return next((
            v for v in range(num_vertices)
            if indegrees[v] == 0
        ))
        

    def _generate_random_edge_weights(self, num_weights, weighted, only_positive_weights):
        if weighted:
            return self.rng.gen_int_array(
                num_weights,
                # make sure weights are strictly positive if only_positive_weights=True
                1 if only_positive_weights else self.min_weight, 
                self.max_weight
            )
        else:
            return [1] * num_weights


    def _get_edge_weights(self, edges=None, adj_matrix=None, directed=True, weighted=True, only_positive_weights=False):
        if edges is None:
            num_vertices = len(adj_matrix)
            edges = [
                (u, v)
                for u in range(num_vertices)
                for v in range(num_vertices)
                if adj_matrix[u][v]
            ]

        weights = self._generate_random_edge_weights(len(edges), weighted, only_positive_weights)

        if directed:
            return [
                (u, v, w) for (u, v), w in zip(edges, weights)
            ]

        # assign same weight for each edge direction
        assigned_edges = set()
        edge_list = []
        for u, v in edges:
            e = tuple(sorted([u, v]))
            if e in assigned_edges:
                continue
            random_weight = weights[len(assigned_edges)]
            edge_list.append((u, v, random_weight))
            edge_list.append((v, u, random_weight))
            assigned_edges.add(e)

        return edge_list


    def _gen_random_edges_from_topo_order(self, topo_order):
        num_vertices = len(topo_order)        
        adj_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        for i, u in enumerate(topo_order):
            bool_array = self.rng.gen_bool_array(num_vertices-i-1)
            for j in range(i+1, num_vertices):
                if bool_array[j-i-1]:
                    adj_matrix[u][topo_order[j]] = 1
        return adj_matrix


    def _generate_random_undirected_graph(self, num_vertices, weighted, only_positive_weights):
        random_bool_grid = self.rng.gen_bool_grid(num_vertices, num_vertices)
        symmetric_adj_matrix = self.copy_bottom_left_tri_to_top_right_tri(random_bool_grid)
        return self._get_edge_weights(adj_matrix=symmetric_adj_matrix, directed=False, weighted=weighted, only_positive_weights=only_positive_weights)


    def _generate_random_directed_graph(self, num_vertices, weighted, only_positive_weights):
        adj_matrix = self.rng.gen_bool_grid(num_vertices, num_vertices)
        return self._get_edge_weights(adj_matrix=adj_matrix, directed=True, weighted=weighted, only_positive_weights=only_positive_weights)


    def _generate_random_dag(self, num_vertices, weighted, only_positive_weights):
        random_topo_order = list(range(num_vertices))
        random.shuffle(random_topo_order)
        adj_matrix = self._gen_random_edges_from_topo_order(random_topo_order)
        return self._get_edge_weights(adj_matrix=adj_matrix, directed=True, weighted=weighted, only_positive_weights=only_positive_weights)

    
    def _generate_random_tree(self, num_vertices, weighted, only_positive_weights, offset=0):
        random_topo_order = list(range(num_vertices))
        random.shuffle(random_topo_order)

        # root is first vertex of generated topological ordering
        root = random_topo_order[0]

        # store parents when adding edges, with -1 as placeholder
        # to avoid creating multiple paths to a node
        parent = [-1 for _ in range(num_vertices)]
        parent[root] = root

        # shuffle all possible edges that abide by topological
        # ordering
        possible_edges = [
            (u, random_topo_order[j])
            for i, u in enumerate(random_topo_order)
            for j in range(i + 1, num_vertices)
        ]
        random.shuffle(possible_edges)

        edges = []
        for u, v in possible_edges:
            if len(edges) == num_vertices - 1:
                break
            if parent[v] != -1:
                # path to node exists
                # so skip this edge
                continue
            parent[v] = u
            # add single edge direction with offset
            edges.append((u+offset, v+offset))
 
        return self._get_edge_weights(edges=edges, directed=False, weighted=weighted, only_positive_weights=only_positive_weights)
    

    def _generate_random_forest(self, num_vertices, weighted, only_positive_weights):
        random_partition = self.rng.gen_random_integer_partition(num_vertices)
        partition_prefix_sum = list(itertools.accumulate(random_partition, initial=0))
        return list(itertools.chain((
            self._generate_random_tree(
                num_tree_vertices,
                weighted,
                only_positive_weights,
                offset=partition_prefix_sum[i]
            )
            for i, num_tree_vertices in enumerate(random_partition)
        )))

    
    def _generate_random_reachable_digraph_from_src(self, src, num_vertices, weighted, only_positive_weights):
        random_digraph = self._generate_random_directed_graph(num_vertices, weighted, only_positive_weights)
        unreachable_nodes = GraphsGenerator._unreachable_vertices_from_src(random_digraph, num_vertices, src)
        # add direct edge from src to unreachable nodes
        random_weights = self._generate_random_edge_weights(len(unreachable_nodes), weighted, only_positive_weights)
        for v, w in zip(unreachable_nodes, random_weights):
            random_digraph.append((src, v, w))
        return random_digraph


    def _generate_random_reachable_dag_from_vertex(self, num_vertices, weighted, only_positive_weights):
        random_dag = self._generate_random_dag(num_vertices, weighted, only_positive_weights)
        dag_src = GraphsGenerator._get_dag_source(random_dag, num_vertices)
        unreachable_nodes = GraphsGenerator._unreachable_vertices_from_src(random_dag, num_vertices, dag_src)
        # add direct edge from src to unreachable nodes
        random_weights = self._generate_random_edge_weights(len(unreachable_nodes), weighted, only_positive_weights)
        for v, w in zip(unreachable_nodes, random_weights):
            random_dag.append((dag_src, v, w))
        return random_dag, dag_src


    def _try_to_generate_reachable_digraph_without_negative_cycle(self, retries=2):
        # try to generate a reachable digraph with negative weight edges without a
        # negative cycle within {retries} generations; if fails both attempts,
        # default to a strictly positive weight reachable digraph
        for _ in range(retries):
            problem = self._generate_graph_problem(directed=True, weighted=True, only_positive_weights=False, reachable_from_src=True, include_src=True)
            if self._has_negative_cycle(**problem):
                continue
            return problem
        return self._generate_graph_problem(directed=True, weighted=True, only_positive_weights=True, reachable_from_src=True, include_src=True)


    def _generate_graph_problem(self, tree=False, acyclic=False, directed=False, weighted=False, only_positive_weights=False, reachable_from_src=False, include_src=False):
        num_vertices = self.rng.gen_int(self.min_vertices, self.max_vertices)
        src = None

        if tree:
            # tree (complete acyclic graph)
            edge_list = self._generate_random_tree(num_vertices, weighted, only_positive_weights)

        elif acyclic and not directed:
            # forest
            edge_list = self._generate_random_forest(num_vertices, weighted, only_positive_weights)

        elif not directed:
            # undirected graph
            edge_list = self._generate_random_undirected_graph(num_vertices, weighted, only_positive_weights)

        elif acyclic and reachable_from_src:
            # directed acyclic graph reachable from src
            edge_list, src = self._generate_random_reachable_dag_from_vertex(num_vertices, weighted, only_positive_weights)

        elif acyclic:
            # directed acyclic graph
            edge_list = self._generate_random_dag(num_vertices, weighted, only_positive_weights)        

        elif reachable_from_src:
            # directed graph that is reachable from src
            edge_list = self._generate_random_reachable_digraph_from_src(
                src := self.rng.gen_int(0, num_vertices-1),
                num_vertices,
                weighted,
                only_positive_weights
            )

        else:
            # directed graph
            edge_list = self._generate_random_directed_graph(num_vertices, weighted, only_positive_weights)

        if not include_src:
            return {
                "edge_list": edge_list,
                "num_vertices": num_vertices
            }
        
        if src is None:
            src = self.rng.gen_int(0, num_vertices-1)

        return {
            "edge_list": edge_list,
            "num_vertices": num_vertices,
            "src": src
        }


    def generate_bellman_ford_problem(self):
        # directed graphs with negative weights
        problem = self._try_to_generate_reachable_digraph_without_negative_cycle()
        problem["task"] = "Find the shortest path distances from src to all vertices in the graph (negative weights allowed)"
        return problem


    def generate_bfs_problem(self):
        # unweighted tree for deterministic traversal
        problem = self._generate_graph_problem(tree=True, weighted=False, include_src=True)
        problem["task"] = "Traverse the graph in breadth-first order from src and track parents (parent of src is just src)"
        return problem


    def generate_dag_shortest_path_problem(self):
        # directed acyclic graph with negative weights
        problem = self._generate_graph_problem(acyclic=True, directed=True, weighted=True, only_positive_weights=False, reachable_from_src=True, include_src=True)
        problem["task"] = "Find the shortest path distances from src to all vertices in a DAG"
        return problem


    def generate_dfs_problem(self):
        # unweighted tree for deterministic traversal
        problem = self._generate_graph_problem(tree=True, weighted=False, include_src=True)
        problem["task"] = "Traverse the graph in depth-first order from src and track parents (parent of src is just src)"
        return problem


    def generate_dijkstra_problem(self):
        # directed graph with positive weights
        problem = self._generate_graph_problem(directed=True, weighted=True, only_positive_weights=True, reachable_from_src=True, include_src=True)
        problem["task"] = "Find the shortest path distances from src to all vertices in the graph"
        return problem


    def generate_topological_sort_problem(self):
        # unweighted directed acyclic graph
        problem = self._generate_graph_problem(acyclic=True, directed=True, weighted=False)
        problem["task"] = "Find a valid topological order of the vertices in the DAG"
        return problem


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.BELLMAN_FORD: self.generate_bellman_ford_problem,
            Algorithm.BFS: self.generate_bfs_problem,
            Algorithm.DAG_SHORTEST_PATH: self.generate_dag_shortest_path_problem,
            Algorithm.DFS: self.generate_dfs_problem,
            Algorithm.DIJKSTRA: self.generate_dijkstra_problem,
            Algorithm.TOPOLOGICAL_SORT: self.generate_topological_sort_problem,
        }[algorithm](**kwargs)