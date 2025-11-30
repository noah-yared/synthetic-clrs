from types import MappingProxyType
from dataclasses import dataclass

# use immutable dataclass for mapped problem
# type space to avoid spelling bugs below
@dataclass
class ProblemType: # readonly problem types
    __slots__ = ()
    DIVIDE_CONQUER = "divide_and_conquer"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    GEOMETRY = "geometry"
    GRAPHS = "graphs"
    GREEDY = "greedy"
    SEARCH = "search"
    SORTING = "sorting"
    STRINGS = "strings"

PROBLEM_TYPES = tuple([
    ProblemType.DIVIDE_CONQUER,
    ProblemType.DYNAMIC_PROGRAMMING,
    ProblemType.GEOMETRY,
    ProblemType.GRAPHS,
    ProblemType.GREEDY,
    ProblemType.SEARCH,
    ProblemType.SORTING,
    ProblemType.STRINGS,
])

PROBLEM_MAPPING = {
    ProblemType.GREEDY: ['activity_selector', 'task_scheduling'],
    ProblemType.GRAPHS: [
        'articulation_points','bellman_ford', 'bfs', 'bridges',
        'dag_shortest_paths', 'dfs', 'dijkstra', 'floyd_warshall',
        'mst_kruskal', 'mst_prim', 'strongly_connected_components',
        'topological_sort'
    ],
    ProblemType.SEARCH: ['binary_search', 'minimum', 'quickselect'],
    ProblemType.SORTING: ['bubble_sort', 'heapsort', 'insertion_sort', 'quicksort'],
    ProblemType.DIVIDE_CONQUER: ['find_maximum_subarray_kadane'],
    ProblemType.GEOMETRY: ['graham_scan', 'jarvis_march', 'segments_intersect'],
    ProblemType.STRINGS: ['kmp_matcher', 'naive_string_matcher'],
    ProblemType.DYNAMIC_PROGRAMMING: ['lcs_length', 'matrix_chain_order', 'optimal_bst']
}

if __name__ == "__main__":
    pass