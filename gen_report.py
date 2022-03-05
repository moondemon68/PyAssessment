import json
from problems import problems
import os
import pandas as pd

report_problems = [
	'max_3',
	'segiempat',
	'student_grade',
	'is_allowed_to_buy',
	'no_of_triangle',
	'air',
]

with open('res/report.csv', 'w+') as f:
	data = []
	res_dir = os.path.abspath('res')
	for problem in report_problems:
		files = problems[problem]
		reference = files[0]
		students = files[1:]
		for student in students:
			try:
				res_grade = os.path.join(res_dir, problem + '-' + student[:-3] + '.json')
				res_random_grade = os.path.join(res_dir, 'RANDOM-' + problem + '-' + student[:-3] + '.json')
				with open(res_grade, 'r') as f_grade:
					grade = json.load(f_grade)
				with open(res_random_grade, 'r') as f_random_grade:
					random_grade = json.load(f_random_grade)
				data.append([problem, student[:-3], grade['grade'], grade['path_constraint_grade'], random_grade['grade']])
			except Exception:
				pass
	df = pd.DataFrame(data, columns=['problem', 'student_file', 'white_black_grade', 'white_grade', 'random_grade'])
	df.to_csv(f, sep=',', index=False, line_terminator='\n')

	print('Report generated in res/report.csv')

