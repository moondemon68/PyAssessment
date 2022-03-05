# Copyright: see copyright.txt

from collections import deque
import sys
import ast
import logging
from typing import Any, Tuple
import grader.utils

from z3 import *
from ..z3_expr.integer import Z3Integer
from ..z3_expr.bitvector import Z3BitVector
from ..symbolic_types.symbolic_int import SymbolicInteger

log = logging.getLogger("se.z3")

class Z3Translator(object):
	def __init__(self) -> None:
		self.N = 32
		self.asserts = None
		self.query = None
		self.use_lia = True
		self.z3_expr = None

	def pcToZ3(self, pc: deque) -> Tuple:
		pcInZ3 = ()
		for pc_item in pc:
			pc_expression = pc_item.symtype.expr
			pc_res = pc_item.result
			z3_constraint = self.cToZ3(pc_expression, pc_res)
			pcInZ3 += (z3_constraint,)
		return pcInZ3

	def cToZ3(self, expr: (list | SymbolicInteger | int), res: bool) -> Any:
		if isinstance(expr, list):
			op: str = expr[0]
			args = [ self.cToZ3(a, res) for a in expr[1:] ]
			z3_l, z3_r = args[0], args[1]

			# arithmetical operations
			if op == "+":
				return z3_l + z3_r
			elif op == "-":
				return z3_l - z3_r
			elif op == "*":
				return z3_l * z3_r
			elif op == "//":
				return z3_l // z3_r
			elif op == "%":
				return z3_l % z3_r

			# bitwise
			elif op == "<<":
				return z3_l << z3_r
			elif op == ">>":
				return z3_l >> z3_r
			elif op == "^":
				return z3_l ^ z3_r
			elif op == "|":
				return z3_l | z3_r
			elif op == "&":
				return z3_l & z3_r

			# equality gets coerced to integer
			if res:
				if op == "==":
					return z3_l == z3_r
				elif op == "!=":
					return z3_l != z3_r
				elif op == "<":
					return z3_l < z3_r
				elif op == ">":
					return z3_l > z3_r
				elif op == "<=":
					return z3_l <= z3_r
				elif op == ">=":
					return z3_l >= z3_r
				else:
					grader.utils.crash("Unknown BinOp during conversion from ast to Z3 (expressions): %s" % op)
			else:
				if op == "==":
					return z3_l != z3_r
				elif op == "!=":
					return z3_l == z3_r
				elif op == "<":
					return z3_l >= z3_r
				elif op == ">":
					return z3_l <= z3_r
				elif op == "<=":
					return z3_l > z3_r
				elif op == ">=":
					return z3_l < z3_r
				else:
					grader.utils.crash("Unknown BinOp during conversion from ast to Z3 (expressions): %s" % op)

		elif isinstance(expr, SymbolicInteger):
			return Int(expr.name)

		elif isinstance(expr, int):
			return IntVal(expr)

	def symToZ3(self, sym_str: (str | list)) -> ArithRef:
		if isinstance(sym_str, str):
			return Int(sym_str)
		else:
			return self.getZ3(sym_str)
	
	def getZ3(self, sym: list) -> ArithRef:
		op, lhs, rhs = sym[0], sym[1], sym[2]
		if isinstance(lhs, list):
			lhs = self.getZ3(lhs)
		elif isinstance(lhs, str):
			lhs = Int(lhs)
		if isinstance(rhs, list):
			rhs = self.getZ3(rhs)
		elif isinstance(rhs, str):
			rhs = Int(rhs)
		if op == "+":
			return lhs + rhs
		elif op == "-":
			return lhs - rhs
		elif op == "*":
			return lhs * rhs
		elif op == "//":
			return lhs / rhs
		elif op == "%":
			return lhs % rhs
		elif op == "<=":
			return lhs <= rhs
		elif op == "<":
			return lhs < rhs
		elif op == ">":
			return lhs > rhs
		elif op == ">=":
			return lhs >= rhs

	def modelToInp(self, m: list) -> list:
		length = len(m)
		return_input = []
		for i in range(length):
			return_input.append((m[i].name(), int(m[m[i]].as_string())))
		return return_input

	def findCounterexample(self, asserts, query):
		"""Tries to find a counterexample to the query while
	  	 asserts remains valid."""
		self.solver = Solver()
		self.query = query
		self.asserts = self._coneOfInfluence(asserts, query)
		res = self._findModel()
		log.debug("Query -- %s" % self.query)
		log.debug("Asserts -- %s" % asserts)
		log.debug("Cone -- %s" % self.asserts)
		log.debug("Result -- %s" % res)
		return res
	# this is very inefficient
	def _coneOfInfluence(self, asserts, query):
		cone = []
		cone_vars = set(query.getVars())
		ws = [ a for a in asserts if len(set(a.getVars()) & cone_vars) > 0 ]
		remaining = [ a for a in asserts if a not in ws ]
		while len(ws) > 0:
			a = ws.pop()
			a_vars = set(a.getVars())
			cone_vars = cone_vars.union(a_vars)
			cone.append(a)
			new_ws = [ a for a in remaining if len(set(a.getVars()) & cone_vars) > 0 ]
			remaining = [ a for a in remaining if a not in new_ws ]
			ws = ws + new_ws
		return cone

	def _findModel(self):
		# Try QF_LIA first (as it may fairly easily recognize unsat instances)
		if self.use_lia:
			self.solver.push()
			self.z3_expr = Z3Integer()
			self.z3_expr.toZ3(self.solver,self.asserts,self.query)
			res = self.solver.check()
			#print(self.solver.assertions)
			self.solver.pop()
			if res == unsat:
				return None

		# now, go for SAT with bounds
		self.N = 32
		self.bound = (1 << 4) - 1
		while self.N <= 64:
			self.solver.push()
			(ret,mismatch) = self._findModel2()
			if (not mismatch):
				break
			self.solver.pop()
			self.N = self.N+8
			if self.N <= 64: print("expanded bit width to "+str(self.N)) 
		#print("Assertions")
		#print(self.solver.assertions())
		if ret == unsat:
			res = None
		elif ret == unknown:
			res = None
		elif not mismatch:
			res = self._getModel()
		else:
			res = None
		if self.N<=64: self.solver.pop()
		return res

	def _setAssertsQuery(self):
		self.z3_expr = Z3BitVector(self.N)
		self.z3_expr.toZ3(self.solver,self.asserts,self.query)

	def _findModel2(self):
		self._setAssertsQuery()
		int_vars = self.z3_expr.getIntVars()
		res = unsat
		while res == unsat and self.bound <= (1 << (self.N-1))-1:
			self.solver.push()
			constraints = self._boundIntegers(int_vars,self.bound)
			self.solver.assert_exprs(constraints)
			res = self.solver.check()
			if res == unsat:
				self.bound = (self.bound << 1)+1
				self.solver.pop()
		if res == sat:
			# Does concolic agree with Z3? If not, it may be due to overflow
			model = self._getModel()
			self.solver.pop()
			mismatch = False
			for a in self.asserts:
				eval = self.z3_expr.predToZ3(a,self.solver,model)
				if (not eval):
					mismatch = True
					break
			if (not mismatch):
				mismatch = not (not self.z3_expr.predToZ3(self.query,self.solver,model))
			return (res,mismatch)
		elif res == unknown:
			self.solver.pop()
		return (res,False)

	def _getModel(self):
		res = {}
		model = self.solver.model()
		for name in self.z3_expr.z3_vars.keys():
			try:
				ce = model.eval(self.z3_expr.z3_vars[name])
				res[name] = ce.as_signed_long()
			except:
				pass
		return res
	
	def _boundIntegers(self,vars,val):
		bval = BitVecVal(val,self.N,self.solver.ctx)
		bval_neg = BitVecVal(-val-1,self.N,self.solver.ctx)
		return And([ v <= bval for v in vars]+[ bval_neg <= v for v in vars])

