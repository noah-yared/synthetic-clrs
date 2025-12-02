class GreedySolver:
    @staticmethod
    def task_scheduling(deadlines, weights, **_):
        tasks = list(zip(deadlines, weights))
        sorted_task_ids = list(sorted(range(len(tasks)), key=lambda i: tasks[i][1], reverse=True))

        taken_slots = set()
        selected = [0] * len(tasks)

        for task_id in sorted_task_ids:
            deadline, _ = tasks[task_id]
            # find an open slot
            slot = deadline
            while slot >= 1 and slot in taken_slots:
                slot -= 1
            if slot == 0:
                # no valid slot found
                continue
            taken_slots.add(slot)
            selected[task_id] = 1

        return selected


    @staticmethod
    def activity_selection(start, finish, **_):
        times = list(zip(start, finish))
        sorted_activity_ids = list(sorted(range(len(times)), key=lambda i: times[i][1]))
        selected = [0] * len(times)

        prev_end = float('-inf')
        for activity_id in sorted_activity_ids:
            # skip overlapping intervals
            if times[activity_id][0] < prev_end:
                continue
            prev_end = times[activity_id][1]
            selected[activity_id] = 1
        
        return selected
