import pytest
import itertools

from synthetic_clrs import (
    Algorithm,
    ALGORITHMS_BY_CATEGORY,
    Category,
    ProblemSolver,
)


EPSILON = 1e-6

def assert_close(a, b, epsilon=EPSILON):
    assert abs(a - b) < epsilon, f"Expected {a} to be close to {b} within {epsilon}!"


################################
### Divide and Conquer Tests ###
################################

TEST_KADANE_INPUTS = [
    ([1, 2, 3, 4, 5], 15),
    ([-1, -2, -3, -4, -5], -1),
    ([1, -2, 3, -4, 5], 5),
    ([1, -2, 3, -4, 5, -6, 7, -8, 9, -5, 6, 5, -4, 8, -7, 6, -5, 4, -3, 2, -1, 1], 19),
    ([1000, -999, 1000], 1001),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_KADANE_INPUTS)
def test_kadane(test_input, expected_output):
    assert ProblemSolver.solve(Algorithm.KADANE, arr=test_input) == expected_output


############################
### Strings Tests ###
############################

TEST_STRING_MATCHER_INPUTS = [
    # no matches
    (("abc", "ac"), -1),
    (("abcd", "abd"), -1),
    # single match
    (("a", "a"), 0),
    (("ab", "b"), 1),
    (("abcde", "cde"), 2),
    # multiple matches
    (("ababababab", "ab"), 0),
    (("xyzbababab", "aba"), 4),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_STRING_MATCHER_INPUTS)
def test_kmp_matcher(test_input, expected_output):
    test, pattern = test_input
    assert ProblemSolver.solve(Algorithm.KMP_MATCHER, text=test, pattern=pattern) == expected_output

@pytest.mark.parametrize("test_input, expected_output", TEST_STRING_MATCHER_INPUTS)
def test_naive_string_matcher(test_input, expected_output):
    text, pattern = test_input
    assert ProblemSolver.solve(Algorithm.NAIVE_STRING_MATCHER, text=text, pattern=pattern) == expected_output


#################################
### Dynamic Programming Tests ###
#################################

TEST_LCS_LENGTH_INPUTS = [
    # no common subsequence
    (("abc", "def"), 0),
    (("abcdef", "ghijkl"), 0),
    # same string
    (("abc", "abc"), 3),
    # multiple matching subsequences
    (("abcb", "acb"), 3),
    (("cbcadef", "acbdef"), 5),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_LCS_LENGTH_INPUTS)
def test_lcs_length(test_input, expected_output):
    a, b = test_input
    _, lcs_length = ProblemSolver.solve(Algorithm.LCS_LENGTH, a=a, b=b)
    assert lcs_length == expected_output

TEST_OPTIMAL_BST_INPUTS = [
    # single key
    (((1/2,), (0.0, 1/2)), 1.5),
    # multiple keys
    (((34/92, 8/92, 50/92), (0, 0, 0, 0)), 142/92),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_OPTIMAL_BST_INPUTS)
def test_optimal_bst(test_input, expected_output):
    ps, qs = test_input
    _, optimal_bst_cost = ProblemSolver.solve(Algorithm.OPTIMAL_BST, ps=ps, qs=qs)
    assert_close(optimal_bst_cost, expected_output)


######################
### Geometry Tests ###
######################

TEST_CONVEX_HULL_INPUTS = [
    # single point
    (([1], [1]), [1]),
    # simple square
    (
        (
            [0, 4, 4, 0],
            [0, 0, 4, 4],
        ),
        [1, 1, 1, 1]
    ),
    # triangle with collinear points
    (
        (
            [0, 2, 4, 2],
            [0, 0, 0, 3],
        ),
        [1, 0, 1, 1]
    ),
    # pentagon
    (
        (
            [0, 3, 4, 2, -1],
            [0, -1, 2, 4, 2],
        ),
        [1, 1, 1, 1, 1]
    ),
    # points with interior points
    (
        (
            [0, 1, 0.8, 0.6, 0],
            [0, 0, 0.1, 0.15, 1],
        ),
        [1, 1, 0, 0, 1]
    ),
    # multiple collinear points
    (
        (
            [0, 1, 2, 3],
            [0, 1, 2, 3],
        ),
        [1, 0, 0, 1] # only endpoints on hull
    ),
    # multiple non-collinear points
    (
        (
            [0, 1, -1, -5, -3, -1, -2, -1, -2, -1],
            [0, -4, -5, -3, -1, -3, -2, -1, -1, 1]
        ),
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 1]
    ),

]
@pytest.mark.parametrize("test_input, expected_output", TEST_CONVEX_HULL_INPUTS)
def test_graham_scan(test_input, expected_output):
    xs, ys = test_input
    selected = ProblemSolver.solve(Algorithm.GRAHAM_SCAN, xs=xs, ys=ys)
    print(f"selected {sum(selected)} points")
    print("selected:", selected)
    print("expected:", expected_output)
    assert selected == expected_output

