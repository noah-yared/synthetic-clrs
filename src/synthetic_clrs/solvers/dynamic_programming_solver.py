class DynamicProgrammingSolver:
    @staticmethod
    def matrix_chain_order(matrices):
        raise NotImplementedError("omitting this algorithm for now...")


    @staticmethod
    def lcs_length(a, b):
        len_a, len_b = tuple(map(len, (a, b)))
        
        # initialize dp table (add dummy row/column 0 to avoid index errors)
        dp = [[0 for _ in range(len_b + 1)] for _ in range(len_a + 1)]
        
        # fill dp table
        for i in range(1, len_a + 1):
            for j in range(1, len_b + 1):
                dp[i][j] = max(
                    dp[i][j-1],
                    dp[i-1][j], # make sure to -1 when indexing a, b since dp is 1-indexed
                    dp[i-1][j-1] + (a[i-1] == b[j-1]) 
                )

        # return full dp table and the answer
        return dp, dp[len_a][len_b]


    @staticmethod
    def optimal_bst(ps, qs):
        if not ps:
            raise ValueError(f"Key probabilities {ps} is empty!")
        
        if len(ps) != len(qs) - 1:
            raise ValueError(f"Length of key probabilities {ps} must be one less than the length of the gap probabilities {qs}!")

        num_keys = len(ps)

        # initialize dp table (1-indexed)
        dp = [[0 for i in range(num_keys + 2)] for j in range(num_keys + 2)]

        # fill base cases
        for i in range(num_keys + 1):
            # use the probability that target
            # is in gap between keys i, i+1
            dp[i+1][i] = qs[i] 

        # fill in dp table in bottom-up manner
        # by considering subproblems with smaller
        # subtree sizes before larger ones so that
        # we can directly use previously computed
        # subproblem solutions
        for sub_tree_size in range(1, num_keys + 1):
            for i in range(1, num_keys - sub_tree_size + 2):
                j = i + sub_tree_size - 1
                w_ij = sum((ps[k] for k in range(i - 1, j))) \
                     + sum((qs[k] for k in range(i - 1, j + 1)))
                dp[i][j] = min([
                    dp[i][r - 1] + dp[r + 1][j] + w_ij
                    for r in range(i, j + 1)
                ])
        
        # return full dp table and the answer
        return dp, dp[1][num_keys]
