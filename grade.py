import os
import sys
import logging
import time
import json
from optparse import OptionParser
from func_timeout import func_timeout, FunctionTimedOut
from grader.grading import random_grade, whitebox_grade

from grader.symbolic.loader import *
from grader.symbolic.explore import ExplorationEngine
from grader.symbolic.grader import GradingEngine
from grader.symbolic.random_grader import RandomGradingEngine
from grader.symbolic.z3_utils.z3_similarity import similarity
from grader.tracing import traceApp

def pretty_print(d: dict) -> None:
	print("{")
	for key, value in d.items():
		print('    ' + str(key) + ' : ' + str(value) + ',')
	print("}")
	print()

def main():
	sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

	usage = "usage: %prog [options] <path to reference *.py file> <path to submission *.py file>"
	parser = OptionParser(usage=usage)

	parser.add_option("-g", "--grader", dest="grader", type="choice", help="Grader to be used.", default="whitebox", choices=['random', 'whitebox'])
	parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file.", default="")
	parser.add_option("-m", "--max-iters", dest="max_iters", type="int", help="Run specified number of iterations (0 for unlimited). Should be used for looping or recursive programs.", default=500)
	parser.add_option("-t", "--max-time", dest="max_time", type="float", help="Maximum time for exploration (0 for unlimited, default 5). Expect maximum execution time to be around three times the amount.", default=5)
	parser.add_option("-q", "--quiet", dest="print_path", action="store_false", help="Quiet mode. Does not print path constraints. Should be activated for looping or recursive programs as printing z3 expressions can be time consuming.", default=True)
	parser.add_option("-a", "--min-args", dest="min_args", action="store", type="int", help="Minimum value for arguments (random grading only)", default=-100)
	parser.add_option("-A", "--max-args", dest="max_args", action="store", type="int", help="Minimum value for arguments (random grading only)", default=100)

	(options, args) = parser.parse_args()

	if not (options.logfile == ""):
		logging.basicConfig(filename=options.logfile, level=logging.DEBUG, filemode='w', format='%(asctime)s %(levelname)8s %(name)20s: %(message)s')

	if len(args) == 0 or not os.path.exists(args[0]):
		parser.error("Missing app to execute")
		sys.exit(1)

	filename = os.path.abspath(args[0])
	filenameStudent = os.path.abspath(args[1])

	result = None
	if options.grader == 'whitebox':
		try:
			whitebox_grade(filename, filenameStudent, options.max_iters, options.max_time, printLogs=True, printPaths=options.print_path)
			
		except ImportError as e:
			# createInvocation can raise this
			logging.error(e)
			return None

		if result == None or result == True:
			sys.exit(0)
		else:
			sys.exit(1)

	else:
		try:
			random_grade(filename, filenameStudent, options.min_args, options.max_args, printLogs=True)

		except ImportError as e:
			# createInvocation can raise this
			logging.error(e)
			sys.exit(1)

		if result == None or result == True:
			sys.exit(0)
		else:
			sys.exit(1)

if __name__ == '__main__':
	try:
		result = func_timeout(20, main)
	except RecursionError as e:
		print('Recursion limit exceeded, probably due to an infinite loop/recursion')
	except Exception as e:
		print('An error occured:', e)
	except FunctionTimedOut as e:
		print('Time limit exceeded')