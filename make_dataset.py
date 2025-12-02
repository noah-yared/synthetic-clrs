import json
import re
from pathlib import Path

from synthetic_clrs import (
    ProblemGenerator,
    ProblemSolver,
    Algorithm,
    Category,
    ALGORITHMS_BY_CATEGORY,
    ALGORITHM_TO_CATEGORY
)


class CLRSDataset:
    def __init__(self, save_dir=None):
        self.data = []
        self.generator = ProblemGenerator()
        self.solver = ProblemSolver()
        self.save_dir = self._ensure_dir(save_dir or "datasets")


    def _compact_json(self, obj, flag=re.DOTALL):
        # make list items space-separated instead of newline-separated
        def collapse_array(match):
            return re.sub(r"\s+", " ", match.group(0), flags=re.DOTALL)
        return re.sub(r"\[(?!\s*[\{\[]).*?\]", collapse_array, obj, flags=re.DOTALL)    


    def _ensure_dir(self, dir):
        dirpath = (Path(__file__).parent / dir)
        dirpath.mkdir(exist_ok=True)
        return dirpath


    def _insert_problem(self, algorithm):
        question = self.generator.generate_problem(algorithm)
        answer = self.solver.solve(algorithm, **question)
        self.data.append({
            "algo_name": algorithm,
            "question": question,
            "answer": answer,
        })


    def generate(self, num_probs_per_algo=100, save_file="synthetic_clrs_dataset.json"):
        for algo in ALGORITHM_TO_CATEGORY.keys():
            for _ in range(num_probs_per_algo):
                self._insert_problem(algo)
        
        with open(self.save_dir / save_file, "w") as f:
            f.write(self._compact_json(json.dumps(self.data, indent=4)))

        print(
            f"Saved generated dataset of "
            f"{len(list(ALGORITHM_TO_CATEGORY.keys())) * num_probs_per_algo} "
            f"problems to the path {self.save_dir / save_file}"
        )


    def load(self, save_file="synthetic_clrs_dataset.json"):
        with open(self.save_dir / save_file, "r") as f:
            self.data = json.load(f)


if __name__ == "__main__":
    dataset = CLRSDataset()
    dataset.generate(num_probs_per_algo=100, save_file="synthetic_clrs_dataset.json")
    dataset.load(save_file="synthetic_clrs_dataset.json")
