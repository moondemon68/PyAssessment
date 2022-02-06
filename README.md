# pyjudge
<img src="/pyjudge-logo.png" width="96">
Concolic execution based automatic grader

## What is this?
PyJudge is an automatic grading tools that takes a reference implementation and a student implementation then finds an input that causes a different output

This code used and is a modified version of [PyExZ3](https://github.com/thomasjball/PyExZ3) that is a Dynamic Symbolic Execution Engine for Python

This program is the deliverable of my [final project](https://drive.google.com/file/d/1UtX47PFaLpUXQhVJggxiudqUaKmhyybi/view?usp=sharing)

## Getting Started
1. Make sure you have Python 3.x installed
2. Install Z3 here https://github.com/Z3Prover/z3
3. For MacOS, open `setup.sh` and change the path according to your local machine then run:
```
. pyjudge/setup.sh
```
4. try grading something
```
python grade.py test/max_3/max_3.py test/max_3/max_3_1.py
```
it should return something like this and saved the result to `res` folder
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
python grade.py <reference_implementation>.py <student_implementation>.py
```

## Comparing with random input
One of the goal of exploring this approach is to see if it can cover edge cases where random input generation can't. To see if it does that on a particular problem, try running it with random input generation and compare the result.

```
python random_grade.py <reference_implementation>.py <student_implementation>.py
```

### How does it do that?
### Limitation
- implementation must be in the form of function with return statement
- function have integer as input

### Literature
[link to paper](https://drive.google.com/file/d/1UtX47PFaLpUXQhVJggxiudqUaKmhyybi/view?usp=sharing)
