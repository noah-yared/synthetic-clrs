from .problem_generator import ProblemGenerator

class DynamicProgrammingGenerator(ProblemGenerator):
    def __init__(self, min_sequence_length=5, max_sequence_length=15, min_char=0, max_char=3, min_keys=2, max_keys=5, seed=None):
        super().__init__(seed)
        self.min_sequence_length = min_sequence_length
        self.max_sequence_length = max_sequence_length
        self.min_char = min_char
        self.max_char = max_char
        self.min_keys = min_keys
        self.max_keys = max_keys


    def _gen_matrix_chain_prob(self):
        raise NotImplementedError("omitting this algorithm...")


    def _gen_lcs_length_prob(self):
        seq_length = self.rng.gen_int(self.min_sequence_length, self.max_sequence_length)
        string_a = self.rng.gen_int_array(seq_length, self.min_char, self.max_char)
        string_b = self.rng.gen_int_array(seq_length, self.min_char, self.max_char)
        return string_a, string_b


    def _gen_optimal_bst_prob(self):
        num_keys = self.rng.gen_int(self.min_keys, self.max_keys)
        # be careful that n_decimals is large enough relative
        # to num_keys (so that distribution is not too sparse)
        random_prob_dist = self.rng.gen_random_discrete_distribution(2 * num_keys + 1, n_decimals=2)
        ps = random_prob_dist[1::2]
        qs = random_prob_dist[::2]
        return {
            "ps": ps,
            "qs": qs
        }

    
    def generate(self, id):
        generator_fns = [
            self._gen_lcs_length_prob,
            self._gen_optimal_bst_prob,
            # self._gen_matrix_chain_prob,
        ]
        assert 0 <= id < len(generator_fns), "id is out of range!"
        return generator_fns[id]()
