class DynamicProgrammingSolver:
    def __init__(self):
        pass

    
    @staticmethod
    def _matrix_chain_solver():
        raise NotImplementedError("omitting this algorithm for now...")


    def _lcs_length_solver(a, b):
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


    def _optimal_bst_solver(ps, qs):
        num_keys = len(ps)

        # initialize dp table (1-indexed)
        dp = [[0 for i in range(num_keys + 1)] for j in range(num_keys + 1)]

        # fill base cases
        for i in range(num_keys):
            dp[i+1][i] = qs[i] # probability target is in gap between keys i, i+1

        # fill in dp table
        for i in range(1, num_keys + 1):
            for j in range(i, num_keys + 1):
                w_ij = sum((ps[k] for k in range(i - 1, j))) \
                     + sum((qs[k] for k in range(i - 1, j + 1)))
                dp[i][j] = min([
                    dp[i][r - 1] + dp[r + 1][j] + w_ij
                    for r in range(i, j + 1)
                ])
        
        # return full dp table and the answer
        return dp, dp[1][num_keys]


    @staticmethod
    def solve(id, **kwargs):
        solvers = [
            DynamicProgrammingSolver._matrix_chain_solver,
            DynamicProgrammingSolver._lcs_length_solver,
            DynamicProgrammingSolver._optimal_bst_solver,
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[id](**kwargs)
