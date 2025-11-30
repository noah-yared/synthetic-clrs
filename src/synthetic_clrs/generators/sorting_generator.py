from .problem_generator import ProblemGenerator

class SortingGenerator(ProblemGenerator):
    def __init__(self, min_length=10, max_length=32, min_element=-1000, max_element=1000, seed=None):
        super().__init__(seed)
        self.min_length = min_length
        self.max_length = max_length
        self.min_element = min_element
        self.max_element = max_element


    def generate(self):
        size = self.rng.gen_int(self.min_length, self.max_length)
        return self.rng.gen_int_array(size, self.min_element, self.max_element)