@pytest.mark.parametrize("test_input, expected_output", TEST_CONVEX_HULL_INPUTS)
def test_jarvis_march(test_input, expected_output):
    xs, ys = test_input
    selected = ProblemSolver.solve(Algorithm.JARVIS_MARCH, xs=xs, ys=ys)
    print(f"selected {sum(selected)} points")
    print("selected:", selected)
    print("expected:", expected_output)
    assert selected == expected_output

TEST_SEGMENT_INTERSECT_INPUTS = [
    # diagonal intersection
    (([0, 2, 0, 2], [0, 2, 2, 0]), 1),
    # diagonal intersection
    (([-1, 1, -1, 1], [-1, 1, 1, -1]), 1),
    # parallel segments
    (([0, 1, 2, 3], [0, 1, 0, 1]), 0),
    # segments would intersect if extended but dont touch
    (([0, 2, 1/2, 2], [0, 2, -1/2, 0]), 0),
    # endpoint of a segment is on another segment
    (([0, 2, 1, 1], [0, 0, 0, 2]), 1),
    # segments share endpoint
    (([0, 1, 1, 2], [0, 1, 1, 0]), 1),
    # collinear segments, dont touch
    (([0, 1, 2, 3], [0, 1, 2, 3]), 0),
    # collinear segments, one endpoint inside other
    (([0, 2, 1, 3], [0, 2, 1, 3]), 1),
    # collinear segments, both endpoints inside other
    (([0, 3, 1, 2], [0, 3, 1, 2]), 1),
    # duplicate segment
    (([0, 1, 0, 1], [0, 1, 0, 1]), 1),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_SEGMENT_INTERSECT_INPUTS)
def test_segment_intersect(test_input, expected_output):
    xs, ys = test_input
    assert ProblemSolver.solve(Algorithm.SEGMENT_INTERSECT, xs=xs, ys=ys) == expected_output


####################
### Graphs Tests ###
####################

TEST_TREE_INPUTS = [
    # single vertex
    (
        (
            [],
            1,
            0
        ),
        [0]
    ),
    # tree without branching
    (
        # 0 <-> 1 <-> 2
        (
            [
                ((0, 1), 1),
                ((1, 2), 1),
            ],
            3,
            0
        ),
        [0, 0, 1]
    ),
    # tree with branching
    (
        # 4
        # | \ 
        # 1  3
        # | \
        # 2  0
        (
            [
                ((4, 1), 1),
                ((1, 2), 1),
                ((4, 3), 1),
                ((1, 2), 1),
                ((1, 0), 1),
            ],
            5,
            4
        ),
        [1, 4, 1, 4, 4]
    ),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_TREE_INPUTS)
def test_bfs(test_input, expected_output):
    edges, num_vertices, src = test_input
    parents = ProblemSolver.solve(Algorithm.BFS, edges=edges, num_vertices=num_vertices, src=src)
    assert parents == expected_output

@pytest.mark.parametrize("test_input, expected_output", TEST_TREE_INPUTS)
def test_dfs(test_input, expected_output):
    edges, num_vertices, src = test_input
    parents = ProblemSolver.solve(Algorithm.DFS, edges=edges, num_vertices=num_vertices, src=src)
    assert parents == expected_output

TEST_DAGS = [
    # single vertex
    ((), 1, 0),
    # dag with all reachable vertices from src
    # 2 <- 0 -> 1 -> 3
    (
        (
            ((0, 1), 2),
            ((0, 2), 3),
            ((1, 3), 4),
        ),
        4,
        0
    ),
    # dag with all reachable vertices but multiple paths
    # to a vertex with differnt weights
    # 0 -> 2
    # |    |
    # |    V
    # | -> 1
    # |    |
    # |    V
    # | -> 3
    (
        (
            ((0, 1), 3),
            ((0, 2), 1),
            ((0, 3), 5),
            ((1, 3), 1),
            ((2, 1), 1),
        ),
        4,
        0
    ),
    # same dag as above but with a negative weight
    # on the edge from 0 to 1
    (
        (
            ((0, 1), -3),
            ((0, 2), 1),
            ((0, 3), 5),
            ((1, 3), 1),
            ((2, 1), 1),
        ),
        4,
        0
    ),
]

