from ..utils import Rng
from ..algorithms import Algorithm

class StringsGenerator:
    def __init__(self, rng=None, min_string_length=3, max_string_length=8, min_char=0, max_char=3, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_string_length = min_string_length
        self.max_string_length = max_string_length
        self.min_char = min_char
        self.max_char = max_char


    def _generate_string_matcher_problem(self):
        text_length = self.rng.gen_int(self.min_string_length, self.max_string_length)
        pattern_length = self.rng.gen_int(self.min_string_length, text_length)

        text = self.rng.gen_int_array(text_length, self.min_char, self.max_char)
        pattern = self.rng.gen_int_array(pattern_length, self.min_char, self.max_char)

        return {
            "text": text,
            "pattern": pattern,
            "task": "Find the index of the first substring of text that matches pattern"
        }


    def generate_kmp_matcher_problem(self):
        return self._generate_string_matcher_problem()

    
    def generate_naive_string_matcher_problem(self):
        return self._generate_string_matcher_problem()


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.KMP_MATCHER: self.generate_kmp_matcher_problem,
            Algorithm.NAIVE_STRING_MATCHER: self.generate_naive_string_matcher_problem,
        }[algorithm](**kwargs)
