import os
import sys
import logging
import traceback
import json
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine
from symbolic.random_grader import RandomGradingEngine

def pretty_print(d):
	print("{")
	for key, value in d.items():
		print('    ' + str(key) + ' : ' + str(value) + ',')
	print("}")

def tracefunc(frame, event, arg, indent=[0]):
	if event == "call":
		indent[0] += 2
		print("-" * indent[0] + "> call function", frame.f_code.co_name)
	elif event == "return":
		print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
		indent[0] -= 2
	return tracefunc

# uncomment to trace function call
# sys.setprofile(tracefunc)

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

usage = "usage: %prog [options] <path to reference *.py file> <path to submission *.py file>"
parser = OptionParser(usage=usage)

parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file", default="")
parser.add_option("-m", "--max-iters", dest="max_iters", type="int", help="Run specified number of iterations", default=0)

(options, args) = parser.parse_args()

if not (options.logfile == ""):
	logging.basicConfig(filename=options.logfile,level=logging.DEBUG)

if len(args) == 0 or not os.path.exists(args[0]):
	parser.error("Missing app to execute")
	sys.exit(1)

filename = os.path.abspath(args[0])
filenameStudent = os.path.abspath(args[1])
	
# Get the object describing the application
app = loaderFactory(filename)
appStudent = loaderFactory(filenameStudent)
if app == None or appStudent == None:
	sys.exit(1)

print ("Reference: " + app.getFile() + "." + app.getEntry())
print ("Grading: " + appStudent.getFile() + "." + appStudent.getEntry())


result = None
try:
	gradingEngine = RandomGradingEngine(app.createInvocation(), appStudent.createInvocation(), "z3")
	tested_case, wrong_case = gradingEngine.grade()
	final_grade = (len(tested_case) - len(wrong_case)) / len(tested_case) * 100
	tested_case = {str(k):v for k, v in tested_case.items()}
	wrong_case = {str(k):v for k, v in wrong_case.items()}
	resultJson = { 'reference': app.getFile(), 'grading': appStudent.getFile(), 'grade': final_grade, 'tested_case': tested_case, 'wrong_case': wrong_case}
	print(resultJson)
	with open('res/RANDOM-'+app.getFile()+'-'+appStudent.getFile()+'.json', 'w') as fp:
		json.dump(resultJson, fp, indent=4)

except ImportError as e:
	# createInvocation can raise this
	logging.error(e)
	sys.exit(1)

if result == None or result == True:
	sys.exit(0)
else:
	sys.exit(1)
