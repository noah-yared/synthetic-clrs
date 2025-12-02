from ..utils import Rng
from ..algorithms import Algorithm

class DivideConquerGenerator:
    def __init__(self, rng=None, min_array_size=2, max_array_size=10, min_element=-10, max_element=10, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_element = min_element
        self.max_element = max_element
        self.min_array_size = min_array_size
        self.max_array_size = max_array_size

    
    def generate_kadane_problem(self):
        array_size = self.rng.gen_int(self.min_array_size, self.max_array_size)
        arr = self.rng.gen_int_array(array_size, self.min_element, self.max_element)
        return {
            "array": arr,
            "task": "Find the maximum subarray sum of the array"
        }
    

    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.KADANE: self.generate_kadane_problem,
        }[algorithm](**kwargs)
