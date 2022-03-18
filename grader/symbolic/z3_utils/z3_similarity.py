# for comparing and getting similarity score
from typing import List
from z3 import BoolRef, ArithRef, simplify, Tactic

# calculate similarity between path constraints
# both path constraints are already in the conjunctive normal form
def similarity(reference: BoolRef, student: BoolRef) -> float:
  referenceSimplified = simplifyExpression(reference)
  studentSimplified = simplifyExpression(student)

  # after simplification, all same expressions should have the same form
  # similarity score using jaccard similarity:
  # the number of reference expressions that is present in student expressions list, divided by
  # the number of expressions
  total = len(referenceSimplified) + len(studentSimplified)

  # both expressions are empty and equal
  if total == 0:
    return 1
  
  intersect = 0
  for r in referenceSimplified:
    if r in studentSimplified:
      intersect += 1
  
  union = total - intersect
  return intersect/union

# simplification techniques used to get a uniform form of expression:
# arith_ineq_lhs => rewrite inequalities so that right-hand-side is a constant
# sort_sums => sort the arguments of + application
# solve-eqs => eliminate variables by solving equations
def simplifyExpression(expr: BoolRef | ArithRef) -> List[BoolRef | ArithRef]:
  expr = simplify(expr, arith_ineq_lhs=True, sort_sums=True)
  t = Tactic('solve-eqs')
  applyResult = t.apply(expr)
  return applyResult[0]
