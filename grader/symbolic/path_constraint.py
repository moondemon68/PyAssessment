# Copyright: see copyright.txt

import logging

from .predicate import Predicate
from .constraint import Constraint

log = logging.getLogger("se.pathconstraint")

class PathConstraint:
	def __init__(self, add, add_pc) -> None:
		self.constraints = {}
		self.add = add
		self.add_pc = add_pc
		self.root_constraint = Constraint(None, None)
		self.current_constraint = self.root_constraint
		self.expected_path = None

	def reset(self, expected: Constraint) -> None:
		self.current_constraint = self.root_constraint
		if expected == None:
			self.expected_path = None
		else:
			self.expected_path = []
			tmp = expected
			while tmp.predicate is not None:
				self.expected_path.append(tmp.predicate)
				tmp = tmp.parent

	def whichBranch(self, branch: bool, symbolic_type: Predicate) -> None:
		""" This function acts as instrumentation.
		Branch can be either True or False."""

		# add both possible predicate outcomes to constraint (tree)
		p = Predicate(symbolic_type, branch)
		self.add_pc(p)
		p.negate()
		cneg = self.current_constraint.findChild(p)
		p.negate()
		c = self.current_constraint.findChild(p)

		if c is None:
			c = self.current_constraint.addChild(p)
			# we add the new constraint to the queue of the engine for later processing
			self.add(c)
			
		# check for path mismatch
		# IMPORTANT: note that we don't actually check the predicate is the
		# same one, just that the direction taken is the same
		if self.expected_path != None and self.expected_path != []:
			expected = self.expected_path.pop()
			# while not at the end of the path, we expect the same predicate result
			# at the end of the path, we expect a different predicate result
			done = self.expected_path == []
			if ( not done and expected.result != c.predicate.result or \
				done and expected.result == c.predicate.result ):
				print("Replay mismatch (done=",done,")")
				print(expected)
				print(c.predicate)

		if cneg is not None:
			# We've already processed both
			cneg.processed = True
			c.processed = True

		self.current_constraint = c

	def toDot(self) -> str:
		# print the thing into DOT format
		header = "digraph {\n"
		footer = "\n}\n"
		return header + self._toDot(self.root_constraint) + footer

	def _toDot(self, c: Constraint) -> str:
		if (c.parent == None):
			label = "root"
		else:
			label = c.predicate.symtype.toString()
			if not c.predicate.result:
				label = "Not("+label+")"
		node = "C" + str(c.id) + " [ label=\"" + label + "\" ];\n"
		edges = [ "C" + str(c.id) + " -> " + "C" + str(child.id) + ";\n" for child in c.children ]
		return node + "".join(edges) + "".join([ self._toDot(child) for child in c.children ])
		
