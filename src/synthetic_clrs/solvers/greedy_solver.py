class GreedySolver:
    @staticmethod
    def _task_scheduling_solver(deadlines, weights):
        tasks = list(enumerate(zip(deadlines, weights)))
        sorted_tasks = list(sorted(tasks, key=lambda e: e[1][1], reverse=True))

        available_slots = [True] * len(tasks)
        selected = [0] * len(tasks)

        # assign most weighted task
        available_slots[sorted_tasks[0][1][0]] = False
        selected[sorted_tasks[0][0]] = 1

        for i in range(1, len(tasks)):
            task_id, (deadline, _) = tasks[i]
            # find an open slot
            slot = deadline
            while slot >= 0 and not available_slots[slot]:
                slot -= 1
            if slot == -1:
                # no valid slot found
                continue
            available_slots[slot] = False
            selected[task_id] = 1

        return selected


    @staticmethod
    def _activity_selection_solver(start, finish):
        times = list(enumerate(zip(start, finish)))
        sorted_times = list(sorted(times, key=lambda e: e[1][1]))

        selected = [0] * len(times)
        selected[sorted_times[0][0]] = 1

        prev_end = sorted_times[0][1][1]
        for i in range(1, len(times)):
            # skip overlapping intervals
            if times[i][1][0] < prev_end:
                continue
            prev_end = times[i][1][1]
            selected[times[i][0]] = 1
        
        return selected


    def solve(id, **kwargs):
        solvers = [
            GreedySolver._task_scheduling_solver,
            GreedySolver._activity_selection_solver
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[id](**kwargs)