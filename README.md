# Synthetic CLRS Dataset Generator

## Overview
This repository contains a dataset generator for synthetic algorithm problems inspired by CLRS. The current algorithms included in the dataset are split into the following categories:

- Divide and Conquer:
    - KADANE
- Dynamic Programming:
    - LCS_LENGTH
    - OPTIMAL_BST
- Geometry:
    - GRAHAM_SCAN
    - JARVIS_MARCH
    - SEGMENT_INTERSECT
- Graphs:
    - BELLMAN_FORD
    - BFS
    - DAG_SHORTEST_PATH
    - DFS
    - DIJKSTRA
    - TOPOLOGICAL_SORT
- Greedy:
    - TASK_SCHEDULING
    - ACTIVITY_SELECTION
- Search:
    - BINARY_SEARCH
    - MINIMUM
- Sorting: 
    - BUBBLE_SORT
    - HEAPSORT
    - INSERTION_SORT
    - QUICKSORT
- Strings: 
    - KMP_MATCHER
    - NAIVE_STRING_MATCHER

## Dataset Format

The dataset is a JSON file containing of list of records corresponding to a problem. Each problem has the following format:
```python
{
    "algo_name": str,
    "question": dict[str, list[int] | list[float] | int | str],
    "answer": list[int] | list[float] | int | float
}
```

The `algo_name` is the name of the algorithm corresponding to the problem. The `question` is a dictionary containing the input parameters for the problem as well as the task description, which is specific to each algorithm. The `answer` is the expected output of the problem.

### Example
This is an example of a problem in the dataset:

```python
{
    "algo_name": "kadane",
    "question": {
        "array": [1, 2, 3, 4, 5],
        "task": "Find the maximum subarray sum of the array"
    },
    "answer": 15
}
```

## Installation

Clone the repository:
```bash
git clone https://github.com/noah-yared/synthetic-clrs.git
cd synthetic-clrs
```

Install the package:
```bash
pip3 install .
```

For development:

```bash
pip3 install -e ".[dev]"
pytest # run tests
```

## Usage
Once the package is installed, generate the dataset by running the `make_dataset.py` script.
```bash
python3 make_dataset.py
```
By default, this will generate a dataset with 100 problems for each algorithm that will be saved in the `datasets` directory with the filename `synthetic_clrs_dataset.json`. To modify the number of problems generated per algorithm, or the save path, see below:
```python
if __name__ == "__main__":
    dataset = CLRSDataset(save_dir="datasets")
    dataset.generate(num_probs_per_algo=100, save_file="synthetic_clrs_dataset.json")
```

A previously saved dataset can also be loaded as follows. By default, the dataset will be loaded from the `datasets` directory with the name `synthetic_clrs_dataset.json` unless another directory/filename is specified in the script:
```python
if __name__ == "__main__":
    dataset = CLRSDataset(save_dir="datasets")
    dataset.load(save_file="synthetic_clrs_dataset.json")
    print(dataset.data)
```
