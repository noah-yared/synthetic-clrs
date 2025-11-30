class StringsSolver:
    def _kmp_match_solver(text, pat):
        def compute_lps():
            # lps[i] denotes the length of the
            # longest proper prefix of pat[0..i]
            # that is also a proper suffix of pat[0..i]
            # 
            # note: proper prefix/suffix excludes the
            # full substring pat[0..i]
            lps = [0 for _ in range(len(pat))]
            for i in range(1, len(pat)):
                if pat[i] == pat[lps[i-1]]:
                    lps[i] += 1
                else:
                    lps[i] = 0
            return lps

        i, j = 0, 0
        while i < len(text):
            # return index of first
            # full pattern match
            if j == len(pat):
                return i - len(pat)

            if text[i] == pat[j]:
                i += 1
                j += 1
            elif j > 0:
                i -= j - lps[j-1] - 1
                j = lps[j-1]
            else:
                # failed at start of pattern
                # so just increment text ptr
                i += 1
        
        return -1


    def _naive_string_match_solver(text, pat):
        i, j = 0, 0
        while i < len(text):
            # return index of first
            # full pattern match
            if j == len(pat):
                return i - len(pat)
            
            if text[i] == pat[j]:
                i += 1
                j += 1
            else:
                # failed so start at 
                # next possible match
                # start index
                i -= j - 1
                j = 0
        
        return -1


    def _solve(id, **kwargs):
        solvers = [
            StringsSolver._kmp_match_solver,
            StringsSolver._naive_string_match_solver
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[id](**kwargs)
