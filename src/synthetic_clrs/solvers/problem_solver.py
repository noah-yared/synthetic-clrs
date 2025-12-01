from types import MappingProxyType
from ..algorithms import Algorithm 
from .divide_conquer_solver import DivideConquerSolver
from .dynamic_programming_solver import DynamicProgrammingSolver
from .geometry_solver import GeometrySolver
from .graphs_solver import GraphsSolver
from .greedy_solver import GreedySolver
from .search_solver import SearchSolver
from .sorting_solver import SortingSolver
from .strings_solver import StringsSolver


class ProblemSolver:
    _SOLVERS = MappingProxyType({
        # divide and conquer
        Algorithm.KADANE: DivideConquerSolver.kadane,

        # dynamic programming
        Algorithm.LCS_LENGTH: DynamicProgrammingSolver.lcs_length,
        Algorithm.OPTIMAL_BST: DynamicProgrammingSolver.optimal_bst,

        # geometry
        Algorithm.GRAHAM_SCAN: GeometrySolver.graham_scan,
        Algorithm.JARVIS_MARCH: GeometrySolver.jarvis_march,
        Algorithm.SEGMENT_INTERSECT: GeometrySolver.segment_intersect,

        # graphs
        Algorithm.BELLMAN_FORD: GraphsSolver.bellman_ford,
        Algorithm.BFS: GraphsSolver.bfs,
        Algorithm.DAG_SHORTEST_PATH: GraphsSolver.dag_shortest_paths,
        Algorithm.DFS: GraphsSolver.dfs,
        Algorithm.DIJKSTRA: GraphsSolver.dijkstra,
        Algorithm.TOPOLOGICAL_SORT: GraphsSolver.topological_sort,
        
        # greedy
        Algorithm.TASK_SCHEDULING: GreedySolver.task_scheduling,
        Algorithm.ACTIVITY_SELECTION: GreedySolver.activity_selection,

        # search
        Algorithm.BINARY_SEARCH: SearchSolver.binary_search,
        Algorithm.MINIMUM: SearchSolver.minimum,

        # sorting
        Algorithm.BUBBLE_SORT: SortingSolver.bubble_sort,
        Algorithm.HEAPSORT: SortingSolver.heapsort,
        Algorithm.INSERTION_SORT: SortingSolver.insertion_sort,
        Algorithm.QUICKSORT: SortingSolver.quicksort,

        # strings
        Algorithm.KMP_MATCHER: StringsSolver.kmp_matcher,
        Algorithm.NAIVE_STRING_MATCHER: StringsSolver.naive_string_matcher,
    })

    @staticmethod
    def solve(algorithm, **kwargs):
        if algorithm not in ProblemSolver._SOLVERS:
            raise ValueError(f"Algorithm {algorithm} not supported! Valid algorithms: {ProblemSolver._SOLVERS.keys()}")
        return ProblemSolver._SOLVERS[algorithm](**kwargs)
