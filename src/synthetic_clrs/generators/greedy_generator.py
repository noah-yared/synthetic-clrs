from ..utils import Rng
from ..algorithms import Algorithm

class GreedyGenerator:
    def __init__(self, rng=None, min_input_size=5, max_input_size=10, min_time=0, max_time=10, min_weight=1, max_weight=10, seed=None):
        self.rng = rng if rng is not None else Rng(seed)
        self.min_time = min_time
        self.max_time = max_time
        self.min_input_size = min_input_size
        self.max_input_size = max_input_size
        self.min_weight = min_weight
        self.max_weight = max_weight


    def generate_activity_selection_problem(self):
        num_tasks = self.rng.gen_int(self.min_input_size, self.max_input_size)

        # generate start times
        start_times = self.rng.gen_int_array(num_tasks, self.min_time, self.max_time-1)
        finish_times = [ # make sure finish times are after start times
            self.rng.gen_int(start+1, self.max_time)
            for start in start_times
        ]

        return {
            "start": start_times,
            "finish": finish_times,
            "task": "Select the maximum number of non-overlapping activities"
        }


    def generate_task_scheduling_problem(self):
        num_tasks = self.rng.gen_int(self.min_input_size, self.max_input_size)
        # generate deadlines for tasks
        deadlines = self.rng.gen_int_array(num_tasks, self.min_time, self.max_time)
        weights = self.rng.gen_int_array(num_tasks, self.min_weight, self.max_weight)
        return {
            "deadlines": deadlines,
            "weights": weights,
            "task": "Schedule tasks to maximize the total weight of the tasks scheduled by their deadline"
        }  


    def generate_problem(self, algorithm: Algorithm, **kwargs):
        return {
            Algorithm.TASK_SCHEDULING: self.generate_task_scheduling_problem,
            Algorithm.ACTIVITY_SELECTION: self.generate_activity_selection_problem,
        }[algorithm](**kwargs)