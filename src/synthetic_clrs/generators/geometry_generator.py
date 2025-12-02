from ..utils import Rng
from ..algorithms import Algorithm

class GeometryGenerator:
    def __init__(self, rng=None, min_num_points=5, max_num_points=20, min_coordinate=-10, max_coordinate=10, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_num_points = min_num_points
        self.max_num_points = max_num_points
        self.min_coordinate = min_coordinate
        self.max_coordinate = max_coordinate


    def _generate_random_segment(self):
        # generate distinct endpoints by randomly
        # choosing x or y coordinate to be strictly
        # distinct on endpoint
        heads = self.rng.gen_bool()
        tails = not heads

        x1, x2 = self.rng.gen_int_array(2, self.min_coordinate, self.max_coordinate, distinct=heads)
        y1, y2 = self.rng.gen_int_array(2, self.min_coordinate, self.max_coordinate, distinct=tails)

        return [(x1, y1), (x2, y2)]


    def _generate_random_points(self, num_points):
        xs = self.rng.gen_int_array(num_points, self.min_coordinate, self.max_coordinate)
        ys = self.rng.gen_int_array(num_points, self.min_coordinate, self.max_coordinate)

        return {
            "xs": xs,
            "ys": ys
        }


    def _generate_convex_hull_problem(self):
        num_points = self.rng.gen_int(self.min_num_points, self.max_num_points)
        random_points = self._generate_random_points(num_points)
        return {
            **random_points,
            "task": "Find the convex hull of the given points"
        }


    def generate_graham_scan_problem(self):
        return self._generate_convex_hull_problem()


    def generate_jarvis_march_problem(self):
        return self._generate_convex_hull_problem()

    
    def generate_segment_intersect_problem(self):
        segments = self._generate_random_segment() + self._generate_random_segment()
        return {
            "xs": [x for x, _ in segments],
            "ys": [y for _, y in segments],
            "task": "Determine whether the two line segments intersect"
        }


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.GRAHAM_SCAN: self.generate_graham_scan_problem,
            Algorithm.JARVIS_MARCH: self.generate_jarvis_march_problem,
            Algorithm.SEGMENT_INTERSECT: self.generate_segment_intersect_problem,
        }[algorithm](**kwargs)
