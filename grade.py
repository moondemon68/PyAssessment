import os
import sys
import logging
import traceback
import json
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine
from symbolic.grader import GradingEngine

def pretty_print(d: dict) -> None:
	print("{")
	for key, value in d.items():
		print('    ' + str(key) + ' : ' + str(value) + ',')
	print("}")
	print()

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
	logging.basicConfig(filename=options.logfile, level=logging.DEBUG, filemode='w', format='%(asctime)s %(levelname)8s %(name)20s: %(message)s')

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
	logging.debug('Exploring reference application')
	explorationEngine = ExplorationEngine(app.createInvocation(), "z3")
	generatedInputs, returnVals, path = explorationEngine.explore(options.max_iters)
	with open('logs/reference.dot', 'w') as outfile:
		print(explorationEngine.path.toDot(), file=outfile)

	logging.debug('Exploring student application')
	explorationEngineStudent = ExplorationEngine(appStudent.createInvocation(), "z3")
	generatedInputsStudent, returnValsStudent, pathStudent = explorationEngineStudent.explore(options.max_iters)
	with open('logs/student.dot', 'w') as outfile:
		print(explorationEngineStudent.path.toDot(), file=outfile)

	generatedInputs += generatedInputsStudent
	returnVals += returnValsStudent
	logging.debug('Grading')
	gradingEngine = GradingEngine(app.createInvocation(), appStudent.createInvocation(), "z3")
	tested_case, wrong_case = gradingEngine.grade(generatedInputs, returnVals)
	
	tested_case_from_formula = tested_case.copy()
	wrong_case_from_formula = wrong_case.copy()
	for generated_input in generatedInputs:
		generated_input_tuple = tuple(sorted(generated_input))
		if generated_input_tuple in tested_case_from_formula:
			del tested_case_from_formula[generated_input_tuple]
		if generated_input_tuple in wrong_case_from_formula:
			del wrong_case_from_formula[generated_input_tuple]

	print('======')
	print('RESULT')
	print('======')
	print('tested: ')
	pretty_print(tested_case)
	print('tested from path dev or path eq: ')
	pretty_print(tested_case_from_formula)
	print('wrong: ')
	pretty_print(wrong_case)
	print('wrong from path dev or path eq: ')
	pretty_print(wrong_case_from_formula)
	print('grade: ')
	final_grade = (len(tested_case) - len(wrong_case)) / len(tested_case) * 100
	print(str(final_grade)+'%')
	tested_case = {str(k):(v[0], v[1]) for k, v in tested_case.items()}	# only get the reference output and the student output
	wrong_case = {str(k):(v[0], v[1]) for k, v in wrong_case.items()}
	resultJson = { 'reference': app.getFile(), 'grading': appStudent.getFile(), 'grade': final_grade, 'tested_case': tested_case, 'wrong_case': wrong_case }
	with open('res/'+app.getFile()+'-'+appStudent.getFile()+'.json', 'w+') as fp:
		json.dump(resultJson, fp, indent=4)
	# check the result
	result = app.executionComplete(returnVals)

except ImportError as e:
	# createInvocation can raise this
	logging.error(e)
	sys.exit(1)

if result == None or result == True:
	sys.exit(0)
else:
	sys.exit(1)
