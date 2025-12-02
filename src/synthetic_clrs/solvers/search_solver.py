class SearchSolver:
    @staticmethod
    def binary_search(array, target, **_):
        l, r = 0, len(array)

        while l < r:
            mid = (l + r) // 2
            if array[mid] == target:
                return mid
            if array[mid] < target:
                l = mid + 1
            else:
                r = mid
        
        return -1
        

    @staticmethod
    def minimum(array, **_):
        if not array:
            raise ValueError(f"Input {array} is empty!")
        return min(array)

    
    @staticmethod
    def quickselect(array, **_):
        raise NotImplementedError("omitting this algorithm for now...")
