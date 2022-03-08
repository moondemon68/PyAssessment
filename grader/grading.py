import sys
import logging
import time
import json

from grader.symbolic.loader import *
from grader.symbolic.random_grader import RandomGradingEngine
from grader.symbolic.loader import *
from grader.symbolic.explore import ExplorationEngine
from grader.symbolic.grader import GradingEngine
from grader.symbolic.z3_utils.z3_similarity import similarity
from grader.tracing import traceApp

def pretty_print(d: dict) -> None:
	print("{")
	for key, value in d.items():
		print('    ' + str(key) + ' : ' + str(value) + ',')
	print("}")
	print()

def random_grade(filename, filenameStudent, printLogs=False):
	# Get the object describing the application
	app = loaderFactory(filename)
	appStudent = loaderFactory(filenameStudent)

	print("Grading: " + appStudent.getFile() + "." + appStudent.getEntry())

	try:
		gradingEngine = RandomGradingEngine(app.createInvocation(), appStudent.createInvocation(), "z3")
		tested_case, wrong_case = gradingEngine.grade()
		final_grade = (len(tested_case) - len(wrong_case)) / len(tested_case) * 100
		tested_case = {str(k):v for k, v in tested_case.items()}
		wrong_case = {str(k):v for k, v in wrong_case.items()}
		resultJson = { 'reference': app.getFile(), 'grading': appStudent.getFile(), 'grade': final_grade, 'tested_case': tested_case, 'wrong_case': wrong_case}
		if printLogs:
			print('tested:')
			pretty_print(tested_case)
			print('wrong:')
			pretty_print(wrong_case)
			print('grade:')
			print(str(final_grade) + '% (' + str(len(tested_case) - len(wrong_case)) + '/' + str(len(tested_case)) + ')')
			print()
			with open('res/RANDOM-'+app.getFile()+'-'+appStudent.getFile()+'.json', 'w') as fp:
				json.dump(resultJson, fp, indent=4)
		return resultJson

	except ImportError as e:
		# createInvocation can raise this
		logging.error(e)
		return None

def semi_whitebox_grade(filename, filenameStudent, maxIters, maxTime):
	# Get the object describing the application
	app = loaderFactory(filename)
	appStudent = loaderFactory(filenameStudent)

	print("Grading: " + appStudent.getFile() + "." + appStudent.getEntry())

	try:
		start_time = time.time()

		explorationEngine = ExplorationEngine(app.createInvocation(), "z3")
		generatedInputs, returnVals, path = explorationEngine.explore(maxIters, maxTime, start_time)
		explorationEngineStudent = ExplorationEngine(appStudent.createInvocation(), "z3")
		generatedInputsStudent, returnValsStudent, pathStudent = explorationEngineStudent.explore(maxIters, maxTime, start_time)
		generatedInputs += generatedInputsStudent
		returnVals += returnValsStudent

		gradingEngine = GradingEngine(app.createInvocation(), appStudent.createInvocation(), "z3")
		tested_case, wrong_case = gradingEngine.grade(generatedInputs, returnVals)
		
		final_grade = (len(tested_case) - len(wrong_case)) / len(tested_case) * 100
		tested_case = {str(k):(v[0], v[1]) for k, v in tested_case.items()}
		wrong_case = {str(k):(v[0], v[1]) for k, v in wrong_case.items()}
		resultJson = { 'reference': app.getFile(), 'grading': appStudent.getFile(), 'grade': final_grade, 'wrong_case': wrong_case }
		return resultJson

	except ImportError as e:
		# createInvocation can raise this
		logging.error(e)
		return None

