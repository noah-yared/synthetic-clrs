class StringsSolver:
    @staticmethod
    def kmp_matcher(text, pattern):
        if not pattern:
            raise ValueError(f"Pattern {pattern} is empty!")

        def compute_lps():
            # lps[i] denotes the length of the
            # longest proper prefix of pattern[0..i]
            # that is also a proper suffix of pattern[0..i]
            # 
            # note: proper prefix/suffix excludes the
            # full substring pattern[0..i]
            lps = [0 for _ in range(len(pattern))]
            for i in range(1, len(pattern)):
                if pattern[i] == pattern[lps[i-1]]:
                    lps[i] += 1
                else:
                    lps[i] = 0
            return lps
        
        # compute longest proper prefix suffix array
        lps = compute_lps()

        i, j = 0, 0
        while i < len(text):
            if text[i] == pattern[j]:
                i += 1
                j += 1
            elif j > 0:
                # failed so backtrack
                i -= j - lps[j-1] - 1
                j = lps[j-1]
            else:
                # failed at start of pattern
                # so just increment text ptr
                i += 1

            # return index of first
            # full pattern match
            if j == len(pattern):
                return i - len(pattern)
        
        return -1


    @staticmethod
    def naive_string_matcher(text, pattern):
        if not pattern:
            raise ValueError(f"Pattern {pattern} is empty!")

        i, j = 0, 0
        while i < len(text):
            if text[i] == pattern[j]:
                i += 1
                j += 1
            else:
                # failed so start at 
                # next possible match
                # start index
                i -= j - 1
                j = 0

            # return index of first
            # full pattern match
            if j == len(pattern):
                return i - len(pattern)
            
        
        return -1
