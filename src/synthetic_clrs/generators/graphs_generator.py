import random
from .problem_generator import ProblemGenerator

class GraphsGenerator(ProblemGenerator):
    def __init__(self, min_vertices=5, max_vertices=10, min_weight=-10, max_weight=10, seed=None):
        super().__init__(seed)
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
        

    def _generate_random_edge_weights(self, num_edges, weighted, only_positive_weights=False):
        if weighted:
            return self.rng.gen_int_array(
                num_edges,
                # make sure weights are strictly positive if only_positive_weights=True
                1 if only_positive_weights else self.min_weight, 
                self.max_weight
            )
        else:
            return [1] * num_edges


    def _get_edge_weights(self, adj_matrix, directed=True, weighted=True, only_positive_weights=False):
        num_vertices = len(adj_matrix)
        edges = []
        for i in range(num_vertices):
            for j in range(num_vertices):
                # (i, j) is same edge as (j, i)
                # so only consider (i, j) for i < j
                if j > i and not directed: 
                    continue
                edges.append((i, j))

        weights = self._generate_random_edge_weights(len(edges), weighted, only_positive_weights)

        return list(zip(edges, weights))


    def _gen_random_edges_from_topo_order(self, topo_order):
        num_vertices = len(topo_order)        
        adj_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        for i, u in enumerate(topo_order):
            bool_array = self.rng.gen_bool_array(num_vertices-i-1)
            for j in range(i+1, num_vertices):
                if bool_array[j-i-1]:
                    adj_matrix[i][topo_order[j]] = 1
        return adj_matrix


    def _generate_random_undirected_graph(self, num_vertices, weighted, only_positive_weights):
        random_bool_grid = self.rng.gen_bool_grid(num_vertices, num_vertices)
        symmetric_adj_matrix = self.copy_bottom_left_tri_to_top_right_tri(random_bool_grid)
        return self._get_edge_weights(symmetric_adj_matrix, directed=False, weighted=weighted, only_positive_weights=only_positive_weights)


    def _generate_random_directed_graph(self, num_vertices, weighted, only_positive_weights):
        adj_matrix = self.rng.gen_bool_grid(num_vertices, num_vertices)
        return self._get_edge_weights(adj_matrix, directed=True, weighted=weighted, only_positive_weights=only_positive_weights)


    def _generate_random_dag(self, num_vertices, weighted, only_positive_weights):
        random_topo_order = list(range(num_vertices))
        random.shuffle(random_topo_order)
        adj_matrix = self._gen_random_edges_from_topo_order(random_topo_order)
        return self._get_edge_weights(adj_matrix, directed=True, weighted=weighted, only_positive_weights=only_positive_weights)

    
    def _generate_random_tree(self, num_vertices, weighted, only_positive_weights):
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
                # path to this node already exists
                # so skip this edge
                continue
            parent[v] = u
            # trees are undirected so add both
            # directions
            edges.append((u, v))
            edges.append((v, u))
                
        weights = self._generate_random_edge_weights(len(edges), weighted, only_positive_weights=only_positive_weights)

        return list(zip(edges, weights))


    def generate(self, tree=False, acyclic=False, directed=False, weighted=False, only_positive_weights=False, include_src=False):
        num_vertices = self.rng.gen_int(self.min_vertices, self.max_vertices)

        if tree:
            # tree (complete acyclic graph)
            graph = self._generate_random_tree(num_vertices, weighted, only_positive_weights)

        elif not directed:
            # undirected graph
            graph = self._generate_random_undirected_graph(num_vertices, weighted, only_positive_weights)

        elif not acyclic:
            # directed graph
            graph = self._generate_random_directed_graph(num_vertices, weighted, only_positive_weights)

        else:
            # default to directed acyclic graph
            graph = self._generate_random_dag(num_vertices, weighted, only_positive_weights)        

        if not include_src:
            return (graph, num_vertices)
        
        random_src = self.rng.gen_int(0, num_vertices-1)
        return ((graph, num_vertices), random_src)