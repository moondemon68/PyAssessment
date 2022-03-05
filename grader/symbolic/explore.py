# Copyright: see copyright.txt

from collections import deque
import logging
import os
import time
from typing import Any, Tuple

from symbolic.constraint import Constraint

from .z3_utils.z3_wrap import Z3Wrapper
from .path_to_constraint import PathToConstraint
from .invocation import FunctionInvocation
from .symbolic_types import symbolic_type, SymbolicType

log = logging.getLogger("se.conc")

class ExplorationEngine:
	def __init__(self, funcinv: FunctionInvocation, solver="z3") -> None:
		self.invocation = funcinv
		# the input to the function
		self.symbolic_inputs = {}  # string -> SymbolicType
		# initialize
		for n in funcinv.getNames():
			self.symbolic_inputs[n] = funcinv.createArgumentValue(n)

		self.constraints_to_solve = deque([])
		self.num_processed_constraints = 0

		self.path = PathToConstraint(lambda c : self.addConstraint(c))
		# link up SymbolicObject to PathToConstraint in order to intercept control-flow
		symbolic_type.SymbolicObject.SI = self.path

		if solver == "z3":
			self.solver = Z3Wrapper()

		# outputs
		self.generated_inputs = []
		self.execution_return_values = []

	def addConstraint(self, constraint: Constraint) -> None:
		self.constraints_to_solve.append(constraint)
		# make sure to remember the input that led to this constraint
		constraint.inputs = self._getInputs()

	def explore(self, max_iterations=0, max_time=0, start_time=0) -> Tuple[list, list, PathToConstraint]:
		self._oneExecution()
		iterations = 1
		if max_iterations != 0 and iterations >= max_iterations:
			log.debug("Maximum number of iterations reached, terminating")
			return self.generated_inputs, self.execution_return_values, self.path
		if max_time != 0 and time.time() - start_time >= max_time:
			log.debug("Time limit exceeded, terminating")
			return self.generated_inputs, self.execution_return_values, self.path

		while not self._isExplorationComplete():
			selected = self.constraints_to_solve.popleft()
			if selected.processed:
				continue
			self._setInputs(selected.inputs)

			log.info("Selected constraint %s" % selected)
			asserts, query = selected.getAssertsAndQuery()
			model = self.solver.findCounterexample(asserts, query)

			if model == None:
				continue
			else:
				for name in model.keys():
					self._updateSymbolicParameter(name,model[name])

			self._oneExecution(selected)

			iterations += 1			
			self.num_processed_constraints += 1

			if max_iterations != 0 and iterations >= max_iterations:
				log.info("Maximum number of iterations reached, terminating")
				break
			if max_time != 0 and time.time() - start_time >= max_time:
				log.info("Time limit exceeded, terminating")
				break

		return self.generated_inputs, self.execution_return_values, self.path

	# private

	def _updateSymbolicParameter(self, name: str, val: Any) -> None:
		self.symbolic_inputs[name] = self.invocation.createArgumentValue(name,val)

	def _getInputs(self) -> dict:
		return self.symbolic_inputs.copy()

	def _setInputs(self, d: Any) -> None:
		self.symbolic_inputs = d

	def _isExplorationComplete(self) -> bool:
		num_constr = len(self.constraints_to_solve)
		if num_constr == 0:
			log.info("Exploration complete")
			return True
		else:
			log.info("%d constraints yet to solve (total: %d, already solved: %d)" % (num_constr, self.num_processed_constraints + num_constr, self.num_processed_constraints))
			return False

	def _getConcrValue(self, v: SymbolicType) -> Any:
		if isinstance(v, SymbolicType):
			return v.getConcrValue()
		else:
			return v

	def _recordInputs(self) -> None:
		args = self.symbolic_inputs
		inputs = [ (k,self._getConcrValue(args[k])) for k in args ]
		self.generated_inputs.append(inputs)
		# print('inputs:',inputs)
		
	def _oneExecution(self, expected_path: Constraint = None) -> None:
		self._recordInputs()
		self.path.reset(expected_path)
		ret = self.invocation.callFunction(self.symbolic_inputs)
		self.execution_return_values.append(ret)