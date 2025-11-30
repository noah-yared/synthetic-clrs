from .problem_generator import ProblemGenerator

class SearchGenerator(ProblemGenerator):
    def __init__(self, min_length=10, max_length=32, min_element=-1000, max_element=1000, seed=None):
        super().__init__(seed)
        self.min_length = min_length
        self.max_length = max_length
        self.min_element = min_element
        self.max_element = max_element


    def _generate_binary_search_prob(self):
        arr_size = self.rng.gen_int(self.min_length, self.max_length)
        sorted_arr = list(sorted(self.rng.gen_int_array(arr_size, self.min_element, self.max_element)))
        random_idx = self.rng.gen_int(0, arr_size-1)
        return {
            "arr": sorted_arr,
            "target": sorted_arr[random_idx]
        }
    

    def _generate_minimum_prob(self):
        arr_size = self.rng.gen_int(self.min_length, self.max_length)
        return self.rng.gen_int_array(arr_size, self.min_element, self.max_element)


    def _generate_quickselect_prob(self):
        # arr_size = self.rng.gen_int(self.min_length, self.max_length)
        # return self.rng.gen_int_array(arr_size, self.min_element, self.max_element)
        raise NotImplementedError("omitting this algorithm...")


    def generate(self, id):
        generators = [
            self._generate_binary_search_prob,
            self._generate_minimum_prob,
            self._generate_quickselect_prob
        ]
        assert 0 <= id < len(generators)
        return generators[id]()
        