TOPOLOGICAL_ORDERINGS = [
    [0],
    [0, 1, 2, 3],
    [0, 2, 1, 3],
    [0, 2, 1, 3],
]
@pytest.mark.parametrize("test_input, expected_output", zip(TEST_DAGS, TOPOLOGICAL_ORDERINGS))
def test_topological_sort(test_input, expected_output):
    edges, num_vertices, _ = test_input
    topo_order = ProblemSolver.solve(Algorithm.TOPOLOGICAL_SORT, edges=edges, num_vertices=num_vertices)
    assert topo_order == expected_output

DAG_SHORTEST_PATH_DISTANCES = [
    [0],
    [0, 2, 3, 6],
    [0, 2, 1, 3],
    [0, -3, 1, -2],
]
@pytest.mark.parametrize("test_input, expected_output", zip(TEST_DAGS, DAG_SHORTEST_PATH_DISTANCES))
def test_dag_shortest_paths(test_input, expected_output):
    edges, num_vertices, src = test_input
    distances = ProblemSolver.solve(Algorithm.DAG_SHORTEST_PATH, edges=edges, num_vertices=num_vertices, src=src)
    assert distances == expected_output

TEST_GRAPH_INPUTS_ONLY_POSITIVE_WEIGHTS = [
    # single vertex
    ((), 1, 0),
    # tree
    # 0 - 1 - 2
    # | 
    # 3 - 4
    (
        (
            ((0, 1), 1),
            ((1, 2), 2),
            ((0, 3), 1),
            ((3, 4), 3),
        ),
        5,
        0
    ),
    # graph with multiple paths to multiple
    # vertices with different weights
    # 0 - 1 - 2
    # |   |   |
    # 3 - 4 - 5
    (
        (
            ((0, 1), 2),
            ((1, 0), 2),
            ((1, 2), 3),
            ((2, 1), 3),
            ((0, 3), 4),
            ((3, 0), 4),
            ((3, 4), 5),
            ((4, 3), 5),
            ((1, 4), 6),
            ((4, 1), 6),
            ((4, 5), 7),
            ((5, 4), 7),
            ((2, 5), 8),
            ((5, 2), 8),
        ),
        6,
        0
    ),
]

UNDIRECTED_GRAPH_SHORTEST_PATH_DISTANCES = [
    [0],
    [0, 1, 3, 1, 4],
    [0, 2, 5, 4, 8, 13],
]
@pytest.mark.parametrize("test_input, expected_output", zip(TEST_GRAPH_INPUTS_ONLY_POSITIVE_WEIGHTS, UNDIRECTED_GRAPH_SHORTEST_PATH_DISTANCES))
def test_dijkstra_undirected(test_input, expected_output):
    edges, num_vertices, src = test_input
    distances = ProblemSolver.solve(Algorithm.DIJKSTRA, edges=edges, num_vertices=num_vertices, src=src)
    assert distances == expected_output

@pytest.mark.parametrize("test_input, expected_output", zip(TEST_GRAPH_INPUTS_ONLY_POSITIVE_WEIGHTS, UNDIRECTED_GRAPH_SHORTEST_PATH_DISTANCES))
def test_bellman_ford_positive_weights(test_input, expected_output):
    edges, num_vertices, src = test_input
    distances = ProblemSolver.solve(Algorithm.BELLMAN_FORD, edges=edges, num_vertices=num_vertices, src=src)
    assert distances == expected_output

TEST_GRAPH_INPUTS_WITH_NEGATIVE_WEIGHTS = [
    # graph with multiple paths to multiple
    # vertices with different weights and large
    # negative weight in the middle
    # 0 - 1 - 2
    # |   V   |
    # 3 - 4 - 5
    (
        (
            ((0, 1), 2),
            ((1, 0), 2),
            ((1, 2), 7),
            ((2, 1), 7),
            ((0, 3), 4),
            ((3, 0), 4),
            ((3, 4), 5),
            ((4, 3), 5),
            ((1, 4), -10),
            ((4, 5), 7),
            ((5, 4), 7),
            ((2, 5), 8),
            ((5, 2), 8),
        ),
        6,
        0
    ),
]

NEGATIVE_WEIGHT_GRAPH_SHORTEST_PATH_DISTANCES = [
    [0, 2, 7, -3, -8, -1],
]
@pytest.mark.parametrize("test_input, expected_output", zip(TEST_GRAPH_INPUTS_WITH_NEGATIVE_WEIGHTS, NEGATIVE_WEIGHT_GRAPH_SHORTEST_PATH_DISTANCES))
def test_bellman_ford_negative_weights(test_input, expected_output):
    edges, num_vertices, src = test_input
    distances = ProblemSolver.solve(Algorithm.BELLMAN_FORD, edges=edges, num_vertices=num_vertices, src=src)
    assert distances == expected_output


