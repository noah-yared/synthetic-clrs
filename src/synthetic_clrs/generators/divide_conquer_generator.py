from .problem_generator.py import ProblemGenerator

class DivideConquerGenerator(ProblemGenerator):
    def __init__(self, min_array_size=5, max_array_size=15, min_element=-10, max_element=10, seed=None):
        super().__init__(seed)
        self.min_array_size = min_array_size
        self.max_array_size = max_array_size

    
    def _generate_max_subarray_sum_prob(self):
        array_size = self.rng.gen_int(self.min_array_size, self.max_array_size)
        return self.rng.gen_int_array(array_size, self.min_element, self.max_element)
    

    def generate(self):
        return self._generate_max_subarray_sum_prob()
    