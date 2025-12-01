from dataclasses import dataclass

@dataclass
class Algorithm:
    __slots__ = () # Immutable

    # divide and conquer
    KADANE = "kadane"

    # dynamic programming
    LCS_LENGTH = "lcs_length"
    OPTIMAL_BST = "optimal_bst"

    # geometry
    GRAHAM_SCAN = "graham_scan"
    JARVIS_MARCH = "jarvis_march"
    SEGMENT_INTERSECT = "segment_intersect"

    # graphs
    BELLMAN_FORD = "bellman_ford"
    BFS = "bfs"
    DAG_SHORTEST_PATH = "dag_shortest_path"
    DFS = "dfs"
    DIJKSTRA = "dijkstra"
    TOPOLOGICAL_SORT = "topological_sort"
    
    # greedy
    TASK_SCHEDULING = "task_scheduling"
    ACTIVITY_SELECTION = "activity_selection"

    # search
    BINARY_SEARCH = "binary_search"
    MINIMUM = "minimum"

    # sorting
    BUBBLE_SORT = "bubble_sort"
    HEAPSORT = "heapsort"
    INSERTION_SORT = "insertion_sort"
    QUICKSORT = "quicksort"

    # strings
    KMP_MATCHER = "kmp_matcher"
    NAIVE_STRING_MATCHER = "naive_string_matcher"
