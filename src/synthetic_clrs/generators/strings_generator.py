from .problem_generator import ProblemGenerator

class StringsGenerator(ProblemGenerator):
    def __init__(self, min_string_length=5, max_string_length=20, min_char=0, max_char=3, seed=None):
        super().__init__(seed)
        self.min_string_length = min_string_length
        self.max_string_length = max_string_length
        self.min_char = min_char
        self.max_char = max_char


    def _generate_string_matcher_prob(self):
        text_length = self.rng.gen_int(self.min_string_length, self.max_string_length)
        pattern_length = self.rng.gen_int(self.min_string_length, text_length)

        text = self.rng.gen_int_array(text_length, self.min_char, self.max_char)
        pattern = self.rng.gen_int_array(pattern_length, self.min_char, self.max_char)

        return {
            "text": text,
            "pattern": pattern
        }
        

    def generate(self):
        return self._generate_string_matcher_prob()