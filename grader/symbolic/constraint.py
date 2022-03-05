# Copyright: see copyright.txt

import logging
from typing import Tuple

from grader.symbolic.predicate import Predicate

log = logging.getLogger("se.constraint")

class Constraint:
	cnt = 0
	"""A constraint is a list of predicates leading to some specific
	   position in the code."""
	def __init__(self, parent: 'Constraint', last_predicate: Predicate) -> None:
		self.inputs = None
		self.predicate = last_predicate
		self.processed = False
		self.parent = parent
		self.children = []
		self.id = self.__class__.cnt
		self.__class__.cnt += 1

	def __eq__(self, other: 'Constraint') -> bool:
		"""Two Constraints are equal iff they have the same chain of predicates"""
		if isinstance(other, Constraint):
			if not self.predicate == other.predicate:
				return False
			return self.parent is other.parent
		else:
			return False

	def getAssertsAndQuery(self) -> Tuple[list, Predicate]:
		self.processed = True

		# collect the assertions
		asserts = []
		tmp = self.parent
		while tmp.predicate is not None:
			asserts.append(tmp.predicate)
			tmp = tmp.parent

		return asserts, self.predicate	       

	def getPath(self) -> str:
		if self.parent == None:
			return ''
		return self.parent.getPath() + ' ' + str(self.predicate)

	def getLength(self) -> int:
		if self.parent == None:
			return 0
		return 1 + self.parent.getLength()

	def __str__(self) -> str:
		return str(self.predicate) + "  (processed: %s, path_len: %d, path: %s)" % (self.processed, self.getLength(), self.getPath())

	def __repr__(self) -> str:
		s = repr(self.predicate) + " (processed: %s)" % (self.processed)
		if self.parent is not None:
			s += "\n  path: %s" % repr(self.parent)
		return s

	def findChild(self, predicate: Predicate) -> 'Constraint':
		# log.debug("children: %s" % self.children)
		for c in self.children:
			if predicate == c.predicate:
				return c
		return None

	def addChild(self, predicate: Predicate) -> 'Constraint':
		assert(self.findChild(predicate) is None)
		c = Constraint(self, predicate)
		self.children.append(c)
		return c

