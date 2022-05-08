import random

class RandomGradingEngine:
    def __init__(self, funcinv, funcinvStudent, solver="z3"):
        random.seed(0)
        self.inputs = {}
        self.funcinv = funcinv
        self.funcinvStudent = funcinvStudent
        self.init_inputs()
        self.tested_case = {}
        self.wrong_case = {}

    def init_inputs(self):
        for arg in self.funcinv.getNames():
            self.inputs[arg] = 0

    def randomize_inputs(self):
        for arg in self.funcinv.getNames():
            self.inputs[arg] = random.randint(-100, 100)
    
    def grade(self):
        for i in range(1000):
            self.randomize_inputs()
            ret = self.funcinv.callFunction(self.inputs)
            retStudent = self.funcinvStudent.callFunction(self.inputs)
            self._add_test_case(ret, retStudent)
        return self.tested_case, self.wrong_case

    def _inputs_dict_to_tuple(self):
        tup = []
        for key in self.inputs:
            tup.append((key, self.inputs[key]))
        return tuple(tup)

    def _add_test_case(self, ret, retStudent):
        self.tested_case[self._inputs_dict_to_tuple()] = (ret, retStudent)
        if ret != retStudent:
            self.wrong_case[self._inputs_dict_to_tuple()] = (ret, retStudent)
