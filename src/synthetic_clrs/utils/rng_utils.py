import numpy as np

class Rng:
    def __init__(self, seed=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()


    def _gen_input(self, shape, min, max):
        num_ints = np.array(shape, dtype=np.int64).prod().item()
        return self.rng.integers(low=min, high=max+1, size=num_ints).reshape(shape)


    def gen_int(self, min, max):
        return self._gen_input(tuple(), min, max).tolist()


    def gen_bool(self):
        return self.gen_int(0, 1)


    def gen_int_array(self, length, min, max):
        return self._gen_input((length,), min, max).tolist()


    def gen_bool_array(self, length):
        return self.gen_int_array(length, 0, 1)


    def gen_int_grid(self, rows, cols, min, max):
        return self._gen_input((rows, cols), min, max).tolist()


    def gen_bool_grid(self, rows, cols):
        return self.gen_int_grid(rows, cols, 0, 1)


    def gen_random_discrete_distribution(self, num_buckets, n_decimals=2):
        random_arr = self._gen_input((num_buckets,), 1, 100)
        random_prob_dist = random_arr / random_arr.sum()

        # round to n_decimals decimal places
        rounded_prob_dist = np.round(random_prob_dist, decimals=n_decimals)

        # make distribution sum to 1 (which may not have been preserved after rounding)
        epsilon = 1 - rounded_prob_dist.sum()
        # epsilon < 0 means we need to subtract, > 0 means add
        increment = (-1 if epsilon < 0 else 1) / (10 ** n_decimals)
        while epsilon:
            random_idx = self.gen_int(0, num_buckets-1)
            rounded_prob_dist[random_idx] += increment
            epsilon -= increment

        return rounded_prob_dist.tolist()
