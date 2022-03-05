from collections import deque
import logging
from typing import Any, Tuple

from grader.symbolic.constraint import Constraint
from grader.symbolic.predicate import Predicate

from .z3_utils.z3_wrap import Z3Wrapper
from .z3_utils.z3_translator import Z3Translator
from .path_constraint import PathConstraint
from .invocation import FunctionInvocation
from .symbolic_types import symbolic_type, SymbolicType
from .symbolic_types.symbolic_int import SymbolicInteger
from z3 import Probe, BoolRef, ArithRef, Or, And, Not, Solver

log = logging.getLogger("se.conc")

class GradingEngine:
	def __init__(self, funcinv: FunctionInvocation, funcinvStudent: FunctionInvocation, solver="z3") -> None:
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

	def addConstraint(self, constraint: Constraint) -> None:
		self.constraints_to_solve.append(constraint)
		# make sure to remember the input that led to this constraint
		constraint.inputs = self._getInputs()

	def addToPathConstraint(self, pred: Predicate) -> None:
		self.path_constraints.append(pred)

	def grade(self, generated_inputs: list, execution_return_values: list) -> Tuple[dict, dict]:
		self.default_input = generated_inputs[0][:]
		for generated_input in generated_inputs:
			# path deviation check
			pc, pcStudent, ret, retStudent = self.execute_program(generated_input)
			self.add_to_tested(generated_input, ret, retStudent, pc, pcStudent, 'Exploration')
			pathDeviationFormula = self.path_deviation_builder(pc, pcStudent)
			sat, res = self.z3_solve(pathDeviationFormula)
			if sat == 'unsat':
				# print('no path deviation, skipping...')
				continue

			# if there is a path deviation, check equivalence using the result of the satisfiability formula to trigger the deviation
			# res contains the case that triggered the path deviation, but can still be correct or wrong
			pc, pcStudent, ret, retStudent = self.execute_program(res)
			self.add_to_tested(res, ret, retStudent, pc, pcStudent, 'PathDeviation')
			if not isinstance(ret, SymbolicInteger) or not isinstance(retStudent, SymbolicInteger):
				continue
			retSym = self.translator.symToZ3(ret.getSymbolicExpr())
			retStudentSym = self.translator.symToZ3(retStudent.getSymbolicExpr())
			pathEquivalenceFormula = self.path_equivalence_builder(pc, pcStudent, retSym, retStudentSym)
			sat, res = self.z3_solve(pathEquivalenceFormula)
			if sat == 'unsat':
				# print('path is equivalent, skipping...')
				continue
			
			# there is a deviation and the deviated path is not equal, so student's program is wrong
			# the test case that made the student's program wrong can be found in res
			pc, pcStudent, ret, retStudent = self.execute_program(res)
			self.add_to_tested(res, ret, retStudent, pc, pcStudent, 'PathEquivalence')
		return self.tested_case, self.wrong_case
	
	# possible sources
	# Exploration, PathDeviation, PathEquivalence
	def add_to_tested(self, case: list, outputReference: Any, outputStudent: Any, pcReference: BoolRef, pcStudent: BoolRef, source: str) -> None:
		if isinstance(outputReference, SymbolicInteger):
			outputReference = outputReference.val
		if isinstance(outputStudent, SymbolicInteger):
			outputStudent = outputStudent.val
		if tuple(sorted(case)) in self.tested_case:
			pass
		self.tested_case[tuple(sorted(case))] = [outputReference, outputStudent, pcReference, pcStudent, source]
		if outputReference != outputStudent:
			self.wrong_case[tuple(sorted(case))] = [outputReference, outputStudent, pcReference, pcStudent, source]
	
	def execute_program(self, sym_inp: list) -> Tuple[BoolRef, BoolRef, Any, Any]:
		for inp in sym_inp:
			self._updateSymbolicParameter(inp[0], inp[1])
		ret = self.invocation.callFunction(self.symbolic_inputs)
		pc = self.translator.pcToZ3(self.path_constraints)
		self.path_constraints = deque([])
		retStudent = self.invocationStudent.callFunction(self.symbolic_inputs)
		pcStudent = self.translator.pcToZ3(self.path_constraints)
		self.path_constraints = deque([])
		return And(pc), And(pcStudent), ret, retStudent

	def path_deviation_builder(self, a: BoolRef, b: BoolRef) -> (Probe | BoolRef):
		return Or(And(a, Not(b)), And(b, Not(a)))

	def path_equivalence_builder(self, a: BoolRef, b: BoolRef, oa: ArithRef, ob: ArithRef) -> (Probe | BoolRef):
		return And(oa!=ob, And(a, b))

	def z3_solve(self, formula: (Probe | BoolRef)) -> Tuple[str, list]:
		s = Solver()
		s.add(formula)
		sat = s.check()
		if repr(sat) == 'sat':
			res = self.translator.modelToInp(s.model())
			res = self.fill_default(res)
			return 'sat', res
		else:
			return 'unsat', None
	
	def fill_default(self, res: list) -> list:
		new_res = res[:]
		for i in self.default_input:
			found = False
			for j in new_res:
				if i[0] == j[0]:
					found = True
					break
			if not found:
				new_res.append(i)
		return new_res

	# private

	def _updateSymbolicParameter(self, name: str, val: Any) -> None:
		self.symbolic_inputs[name] = self.invocation.createArgumentValue(name,val)

	def _getInputs(self) -> None:
		return self.symbolic_inputs.copy()

	def _setInputs(self, d: dict) -> None:
		self.symbolic_inputs = d

	def _printPCDeque(self) -> None:
		for i in self.path_constraints:
			print(i)
			print('---\n')

	def _pretty_print(self, d: dict) -> None:
		print("{")
		for key, value in d.items():
			print('    ' + str(key) + ' : ' + str(value) + ',')
		print("}")