from ..utils import Rng
from ..algorithms import Algorithm

class DynamicProgrammingGenerator:
    def __init__(self, rng=None, min_sequence_length=2, max_sequence_length=8, min_char=0, max_char=3, min_keys=2, max_keys=5, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_sequence_length = min_sequence_length
        self.max_sequence_length = max_sequence_length
        self.min_char = min_char
        self.max_char = max_char
        self.min_keys = min_keys
        self.max_keys = max_keys


    def generate_matrix_chain_problem(self):
        raise NotImplementedError("omitting this algorithm...")


    def generate_lcs_length_problem(self):
        seq_length = self.rng.gen_int(self.min_sequence_length, self.max_sequence_length)
        a = self.rng.gen_int_array(seq_length, self.min_char, self.max_char)
        b = self.rng.gen_int_array(seq_length, self.min_char, self.max_char)
        return {
            "sequence_a": a,
            "sequence_b": b,
            "task": "Find the length of the longest common subsequence of the two sequences"
        }


    def generate_optimal_bst_problem(self):
        num_keys = self.rng.gen_int(self.min_keys, self.max_keys)
        # make sure n_decimals is large enough relative
        # to num_keys (so that distribution is not too sparse)
        import math
        n_decimals = math.floor(math.log10(num_keys)) + 2
        random_prob_dist = self.rng.gen_random_discrete_distribution(2 * num_keys + 1, n_decimals=n_decimals)
        ps = random_prob_dist[1::2]
        qs = random_prob_dist[::2]
        return {
            "key_probabilities": ps,
            "gap_probabilities": qs,
            "decimal_places": n_decimals,
            "task": "Compute the minimum expected search cost for an optimal binary search tree given key and gap probabilities"
        }
 

    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.LCS_LENGTH: self.generate_lcs_length_problem,
            Algorithm.OPTIMAL_BST: self.generate_optimal_bst_problem,
        }[algorithm](**kwargs)
