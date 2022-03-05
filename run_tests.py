import os
import re
import sys
import subprocess
from optparse import OptionParser
from sys import platform as _platform
from problems import problems

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

usage = "usage: %prog [options] <test directory>"
parser = OptionParser()
(options, args) = parser.parse_args()

if len(args) == 0 or not os.path.exists(args[0]):
    parser.error("Please supply directory of tests")
    sys.exit(1)
    
test_dir = os.path.abspath(args[0])

if not os.path.isdir(test_dir):
    print("Please provide a directory of test scripts.")
    sys.exit(1)

tested_problems = [
    'air',
    # 'arithmetic_seq',
    # 'digits',
    'is_allowed_to_buy',
    # 'is_ordered',
    'max_3',
    # 'mid_3',
    # 'min_3',
    'no_of_triangle',
    # 'pow3abs',
    'segiempat',
    'student_grade',
    # 'sum_20',
]

failed = []
print('Running tests:')
for problem in problems:
    if problem not in tested_problems:
        continue
    print('Problem:', problem)
    files = problems[problem]
    reference = files[0]
    students = files[1:]
    for student in students:
        fullReference = os.path.join(test_dir, problem, reference)
        fullStudent = os.path.join(test_dir, problem, student)
        with open(os.devnull, 'w') as devnull:
            ret = subprocess.call([sys.executable, 'grade.py', fullReference, fullStudent, '-m 25', '-t 0.1'], stdout=devnull, stderr=devnull)
            retRandom = subprocess.call([sys.executable, 'random_grade.py', fullReference, fullStudent], stdout=devnull, stderr=devnull)
            if ret == 0 and retRandom == 0:
                print(bcolors.OKGREEN + "✓", student + bcolors.ENDC)
            else:
                failed.append((problem, student))
                print(bcolors.FAIL + "✗", student + bcolors.ENDC)

print()
if failed != []:
    print('Failed tests:')
    for problem, student in failed:
        print(bcolors.FAIL + problem + ' - ' + student + bcolors.ENDC)
else:
    print(bcolors.OKGREEN + 'All tests passed!' + bcolors.ENDC)
