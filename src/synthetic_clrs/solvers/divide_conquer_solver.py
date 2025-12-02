class DivideConquerSolver:
    @staticmethod
    def kadane(array, **_):
        if not array:
            raise ValueError(f"Input {array} is empty!")

        def best_cross_subarray(i, j):
            if i == j:
                return (i, j), array[i]

            mid = (i + j) // 2

            # initialize to smallest cross subarray
            curr_best_cross_sum = array[mid] + array[mid + 1]
            curr_best_cross_range = (mid, mid + 1)

            # extend left to maximize cross subarray sum
            cross_sum_so_far = curr_best_cross_sum
            for l in range(mid - 1, -1, -1):
                cross_sum_so_far += array[l]
                if cross_sum_so_far > curr_best_cross_sum:
                    curr_best_cross_sum = cross_sum_so_far
                    curr_best_cross_range = (l, curr_best_cross_range[1])

            # extend right to maximize cross subarray sum
            cross_sum_so_far = curr_best_cross_sum
            for r in range(mid + 2, j + 1):
                cross_sum_so_far += array[r]
                if cross_sum_so_far > curr_best_cross_sum:
                    curr_best_cross_sum = cross_sum_so_far
                    curr_best_cross_range = (curr_best_cross_range[0], r)

            return curr_best_cross_range, curr_best_cross_sum

        def subproblem(i, j):
            if i == j:
                return (i, j), array[i]

            mid = (i + j) // 2

            left_solution = subproblem(i, mid)
            right_solution = subproblem(mid + 1, j)
            cross_solution = best_cross_subarray(i, j)

            return max(
                [left_solution, right_solution, cross_solution],
                key=lambda e: e[1] # weigh by subarray sum
            )

        _, max_subarray_sum = subproblem(0, len(array) - 1)

        return max_subarray_sum