####################
### Greedy Tests ###
####################

TEST_TASK_SCHEDULING_INPUTS = [
    # single task 
    (([1], [1]), [1]),
    # multiple tasks that can all be scheduled
    (([1, 2, 3], [2, 5, 4]), [1, 1, 1]),
    # multiple tasks, some cannot be scheduled
    (([1, 2, 2], [2, 5, 4]), [0, 1, 1]),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_TASK_SCHEDULING_INPUTS)
def test_task_scheduling(test_input, expected_output):
    deadlines, weights = test_input
    selected = ProblemSolver.solve(Algorithm.TASK_SCHEDULING, deadlines=deadlines, weights=weights)
    assert selected == expected_output

TEST_ACTIVITY_SELECTION_INPUTS = [
    # single activity
    (([1], [1]), [1]),
    # multiple activities, all can be selected
    (([1, 4, 8, 6], [3, 5, 9, 7]), [1, 1, 1, 1]),
    # multiple activities, some cannot be selected
    (([1, 2, 3, 5], [6, 5, 4, 7]), [0, 0, 1, 1]),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_ACTIVITY_SELECTION_INPUTS)
def test_activity_selection(test_input, expected_output):
    start, finish = test_input
    selected = ProblemSolver.solve(Algorithm.ACTIVITY_SELECTION, start=start, finish=finish)
    assert selected == expected_output


####################
### Search Tests ###
####################

TEST_BINARY_SEARCH_INPUTS = [
    # single element
    (([1], 1), 0),
    # multiple elements, target at beginning
    ((list(range(1, 10, 3)), 1), 0),
    # multiple elements, target at end
    ((list(range(0, 10, 3)), 9), 3),
    # multiple elements, target in middle
    ((list(range(-10, 10, 2)), 8), 9), 
    ((list(range(100)), 97), 97),
    # target not in array
    ((list(range(1, 10, 3)), 5), -1), 
]
@pytest.mark.parametrize("test_input, expected_output", TEST_BINARY_SEARCH_INPUTS)
def test_binary_search(test_input, expected_output):
    arr, target = test_input
    assert ProblemSolver.solve(Algorithm.BINARY_SEARCH, arr=arr, target=target) == expected_output

TEST_MINIMUM_INPUTS = [
    # single element
    ([1], 1),
    # multiple elements
    ([7, 8, -5, 1, -2], -5),
    ([2, 10, 3, 7, 0], 0),
    ([22, 13, 47, 16, 29, 35], 13),
]
@pytest.mark.parametrize("test_input, expected_output", TEST_MINIMUM_INPUTS)
def test_minimum(test_input, expected_output):
    arr = test_input
    assert ProblemSolver.solve(Algorithm.MINIMUM, arr=arr) == expected_output


#####################
### Sorting Tests ###
#####################

TEST_SORT_ARRAY_INPUTS = [
    # single element
    ([1], [1]),
    # multiple elements, already sorted
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([10, 100, 1000], [10, 100, 1000]),
    # multiple elements, not sorted
    ([7, 8, -5, 1, -2], [-5, -2, 1, 7, 8]),
    ([2, 10, 3, 7, 0], [0, 2, 3, 7, 10]),
    ([22, 13, 47, 16, 29, 35], [13, 16, 22, 29, 35, 47]),
]
SORTING_ALGORITHMS = ALGORITHMS_BY_CATEGORY[Category.SORTING]
TEST_INPUTS_BY_SORTING_ALGORITHM = list(zip(
    SORTING_ALGORITHMS * len(TEST_SORT_ARRAY_INPUTS),
    [test_input for test_input, _ in TEST_SORT_ARRAY_INPUTS] * len(SORTING_ALGORITHMS),
    [expected_output for _, expected_output in TEST_SORT_ARRAY_INPUTS] * len(SORTING_ALGORITHMS),
))
SORTING_TEST_IDS = [f"{algo}_{i}" for i, (algo, *_) in enumerate(TEST_INPUTS_BY_SORTING_ALGORITHM)]

@pytest.mark.parametrize(
    "sorting_algorithm, test_input, expected_output",
    TEST_INPUTS_BY_SORTING_ALGORITHM,
    ids=SORTING_TEST_IDS
)
def test_sort(sorting_algorithm, test_input, expected_output):
    arr = test_input
    assert ProblemSolver.solve(sorting_algorithm, arr=arr) == expected_output
