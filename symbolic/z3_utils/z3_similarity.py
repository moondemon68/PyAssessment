# for comparing and getting similarity score
from typing import List
from z3 import BoolRef, ArithRef, simplify, Tactic

# calculate similarity between path constraints
# both path constraints are already in the conjunctive normal form
def similarity(reference: BoolRef, student: BoolRef) -> float:
  reference = simplifyExpression(reference)
  student = simplifyExpression(student)

  # after simplification, all same expressions should have the same form
  # similarity score is counted by summing:
  # the number of reference expressions that is present in student expressions list
  # the number of student expressions that is present in reference expressions list
  total = len(reference) + len(student)
  present = 0
  for r in reference:
    if r in student:
      present += 1
  for s in student:
    if s in reference:
      present += 1
  
  return present/total

# simplification techniques used to get a uniform form of expression:
# arith_ineq_lhs => rewrite inequalities so that right-hand-side is a constant
# sort_sums => sort the arguments of + application
# solve-eqs => eliminate variables by solving equations
def simplifyExpression(expr: BoolRef | ArithRef) -> List[BoolRef | ArithRef]:
  expr = simplify(expr, arith_ineq_lhs=True, sort_sums=True)
  t = Tactic('solve-eqs')
  applyResult = t.apply(expr)
  return applyResult[0]
