from ..utils.rng_utils import Rng

class ProblemGenerator():
    def __init__(self, seed):
        self.rng = Rng(seed)


    def generate(self, *args, **kwargs):
        raise NotImplementedError("Implement in base class")