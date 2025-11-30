class SearchSolver:
    @staticmethod
    def _solve_binary_search(arr, target):
        l, r = 0, len(arr)

        while l < r:
            mid = (l + r) // 2
            if arr[mid] == target:
                return mid
            if arr[mid] < target:
                l = mid + 1
            else:
                r = mid
        
        return -1
        

    @staticmethod
    def _solve_minimum(arr):
        if not arr:
            raise ValueError(f"Input {arr} is empty!")
        return min(arr)

    
    @staticmethod
    def _solve_quickselect(arr):
        raise NotImplementedError("omitting this algorithm for now...")

    
    @staticmethod
    def solve(id, **kwargs):
        solvers = [
            SearchSolver._solve_binary_search,
            SearchSolver._solve_minimum,
            SearchSolver._solve_quickselect,
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[id](**kwargs)
