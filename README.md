# PyAssessment
Concolic execution based automatic grading tool for Python functions.

## About This Project
PyAssessment is an automatic grading tool which gives a score to a student implementation based on its semantic similarity with a reference implementation.

This code is a modified version of:
- [PyJudge](https://github.com/Barbariansyah/pyjudge): An automatic grading tool that takes a reference implementation and a student implementation, and finds input(s) that generate a different output.
- [PyExZ3](https://github.com/thomasjball/PyExZ3): A Dynamic Symbolic Execution Engine for Python.

This repository will be the deliverable of my final project.

## Getting Started
1. Make sure you have Python 3.x installed.
2. Install Z3 [here](https://github.com/Z3Prover/z3) or using pip.
```
pip install z3-solver
```
3. For MacOS, open `setup.sh` and change the path according to your local machine then run:
```
. pyjudge/setup.sh
```
4. Try grading something.
```
python grade.py test/max_3/max_3.py test/max_3/max_3_1.py
```
It should return something like this and save the result to `res` folder.
```
Reference: max_3.max_3
Grading: max_3_1.max_3_1
======
RESULT
======

tested: 
{(('a', 0), ('b', 0), ('c', 0)): (0, 0), (('a', 0), ('b', 0), ('c', 1)): (1, 1), (('a', 0), ('b', 2), ('c', 0)): (2, 2), (('a', -1), ('b', 0), ('c', 0)): (0, 0), (('a', 0), ('b', 0), ('c', -1)): (0, -1), (('a', 1), ('b', 2), ('c', 3)): (3, 3), (('a', 1), ('b', 0), ('c', 2)): (2, 2), (('a', 0), ('b', -1), ('c', 0)): (0, 0), (('a', 2), ('b', 0), ('c', 0)): (2, 2), (('a', 4), ('b', 5), ('c', 0)): (5, 5), (('a', 2), ('b', 0), ('c', 8)): (8, 8), (('a', 0), ('b', 1), ('c', 2)): (2, 2)}

tested from path dev or path eq: 
{(('a', -1), ('b', 0), ('c', 0)): (0, 0), (('a', 0), ('b', 0), ('c', -1)): (0, -1), (('a', 0), ('b', -1), ('c', 0)): (0, 0)}

wrong: 
{(('a', 0), ('b', 0), ('c', -1)): (0, -1)}

wrong from path dev or path eq: 
{(('a', 0), ('b', 0), ('c', -1)): (0, -1)}

grade: 
91.66666666666666%
```

## Usage
```
python grade.py <reference_implementation> <student_implementation>
```

## Comparing with Random Input
One of the goal of exploring this approach is to see if it can cover edge cases where random input generation can't. To see if it does that on a particular problem, try generating random inputs and compare the result with PyAssessment.

```
python random_grade.py <reference_implementation> <student_implementation>
```

## How does it do that?
TODO: Will do after finishing the project (obviously).

## Limitation
- Implementation must be in the form of a python function with a return statement (not a procedure).
- The function must use integer(s) as input argument(s).

## Literature
TODO: Will put a link to the paper after finishing the project.
