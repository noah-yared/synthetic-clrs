from ..utils import Rng
from ..algorithms import Algorithm

class SearchGenerator:
    def __init__(self, rng=None, min_num_elements=5, max_num_elements=15, min_element=-100, max_element=100, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_num_elements = min_num_elements
        self.max_num_elements = max_num_elements
        self.min_element = min_element
        self.max_element = max_element


    def generate_binary_search_problem(self):
        num_elements = self.rng.gen_int(self.min_num_elements, self.max_num_elements)
        arr = list(sorted(self.rng.gen_int_array(num_elements, self.min_element, self.max_element)))
        target_idx = self.rng.gen_int(0, num_elements-1)
        return {
            "array": arr,
            "target": arr[target_idx],
            "task": "Find the index of target in the array"
        }
    

    def generate_minimum_problem(self):
        num_elements = self.rng.gen_int(self.min_num_elements, self.max_num_elements)
        arr = self.rng.gen_int_array(num_elements, self.min_element, self.max_element)
        return {
            "array": arr,
            "task": "Find the minimum element of the array"
        }


    def generate_quickselect_problem(self):
        raise NotImplementedError("omitting this algorithm for now...")


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.BINARY_SEARCH: self.generate_binary_search_problem,
            Algorithm.MINIMUM: self.generate_minimum_problem,
        }[algorithm](**kwargs)