from .problem_generator import ProblemGenerator

class GeometryGenerator(ProblemGenerator):
    def __init__(self, min_num_segments=5, max_num_segments=20, min_coordinate=-10, max_coordinate=10, seed=None):
        super().__init__(seed)
        self.min_num_segments = min_num_segments
        self.max_num_segments = max_num_segments
        self.min_coordinate = min_coordinate
        self.max_coordinate = max_coordinate


    def _generate_segments(self, segment_intersection=False):
        # must have exactly four segments for segment intersection
        num_segments = 4 if segment_intersection else self.rng.gen_int(self.min_num_segments, self.max_num_segments)

        xs = self.rng.gen_int_array(num_segments, self.min_coordinate, self.max_coordinate)
        ys = self.rng.gen_int_array(num_segments, self.min_coordinate, self.max_coordinate)

        return {
            "xs": xs,
            "ys": ys
        }
        

    def generate(self, **kwargs):
        return self._generate_segments(**kwargs)
