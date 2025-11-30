from .problem_generator import ProblemGenerator

class GreedyGenerator(ProblemGenerator):
    def __init__(self, min_input_size=5, max_input_size=15, min_time=0, max_time=1000, min_weight=1, max_weight=10, seed=None):
        super().__init__(seed)
        self.min_time = min_time
        self.max_time = max_time
        self.min_input_size = min_input_size
        self.max_input_size = max_input_size


    def _generate_activity_selection_prob(self):
        num_tasks = self.rng.gen_int(self.min_input_size, self.max_input_size)

        # generate start times
        start_times = self.rng.gen_int_array(num_tasks, self.min_time, self.max_time-1)
        finish_times = [ # make sure finish times are after start times
            self.rng.gen_int(start+1, self.max_time)
            for start in start_times
        ]

        return {
            "start": start_times,
            "finish": finish_times
        }


    def _generate_task_scheduling_prob(self):
        num_tasks = self.rng.gen_int(self.min_input_size, self.max_input_size)
        # generate deadlines for tasks
        deadlines = self.rng.gen_int_array(num_tasks, self.min_time, self.max_time)
        weights = self.rng.gen_int_array(num_tasks, self.min_weight, self.max_weight)
        return {
            "deadlines": deadlines,
            "weights": weights
        }  

    
    def generate(self, id):
        generator_fns = [
            self._generate_activity_selection_prob,
            self._generate_task_scheduling_prob,
        ]
        assert id >= 0 and id < len(generator_fns), "id out of range!"
        return generator_fns[id]()

