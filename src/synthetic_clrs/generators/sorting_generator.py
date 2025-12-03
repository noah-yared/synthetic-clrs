from ..utils import Rng
from ..algorithms import Algorithm

class SortingGenerator:
    def __init__(self, rng=None, min_num_elements=5, max_num_elements=10, min_element=-100, max_element=100, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_num_elements = min_num_elements
        self.max_num_elements = max_num_elements
        self.min_element = min_element
        self.max_element = max_element


    def _generate_sorting_problem(self):
        num_elements = self.rng.gen_int(self.min_num_elements, self.max_num_elements)
        arr = self.rng.gen_int_array(num_elements, self.min_element, self.max_element)
        return {
            "array": arr,
            "task": "Sort the array in ascending order"
        }


    def generate_bubble_sort_problem(self):
        return self._generate_sorting_problem()


    def generate_heapsort_problem(self):
        return self._generate_sorting_problem()


    def generate_insertion_sort_problem(self):
        return self._generate_sorting_problem()


    def generate_quicksort_problem(self):
        return self._generate_sorting_problem()


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.BUBBLE_SORT: self.generate_bubble_sort_problem,
            Algorithm.HEAPSORT: self.generate_heapsort_problem,
            Algorithm.INSERTION_SORT: self.generate_insertion_sort_problem,
            Algorithm.QUICKSORT: self.generate_quicksort_problem,
        }[algorithm](**kwargs)
