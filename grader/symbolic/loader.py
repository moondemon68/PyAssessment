# Copyright: copyright.txt

import inspect
import re
import os
import sys
from types import ModuleType
from typing import Any
from .invocation import FunctionInvocation
from .symbolic_types import SymbolicInteger, getSymbolic

# The built-in definition of len wraps the return value in an int() constructor, destroying any symbolic types.
# By redefining len here we can preserve symbolic integer types.
import builtins
builtins.len = (lambda x : x.__len__())

class Loader:
	def __init__(self, filename: str) -> None:
		self._fileName: str = os.path.basename(filename)
		self._fileName: str = self._fileName[:-3]
		self._entryPoint: str = self._fileName
		self._resetCallback(True)

	def getFile(self) -> str:
		return self._fileName

	def getEntry(self) -> str:
		return self._entryPoint
	
	def createInvocation(self) -> FunctionInvocation:
		inv: FunctionInvocation = FunctionInvocation(self._execute, self._resetCallback)
		func = self.app.__dict__[self._entryPoint]
		argspec = inspect.getargspec(func)
		# check to see if user specified initial values of arguments
		if "concrete_args" in func.__dict__:
			for (f,v) in func.concrete_args.items():
				if not f in argspec.args:
					print("Error in @concrete: " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				else:
					Loader._initializeArgumentConcrete(inv,f,v)
		if "symbolic_args" in func.__dict__:
			for (f,v) in func.symbolic_args.items():
				if not f in argspec.args:
					print("Error (@symbolic): " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				elif f in inv.getNames():
					print("Argument " + f + " defined in both @concrete and @symbolic")
					raise ImportError()
				else:
					s = getSymbolic(v)
					if (s == None):
						print("Error at argument " + f + " of entry point " + self._entryPoint + " : no corresponding symbolic type found for type " + str(type(v)))
						raise ImportError()
					Loader._initializeArgumentSymbolic(inv, f, v, s)
		for a in argspec.args:
			if not a in inv.getNames():
				Loader._initializeArgumentSymbolic(inv, a, 0, SymbolicInteger)
		return inv

	# need these here (rather than inline above) to correctly capture values in lambda
	def _initializeArgumentConcrete(inv, f: str, val) -> None:
		inv.addArgumentConstructor(f, val, lambda n,v: val)

	def _initializeArgumentSymbolic(inv, f: str, val, st: type) -> None:
		inv.addArgumentConstructor(f, val, lambda n,v: st(n,v))

	def executionComplete(self, return_vals: list) -> bool:
		if "expected_result" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result"]())
		if "expected_result_set" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result_set"](), False)
		else:
			return None

	# -- private

	def _resetCallback(self, firstpass=False) -> None:
		self.app: ModuleType = None
		if firstpass and self._fileName in sys.modules:
			print("There already is a module loaded named " + self._fileName)
			raise ImportError()
		try:
			if (not firstpass and self._fileName in sys.modules):
				del(sys.modules[self._fileName])
			self.app: ModuleType =__import__(self._fileName)
			if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
				print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
				raise ImportError()
		except Exception as arg:
			print("Couldn't import " + self._fileName)
			print(arg)
			raise ImportError()

	def _getFunc(self, **args: dict) -> Any:
		return self.app.__dict__[self._entryPoint]

	def _execute(self, **args: dict) -> Any:
		return self.app.__dict__[self._entryPoint](**args)

	def _toBag(self, l: list) -> dict:
		bag = {}
		for i in l:
			if i in bag:
				bag[i] += 1
			else:
				bag[i] = 1
		return bag

	def _check(self, computed: list, expected: list, as_bag=True) -> bool:
		b_c = self._toBag(computed)
		b_e = self._toBag(expected)
		if as_bag and b_c != b_e or not as_bag and set(computed) != set(expected):
			print("-------------------> %s test failed <---------------------" % self._fileName)
			print("Expected: %s, found: %s" % (b_e, b_c))
			return False
		else:
			print("%s test passed <---" % self._fileName)
			return True
	
def loaderFactory(filename: str) -> Loader:
	if not os.path.isfile(filename) or not re.search(".py$",filename):
		print("Please provide a Python file to load")
		return None
	try: 
		dir = os.path.dirname(filename)
		sys.path = [ dir ] + sys.path
		ret = Loader(filename)
		return ret
	except ImportError:
		sys.path = sys.path[1:]
		return None


