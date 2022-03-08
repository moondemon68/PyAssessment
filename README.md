# PyAssessment
Concolic execution based automatic grading tool for Python functions.

## About This Project
PyAssessment is an automatic grading tool which gives a score to a student implementation based on its semantic similarity with a reference implementation. This tool can be used in the form a web service.

This code is a modified version of:
- [PyJudge](https://github.com/Barbariansyah/pyjudge): An automatic grading tool that takes a reference implementation and a student implementation, and finds input(s) that generate a different output.
- [PyExZ3](https://github.com/thomasjball/PyExZ3): A Dynamic Symbolic Execution Engine for Python.

This repository will be the deliverable of my final project.

## Getting Started (Docker)
1. Make sure you have docker installed.
2. Start the server using this command:
```
docker-compose up --build
```
3. Visit http://localhost:5000/. Ignore the IP given in the server log.

## Getting Started (Python)
1. Make sure you have Python of version at least 3.10 installed (due to type hinting).
2. Install the requirements.
```
pip install -r requirements.txt
```
3. For MacOS, open `setup.sh` and change the path according to your local machine then run:
```
. grader/setup.sh
```
4. Make sure you are in the repository root. Set the python path to current directory:
```
set PYTHONPATH=.
```
5. Start the server using this command:
```
python web_service/src/main.py
```
6. Visit http://localhost:5000/. Ignore the IP given in the server log.

## Endpoints
Full documentation can be accessed [here (TBD)](www.google.com).

## Usage
```
python grade.py <reference_implementation> <student_implementation> [options]
```

## Example Usage
```
python grade.py test/max_3/max_3.py test/max_3/max_3_1.py
```
It should return something like this and save the result to `res` folder.

DOT files containing the exploration paths can be seen in `logs` folder as `student.dot` and `reference.dot`. DOT files can be viewed using `graphviz` (online services such as [this](https://dreampuf.github.io/GraphvizOnline) can also be used).
```
Reference: max_3.max_3
Grading: max_3_1.max_3_1
======
RESULT
======
tested:
{
    (('a', 0), ('b', 0), ('c', 0)) : [0, 0, And(a >= b, a >= c), And(a <= b, b <= a), 'Exploration'],
    (('a', 0), ('b', -1), ('c', 0)) : [0, 0, And(a >= b, a >= c), And(a > b, a <= c, b <= a), 'PathDeviation'],
    (('a', 0), ('b', 2), ('c', 0)) : [2, 2, And(a < b, b >= a, b >= c), And(a <= b, b > a, b > c), 'Exploration'],
    (('a', -1), ('b', 0), ('c', 0)) : [0, 0, And(a < b, b >= a, b >= c), And(a <= b, b > a, b <= c), 'PathDeviation'],
    (('a', 0), ('b', 0), ('c', 1)) : [1, 1, And(a >= b, a < c, b >= a, b < c), And(a <= b, b <= a), 'Exploration'],
    (('a', 0), ('b', 0), ('c', -1)) : [0, -1, And(a >= b, a >= c), And(a <= b, b <= a), 'PathEquivalence'],
    (('a', 1), ('b', 2), ('c', 3)) : [3, 3, And(a < b, b >= a, b < c), And(a <= b, b > a, b <= c), 'Exploration'],
    (('a', 1), ('b', 0), ('c', 2)) : [2, 2, And(a >= b, a < c, b < a), And(a > b, a <= c, b <= a), 'Exploration'],
    (('a', 2), ('b', 0), ('c', 0)) : [2, 2, And(a >= b, a >= c), And(a > b, a > c), 'Exploration'],
    (('a', 0), ('b', 1), ('c', 0)) : [1, 1, And(a < b, b >= a, b >= c), And(a <= b, b > a, b > c), 'Exploration'],
    (('a', 10), ('b', 0), ('c', 12)) : [12, 12, And(a >= b, a < c, b < a), And(a > b, a <= c, b <= a), 'Exploration'],
    (('a', 4), ('b', 5), ('c', 8)) : [8, 8, And(a < b, b >= a, b < c), And(a <= b, b > a, b <= c), 'Exploration'],
}

tested from path dev or path eq:
{
    (('a', 0), ('b', -1), ('c', 0)) : [0, 0, And(a >= b, a >= c), And(a > b, a <= c, b <= a), 'PathDeviation'],
    (('a', -1), ('b', 0), ('c', 0)) : [0, 0, And(a < b, b >= a, b >= c), And(a <= b, b > a, b <= c), 'PathDeviation'],
    (('a', 0), ('b', 0), ('c', -1)) : [0, -1, And(a >= b, a >= c), And(a <= b, b <= a), 'PathEquivalence'],
}

wrong:
{
    (('a', 0), ('b', 0), ('c', -1)) : [0, -1, And(a >= b, a >= c), And(a <= b, b <= a), 'PathEquivalence'],
}

wrong from path dev or path eq:
{
    (('a', 0), ('b', 0), ('c', -1)) : [0, -1, And(a >= b, a >= c), And(a <= b, b <= a), 'PathEquivalence'],
}

grade:
91.66666666666666% (11/12)

path constraints:
{
    (And(a >= b, a >= c), And(a <= b, b <= a)) : 0.5,
    (And(a >= b, a >= c), And(a > b, a <= c, b <= a)) : 1,
    (And(a < b, b >= a, b >= c), And(a <= b, b > a, b > c)) : 1,
    (And(a < b, b >= a, b >= c), And(a <= b, b > a, b <= c)) : 1,
    (And(a >= b, a < c, b >= a, b < c), And(a <= b, b <= a)) : 1,
    (And(a < b, b >= a, b < c), And(a <= b, b > a, b <= c)) : 1,
    (And(a >= b, a < c, b < a), And(a > b, a <= c, b <= a)) : 1,
    (And(a >= b, a >= c), And(a > b, a > c)) : 1,
}

path constraint grade:
93.75% (7.5/8)

feedback:
Please check line(s) 2, 4, 7 in your program.
```

## Options
```
  -h, --help            show this help message and exit
  -g GRADER, --grader=GRADER
                        Grader to be used. ['random', 'whitebox' (default)]
  -l LOGFILE, --log=LOGFILE
                        Save log output to a file.
  -m MAX_ITERS, --max-iters=MAX_ITERS
                        Run specified number of iterations (0 for unlimited).
                        Should be used for looping or recursive programs.
  -t MAX_TIME, --max-time=MAX_TIME
                        Maximum time for exploration (0 for unlimited). Expect
                        maximum execution time to be around three times the
                        amount.
  -q, --quiet           Quiet mode. Does not print path constraints. Should be
                        activated for looping or recursive programs as
                        printing z3 expressions can be time consuming.
```

## Comparing with Random Input
One of the goal of exploring this approach is to see if it can cover edge cases where random input generation can't. To see if it does that on a particular problem, try generating random inputs and compare the result with PyAssessment.

```
python grade.py <reference_implementation> <student_implementation> -g random
```

## Test All in Directory
1. Define the problem, reference solution, and student solutions in `problems.py`.
2. Run `python run_tests.py [test_directory]`
```
python run_tests.py test
```
3. A message `All tests passed!` will be printed if all tests passed. The json result of all tests will be saved in the `res` folder.

## Generate Report
1. Make sure that all json results are present in the `res` folder. It should work fine if you have run the `test all` command.
2. Run `python generate_report.py`
3. The report will be generated in the `res` folder with filename `report.csv`.

## Cleanup
Cleans up the `res` and `logs` folder.
```
python clean.py
```

## Timelimits
For both the web service and `grade.py`, there is a hard time limit of 10 seconds. This is used to handle the case where the student implementation is not responding due to infinite loops or recursion.

## How does it do that?
TODO: Will do after finishing the project (obviously).

## Limitation
- Implementation must be in the form of a python function with a return statement (not a procedure).
- The function must use integer(s) as input argument(s).

## Literature
TODO: Will put a link to the paper after finishing the project.

## TODO
- Check the case where conditions are correct but the return statement is wrong (what score should be given?)
- Add timelimit as a request parameter that can override default 10 seconds
- Refactor code such that both grade.py and the web service use the same grading function in grader/grading.py