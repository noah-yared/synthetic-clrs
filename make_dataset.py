import json
import pandas as pd
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
    def __init__(self, save_file=None):
        self.df = pd.DataFrame(columns=["algo_name", "input", "answer"])
        self.generator = ProblemGenerator()
        self.solver = ProblemSolver()
        self.save_path = (
            self._ensure_dir("datasets")
            / (save_file or "synthetic_clrs_dataset.parquet")
        )


    def _ensure_dir(self, dir):
        dirpath = (Path(__file__).parent / dir)
        dirpath.mkdir(exist_ok=True)
        return dirpath


    def _insert_problem(self, algorithm):
        question = self.generator.generate_problem(algorithm)
        answer = self.solver.solve(algorithm, **question)
        self.df.loc[len(self.df)] = {
            "algo_name": algorithm,
            "question": question,
            "answer": answer,
        }


    def generate(self, num_probs_per_algo=1000, save_file="synthetic_clrs_dataset.parquet"):
        for algo in ALGORITHM_TO_CATEGORY.keys():
            for _ in range(num_probs_per_algo):
                self._insert_problem(algo)
        
        self.df.to_parquet(self.save_path)
        print(
            f"Saved generated dataset of "
            f"{len(list(ALGORITHM_TO_CATEGORY.keys())) * num_probs_per_algo} "
            f"problems to the path {self.save_path}"
        )


if __name__ == "__main__":
    dataset = CLRSDataset()
    dataset.generate(num_probs_per_algo=1000)
