import numpy as np

class Rng:
    def __init__(self, seed=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()


    def _make_prob_dist(self, size, exclude_indices=()):
        arr = np.ones(size)
        arr[list(exclude_indices)] = 0
        return arr / (size - len(exclude_indices))


    def _gen_input(self, shape, min_int, max_int, exclude=(), distinct=False):
        sample_size = np.array(shape, dtype=np.int64).prod().item()
        pop_size = max_int - min_int + 1

        if distinct and sample_size > pop_size:
            raise ValueError(
                f"Sampling set ({pop_size}) must be at least the size of the "
                f"input to generate ({sample_size})."
            )

        # uniform distribution over the non-excluded ints in [min_int, max_int]
        prob_dist = self._make_prob_dist(
            pop_size,
            exclude_indices=tuple(
                exc - min_int for exc in exclude
            )
        )

        # sample random indices
        random_indices = self.rng.choice(
            pop_size,
            sample_size,
            replace=(not distinct),
            p=prob_dist
        )

        return np.array(range(min_int, max_int + 1))[random_indices].reshape(shape)

    
    def gen_random_integer_partition(self, num):
        partition = [0] * num
        for _ in range(num):
            partition[self.gen_int(0, num - 1)] += 1
        return [n for n in partition if n != 0]


    def gen_int(self, min_int, max_int, **kwargs):
        return self._gen_input(tuple(), min_int, max_int, **kwargs).tolist()


    def gen_bool(self, **kwargs):
        return bool(self.gen_int(0, 1, **kwargs))


    def gen_int_array(self, length, min_int, max_int, **kwargs):
        return self._gen_input((length,), min_int, max_int, **kwargs).tolist()


    def gen_bool_array(self, length, **kwargs):
        return self.gen_int_array(length, 0, 1, **kwargs)


    def gen_int_grid(self, rows, cols, min_int, max_int, **kwargs):
        return self._gen_input((rows, cols), min_int, max_int, **kwargs).tolist()


    def gen_bool_grid(self, rows, cols, **kwargs):
        return self.gen_int_grid(rows, cols, 0, 1, **kwargs)


    def gen_random_discrete_distribution(self, num_buckets, n_decimals=2):
        random_arr = self._gen_input((num_buckets,), 1, 100)
        random_prob_dist = random_arr / random_arr.sum()

        # round to n_decimals decimal places
        rounded_prob_dist = np.round(random_prob_dist, decimals=n_decimals)

        # make distribution sum to 1 (which may not have been preserved after rounding)
        epsilon = np.round(1 - rounded_prob_dist.sum(), decimals=n_decimals)
        random_idx = self.gen_int(0, num_buckets-1)
        rounded_prob_dist[random_idx] = np.round(rounded_prob_dist[random_idx] + epsilon, decimals=n_decimals)

        return rounded_prob_dist.tolist()
