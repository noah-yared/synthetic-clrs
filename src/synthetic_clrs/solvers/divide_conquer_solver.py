class DivideConquerSolver:
    def __init__(self):
        pass

    
    @staticmethod
    def _max_subarray_solver(arr):
        if not arr:
            raise ValueError(f"Input {arr} is empty!")

        def best_cross_subarray(i, j):
            mid = (i + j) // 2

            # initialize to smallest cross subarray
            curr_best_cross_sum = arr[mid] + arr[mid + 1]
            curr_best_cross_range = (mid, mid + 1)

            # extend left to maximize cross subarray sum
            cross_sum_so_far = curr_best_cross_sum
            for l in range(mid - 1, -1, -1):
                cross_sum_so_far += arr[l]
                if cross_sum_so_far > curr_best_cross_sum:
                    curr_best_cross_sum += cross_sum_so_far
                    curr_best_cross_range = (l, curr_best_cross_range[1])

            # extend right to maximize cross subarray sum
            cross_sum_so_far = curr_best_cross_sum
            for r in range(mid + 2, j + 1):
                cross_sum_so_far += arr[r]
                if cross_sum_so_far > curr_best_cross_sum:
                    curr_best_cross_sum += cross_sum_so_far
                    curr_best_cross_range = (curr_best_cross_range[0], r)

            return curr_best_cross_range, curr_best_cross_sum

        def subproblem(i, j):
            if i == j:
                return (i, j), arr[i]

            mid = (i + j) // 2

            left_solution = subproblem(i, mid)
            right_solution = subproblem(mid + 1, j)
            cross_solution = best_cross_subarray(i, j)

            return max(
                [left_solution, right_solution, cross_solution],
                key=lambda e: e[1] # weigh by subarray sum
            )

        subarray_range, _ = subproblem(0, len(arr) - 1)

        return subarray_range


    @staticmethod
    def solve(id, **kwargs):
        solvers = [
            DivideConquerSolver._max_subarray_solver
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[i](**kwargs)
