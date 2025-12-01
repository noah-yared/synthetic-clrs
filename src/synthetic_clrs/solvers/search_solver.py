class SearchSolver:
    @staticmethod
    def binary_search(arr, target):
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
    def minimum(arr):
        if not arr:
            raise ValueError(f"Input {arr} is empty!")
        return min(arr)

    
    @staticmethod
    def quickselect(arr):
        raise NotImplementedError("omitting this algorithm for now...")
