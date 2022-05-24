import os
import sys
import subprocess
from optparse import OptionParser
from problems import problems, tested_problems

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

failed = []
print('Running tests:')
for problem in problems:
    if problem not in tested_problems:
        continue
    print('Problem:', problem)
    files = problems[problem]['files']
    min_args = str(problems[problem]['min_args'])
    max_args = str(problems[problem]['max_args'])
    reference = files[0]
    students = files[1:]
    for student in students:
        fullReference = os.path.join(test_dir, problem, reference)
        fullStudent = os.path.join(test_dir, problem, student)
        with open(os.devnull, 'w') as devnull:
            ret = subprocess.call([sys.executable, 'grade.py', fullReference, fullStudent, '-m', '50', '-t', '0.5', '-g', 'whitebox'], stdout=devnull, stderr=devnull)
            retRandom = subprocess.call([sys.executable, 'grade.py', fullReference, fullStudent, '-g', 'random', '-a', min_args, '-A', max_args], stdout=devnull, stderr=devnull)
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
