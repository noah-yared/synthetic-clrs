from types import MappingProxyType
from dataclasses import dataclass

from .algorithms import Algorithm

# use immutable dataclass for mapped problem
# type space to avoid spelling bugs below
@dataclass
class Category:
    """Algorithm category constants."""
    __slots__ = ()
    DIVIDE_CONQUER = "divide_and_conquer"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    GEOMETRY = "geometry"
    GRAPHS = "graphs"
    GREEDY = "greedy"
    SEARCH = "search"
    SORTING = "sorting"
    STRINGS = "strings"

ALGORITHMS_BY_CATEGORY = MappingProxyType({
    Category.GREEDY: [
        Algorithm.ACTIVITY_SELECTION,
        Algorithm.TASK_SCHEDULING
    ],
    Category.GRAPHS: [
        Algorithm.BELLMAN_FORD,
        Algorithm.BFS,
        Algorithm.DAG_SHORTEST_PATH,
        Algorithm.DFS,
        Algorithm.DIJKSTRA,
        Algorithm.TOPOLOGICAL_SORT
    ],
    Category.SEARCH: [
        Algorithm.BINARY_SEARCH,
        Algorithm.MINIMUM
    ],
    Category.SORTING: [
        Algorithm.BUBBLE_SORT,
        Algorithm.HEAPSORT,
        Algorithm.INSERTION_SORT,
        Algorithm.QUICKSORT
    ],
    Category.DIVIDE_CONQUER: [
        Algorithm.KADANE
    ],
    Category.GEOMETRY: [
        Algorithm.GRAHAM_SCAN,
        Algorithm.JARVIS_MARCH,
        Algorithm.SEGMENT_INTERSECT
    ],
    Category.STRINGS: [
        Algorithm.KMP_MATCHER,
        Algorithm.NAIVE_STRING_MATCHER
    ],
    Category.DYNAMIC_PROGRAMMING: [
        Algorithm.LCS_LENGTH,
        Algorithm.OPTIMAL_BST
    ],
})

ALGORITHM_TO_CATEGORY = MappingProxyType({
    algorithm: category
    for category, algorithms in ALGORITHMS_BY_CATEGORY.items()
    for algorithm in algorithms
})