def whitebox_grade(filename, filenameStudent, maxIters, maxTime, printLogs=False, printPaths=False):
	# Get the object describing the application
	app = loaderFactory(filename)
	appStudent = loaderFactory(filenameStudent)

	print("Grading: " + appStudent.getFile() + "." + appStudent.getEntry())

	try:
		start_time = time.time()

		explorationEngine = ExplorationEngine(app.createInvocation(), "z3")
		generatedInputs, returnVals, path = explorationEngine.explore(maxIters, maxTime, start_time)
		explorationEngineStudent = ExplorationEngine(appStudent.createInvocation(), "z3")
		generatedInputsStudent, returnValsStudent, pathStudent = explorationEngineStudent.explore(maxIters, maxTime, start_time)
		generatedInputs += generatedInputsStudent
		returnVals += returnValsStudent

		gradingEngine = GradingEngine(app.createInvocation(), appStudent.createInvocation(), "z3")
		tested_case, wrong_case = gradingEngine.grade(generatedInputs, returnVals)

		# Path constraint grading
		pathConstraints = {}
		studentScore = 0
		totalScore = 0
		for case in tested_case:
			referenceOutput = tested_case[case][0]
			studentOutput = tested_case[case][1]
			referencePathConstraint = tested_case[case][2]
			studentPathConstraint = tested_case[case][3]

			# calculate similarity of path constraints
			score = 0
			if referenceOutput == studentOutput:
				# if the output is the same, then the path constraint is correct
				score = 1
			else:
				# else, we need to calculate the similarity of the path constraint that lead to the wrong output with the path constraint that lead to the right output
				similarityScore = similarity(referencePathConstraint, studentPathConstraint)
				if similarityScore == 1:
					# if the path constraints are exactly the same and the output is different, then the mistake is in the output (not the conditions)
					score = 0.2 # need to ask about this, how the scoring works in teaching env
				else:
					score = similarityScore
			
			# two path constraints may produce different results based on the input, so previously correct path constraints may be wrong now
			if (referencePathConstraint, studentPathConstraint) not in pathConstraints:
				pathConstraints[(referencePathConstraint, studentPathConstraint)] = score
			else:
				pathConstraints[(referencePathConstraint, studentPathConstraint)] = min(score, pathConstraints[(referencePathConstraint, studentPathConstraint)])
		
		# calculate score
		for key in pathConstraints:
			studentScore += pathConstraints[key]
			totalScore += 1
		pathConstraintGrade = studentScore / totalScore * 100

		# Get feedback
		visitedLines = traceApp(appStudent, wrong_case)
		visitedLines = [str(x) for x in visitedLines]
		feedback = 'Please check line(s) ' + ', '.join(visitedLines) + ' in your program.'
		
		if printLogs:
			with open('logs/reference.dot', 'w') as outfile:
				print(explorationEngine.path.toDot(), file=outfile)
			with open('logs/student.dot', 'w') as outfile:
				print(explorationEngineStudent.path.toDot(), file=outfile)
			# Replace all PathDeviation or PathEquivalence with Exploration if the case is actually generated by exploration
			for generated_input in generatedInputs:
				generated_input_tuple = tuple(sorted(generated_input))
				for key in tested_case:
					if key == generated_input_tuple:
						tested_case[key][4] = 'Exploration'
				for key in wrong_case:
					if key == generated_input_tuple:
						wrong_case[key][4] = 'Exploration'
			# Filter out the cases that are generated by exploration to show path deviation or path equivalence cases
			tested_case_from_formula = tested_case.copy()
			wrong_case_from_formula = wrong_case.copy()
			for generated_input in generatedInputs:
				generated_input_tuple = tuple(sorted(generated_input))
				if generated_input_tuple in tested_case_from_formula:
					del tested_case_from_formula[generated_input_tuple]
				if generated_input_tuple in wrong_case_from_formula:
					del wrong_case_from_formula[generated_input_tuple]
			# Don't print path deviation and equivalence if print_path is false
			if not printPaths:
				for key in tested_case:
					tested_case[key][2] = '-'
					tested_case[key][3] = '-'
				for key in wrong_case:
					wrong_case[key][2] = '-'
					wrong_case[key][3] = '-'
			# Print out the results
			print('======')
			print('RESULT')
			print('======')
			print('tested:')
			pretty_print(tested_case)
			print('tested from path dev or path eq:')
			pretty_print(tested_case_from_formula)
			print('wrong:')
			pretty_print(wrong_case)
			print('wrong from path dev or path eq:')
			pretty_print(wrong_case_from_formula)
			print('grade:')
			final_grade = (len(tested_case) - len(wrong_case)) / len(tested_case) * 100
			print(str(final_grade) + '% (' + str(len(tested_case) - len(wrong_case)) + '/' + str(len(tested_case)) + ')')
			print()
			if printPaths:
				print('path constraints:')
				pretty_print(pathConstraints)
			print('path constraint grade:')
			pathConstraintGrade = studentScore / totalScore * 100
			print(str(pathConstraintGrade) + '% (' + str(studentScore) + '/' + str(totalScore) + ')')
			print()
			print('feedback:')
			print(feedback)
			print()
			testedCaseFile = {str(k):(v[0], v[1]) for k, v in tested_case.items()}
			wrongCaseFile = {str(k):(v[0], v[1]) for k, v in wrong_case.items()}
			resultJsonFile = { 'reference': app.getFile(), 'grading': appStudent.getFile(), 'grade': final_grade, 'path_constraint_grade': pathConstraintGrade, 'tested_case': testedCaseFile, 'wrong_case': wrongCaseFile, 'feedback': feedback }
			with open('res/'+app.getFile()+'-'+appStudent.getFile()+'.json', 'w+') as fp:
				json.dump(resultJsonFile, fp, indent=4)

		tested_case = {str(k):(v[0], v[1]) for k, v in tested_case.items()}
		wrong_case = {str(k):(v[0], v[1]) for k, v in wrong_case.items()}
		resultJson = { 'reference': app.getFile(), 'grading': appStudent.getFile(), 'grade': pathConstraintGrade, 'wrong_case': wrong_case, 'feedback': feedback }
		return resultJson

	except ImportError as e:
		# createInvocation can raise this
		logging.error(e)
		return None
