# Copyright: see copyright.txt
from _collections_abc import dict_keys
from typing import Any

class FunctionInvocation:
	def __init__(self, function, reset) -> None:
		self.function = function
		self.reset = reset
		self.arg_constructor = {}
		self.initial_value = {}

	def callFunction(self, args: dict) -> Any:
		self.reset()
		return self.function(**args)

	def addArgumentConstructor(self, name, init, constructor) -> None:
		self.initial_value[name] = init
		self.arg_constructor[name] = constructor

	def getNames(self) -> dict_keys:
		return self.arg_constructor.keys()

	def createArgumentValue(self, name, val=None):
		if val == None:
			val = self.initial_value[name]
		return self.arg_constructor[name](name,val)

	

