from ..utils.rng_utils import Rng
from ..algorithms import Algorithm
from ..problem_mappings import ALGORITHM_TO_CATEGORY, Category
from .greedy_generator import GreedyGenerator
from .divide_conquer_generator import DivideConquerGenerator
from .dynamic_programming_generator import DynamicProgrammingGenerator
from .geometry_generator import GeometryGenerator
from .graphs_generator import GraphsGenerator
from .search_generator import SearchGenerator
from .sorting_generator import SortingGenerator
from .strings_generator import StringsGenerator

class ProblemGenerator():
    def __init__(self, seed=None):
        rng = Rng(seed)
        self.generators = {
            Category.GREEDY: GreedyGenerator(rng=rng),
            Category.DIVIDE_CONQUER: DivideConquerGenerator(rng=rng),
            Category.DYNAMIC_PROGRAMMING: DynamicProgrammingGenerator(rng=rng),
            Category.GEOMETRY: GeometryGenerator(rng=rng),
            Category.GRAPHS: GraphsGenerator(rng=rng),
            Category.SEARCH: SearchGenerator(rng=rng),
            Category.SORTING: SortingGenerator(rng=rng),
            Category.STRINGS: StringsGenerator(rng=rng),
        }


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        problem_generator = self.generators[ALGORITHM_TO_CATEGORY[algorithm]]
        return problem_generator.generate_problem(algorithm, **kwargs)
