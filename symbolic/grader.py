from collections import deque
import logging
import os

from .z3_wrap import Z3Wrapper
from .z3_translator import Z3Translator
from .path_constraint import PathConstraint
from .invocation import FunctionInvocation
from .symbolic_types import symbolic_type, SymbolicType
from .symbolic_types.symbolic_int import SymbolicInteger
from z3 import *

log = logging.getLogger("se.conc")

class GradingEngine:
	def __init__(self, funcinv, funcinvStudent, solver="z3"):
		self.tested_case = {}
		self.wrong_case = {}
		self.invocation = funcinv
		self.invocationStudent = funcinvStudent
		# the input to the function
		self.symbolic_inputs = {}  # string -> SymbolicType
		self.default_input = []
		# initialize
		for n in funcinv.getNames():
			self.symbolic_inputs[n] = funcinv.createArgumentValue(n)

		# print(self.symbolic_inputs)

		self.constraints_to_solve = deque([])
		self.num_processed_constraints = 0
		
		self.path_constraints = deque([])

		self.path = PathConstraint(lambda c : self.addConstraint(c), lambda p: self.addToPathConstraint(p))
		# link up SymbolicObject to PathToConstraint in order to intercept control-flow
		symbolic_type.SymbolicObject.SI = self.path

		if solver == "z3":
			self.solver = Z3Wrapper()
			self.translator = Z3Translator()

		# outputs
		self.generated_inputs = []
		self.execution_return_values = []

	def addConstraint(self, constraint):
		self.constraints_to_solve.append(constraint)
		# make sure to remember the input that led to this constraint
		constraint.inputs = self._getInputs()

	def addToPathConstraint(self, pred):
		self.path_constraints.append(pred)

	def grade(self, generated_inputs, execution_return_values):
		# print(generated_inputs)
		# print(execution_return_values)
		self.default_input = generated_inputs[0][:]
		for generated_input in generated_inputs:
			# print('from set: ')
			pc, pcStudent, ret, retStudent = self.execute_program(generated_input)
			# if ret.val != retStudent.val:
			# 	print('\33[41mgen input - implementation is incorrect:\033[0m')
			# 	print(generated_input)
			# else:
			# 	print('gen input')
			# 	print(generated_input)
			self.add_to_tested(generated_input, ret, retStudent)
			pathDeviationForm = self.path_deviation_builder(pc, pcStudent)
			sat, res = self.z3_solve(pathDeviationForm)
			if sat != 'sat':
				# print('no path deviation, skipping...')
				continue
			# print('from path dev: ')
			pc, pcStudent, ret, retStudent = self.execute_program(res)
			# if ret.val != retStudent.val:
			# 	print('\33[41mpath dev - implementation is incorrect:\033[0m')
			# 	print(res)
			# 	print(pathDeviationForm)
			# else:
			# 	print('path dev')
			# 	print(res)
			# 	print(pathDeviationForm)
			self.add_to_tested(res, ret, retStudent)
			if not isinstance(ret, SymbolicInteger) or not isinstance(retStudent, SymbolicInteger) or ret.name == "se" or retStudent.name == "se": # se is a wrapper string for operations (refer symbolic_int.py), so we can ignore it as it won't affect the result
				continue
			retSym = self.translator.symToZ3(ret.name)
			retStudentSym = self.translator.symToZ3(retStudent.name)
			pathEquivalenceForm = self.path_equivalence_builder(pc, pcStudent, retSym, retStudentSym)
			sat, res = self.z3_solve(pathEquivalenceForm)
			if sat != 'sat':
				# print('path is equivalent, skipping...')
				continue
			# print('from path equiv: ')
			pc, pcStudent, ret, retStudent = self.execute_program(res)
			# if ret.val != retStudent.val:
			# 	print('\33[41mpath equivalence - implementation is incorrect\033[0m')
			# 	print(res)
			# 	print(pathEquivalenceForm)
			# else:
			# 	print('path equivalence')
			# 	print(res)
			# 	print(pathEquivalenceForm)
			self.add_to_tested(res, ret, retStudent)
		return self.tested_case, self.wrong_case
	
	def add_to_tested(self, case, output_ref, output_stud):
		if isinstance(output_ref, SymbolicInteger):
			output_ref = output_ref.val
		if isinstance(output_stud, SymbolicInteger):
			output_stud = output_stud.val
		if tuple(sorted(case)) in self.tested_case:
			pass
		self.tested_case[tuple(sorted(case))] = (output_ref, output_stud)
		if output_ref != output_stud:
			self.wrong_case[tuple(sorted(case))] = (output_ref, output_stud)
	
	def execute_program(self, sym_inp):
		for inp in sym_inp:
			self._updateSymbolicParameter(inp[0], inp[1])
		ret = self.invocation.callFunction(self.symbolic_inputs)
		# print('ret: '+str(ret.val))
		# self._printPCDeque()
		pc = self.translator.pcToZ3(self.path_constraints)
		self.path_constraints = deque([])
		retStudent = self.invocationStudent.callFunction(self.symbolic_inputs)
		# print('retStudent: '+str(retStudent.val))
		pcStudent = self.translator.pcToZ3(self.path_constraints)
		self.path_constraints = deque([])
		# ret is SymbolicInteger
		# ret.name
		# ret.val
		return And(pc), And(pcStudent), ret, retStudent

	def path_deviation_builder(self, a, b):
		return Or(And(a, Not(b)), And(b, Not(a)))

	def path_equivalence_builder(self, a, b, oa, ob):
		return And(oa!=ob, And(a, b))

	def z3_solve(self, formula):
		s = Solver()
		s.add(formula)
		sat = s.check()
		# print(s.check())
		# print(s.model())
		if repr(sat) == 'sat':
			res = self.translator.modelToInp(s.model())
			res = self.fill_default(res)
			return 'sat', res
		else:
			return 'unsat', None
	
	def fill_default(self, res):
		new_res = res[:]
		# print(self.default_input)
		# print(new_res)
		for i in self.default_input:
			found = False
			for j in new_res:
				# print(i, j)
				if i[0] == j[0]:
					# print(i, j)
					found = True
					break
			if not found:
				new_res.append(i)
		return new_res

	# private

	def _updateSymbolicParameter(self, name, val):
		self.symbolic_inputs[name] = self.invocation.createArgumentValue(name,val)

	def _getInputs(self):
		return self.symbolic_inputs.copy()

	def _setInputs(self,d):
		self.symbolic_inputs = d

	def _printPCDeque(self):
		for i in self.path_constraints:
			print(i)
			print('---\n')

	def _pretty_print(self, d):
		print("{")
		for key, value in d.items():
			print('    ' + str(key) + ' : ' + str(value) + ',')
		print("}")