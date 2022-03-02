# Copyright - see copyright.txt

from symbolic.symbolic_types.symbolic_type import SymbolicType


class Predicate:
	"""Predicate is one specific ``if'' encountered during the program execution.
	   """
	def __init__(self, st: SymbolicType, result: bool) -> None:
		self.symtype = st
		self.result = result

	def getVars(self) -> list:
		return self.symtype.getVars()

	def __eq__(self, other: 'Predicate') -> bool:
		if isinstance(other, Predicate):
			res = self.result == other.result and self.symtype.symbolicEq(other.symtype)
			return res
		else:
			return False

	def __hash__(self) -> int:
		return hash(self.symtype)

	def __str__(self) -> str:
		return self.symtype.toString() + " (%s)" % (self.result)

	def __repr__(self) -> str:
		return self.__str__()

	def negate(self) -> None:
		"""Negates the current predicate"""
		assert(self.result is not None)
		self.result = not self.result

