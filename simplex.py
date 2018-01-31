from functools import reduce
from copy import deepcopy
from utils import transpose, invert_sign
import operator

OBJECTIVE_ROW = -1
B_COL = -1

def solve_simplex(kind, objective_coefficients, raw_constraints):
  ops = [raw_constraint[-1] for raw_constraint in raw_constraints]
  different_ops = len(set(ops))

  if different_ops > 1:
    print("We don't support mixed constraints")
    raise

  if kind == "Max":
    return iterate_maximization(objective_coefficients, raw_constraints)
  elif kind == "Min":
    if (all(op == ">=" for op in ops)):
      primal_problem = raw_constraints + [
        objective_coefficients + [0, "objective"]
      ]
      dual_problem = primal_problem_to_dual(primal_problem)

      dual_objective = dual_problem[-1][:-2]
      dual_var_number = len(dual_objective)
      dual_constraints = dual_problem[:-1]
      dual_solution = iterate_maximization(dual_objective, dual_constraints)

      primal_solution = deepcopy(dual_solution)

      optimal = primal_solution["iterations"][-1]

      primal_solution["variables"] = optimal[-1][dual_var_number:-1]

      return primal_solution
    elif (all(op == "<=" for op in ops)):
      dual_objective = [-coefficient for coefficient in objective_coefficients]
      result = iterate_maximization(dual_objective, raw_constraints)

      for i, table in enumerate(result["iterations"]):
        result["iterations"][i][-1][-1] = (-1) * result["iterations"][i][-1][-1]

      result["value"] = result["iterations"][-1][-1][-1]
      return result
  else:
    print("Invalid simplex kind '%s'" % kind)
    raise

def iterate_maximization(objective_coefficients, raw_constraints):
  n_vars = len(objective_coefficients)
  iterations = []
  tableau = []

  extra_variables_count = len([
    1 for raw_constraint in raw_constraints
    if raw_constraint[-1] != "="
  ])

  # Add constraints to the tableau
  current_extra_var = 0
  for raw_constraint in raw_constraints:
    # Example: [1, 2, 3, ">="] as 1x + 2y >= 3
    values = raw_constraint[:-2] # [1, 2]
    op = raw_constraint[-1] # ">="
    rhs = raw_constraint[-2] # 3
    extra_variables = [0] * extra_variables_count # [0, 0,... 0]

    if op == "<=":
      # slack variable
      extra_variables[current_extra_var] = 1
      current_extra_var = current_extra_var + 1
    elif op == ">=":
      # surplus variable
      extra_variables[current_extra_var] = -1
      current_extra_var = current_extra_var + 1

    constraint_row = values + extra_variables + [rhs]
    tableau.append(constraint_row)

  # [1, 2, 3] as Max/Min Z = 1x + 2y + 3z
  extra_variables = [0] * extra_variables_count
  # Set it to Z - 1x - 2y - 3z = 0
  objective_row = [
    -a for a in objective_coefficients
  ] + [0] + extra_variables

  tableau.append(objective_row)
  iterations.append(deepcopy(tableau))

  while (any([x < 0 for x in tableau[OBJECTIVE_ROW]])):
    # A column
    pivot_col_n = entering_variable = lowest_index(tableau[OBJECTIVE_ROW])
    pivot_row_n = leaving_variable = lowest_positive_index([
      row[B_COL] / row[entering_variable]
        if row[entering_variable] != 0 else -1
      for row in tableau
    ])

    pivot_row = tableau[pivot_row_n]
    pivot = pivot_row[pivot_col_n]
    new_pivot_row = divide_vector_by_scalar(pivot_row, pivot)

    tableau = [
      new_pivot_row if i == pivot_row_n
      else [
        row[j] - row[pivot_col_n] * tableau[pivot_row_n][j] / pivot
        for j in range(len(row))
      ]
      for i, row in enumerate(tableau)
    ]

    iterations.append(deepcopy(tableau))

  value = tableau[OBJECTIVE_ROW][B_COL]
  variables = []

  for var_i in range(n_vars):
    col = [row[var_i] for row in tableau]

    has_negatives = len([x for x in col if round(x, 2) < 0]) > 0
    count_ones = len([x for x in col if round(x, 2) == 1])

    basic_var = not has_negatives and count_ones == 1

    if basic_var:
      value_row = col.index(1)
      variables.append(tableau[value_row][B_COL])
    else:
      variables.append(0)


  return {
    "value": value,
    "variables": variables,
    "iterations": iterations,
  }

def lowest_index(row):
  current_lowest = float("inf")
  current_index = -1
  for i, value in enumerate(row):
    if value < current_lowest:
      current_lowest = value
      current_index = i
  return current_index

def lowest_positive_index(row):
  current_lowest = float("inf")
  current_index = -1
  for i, value in enumerate(row):
    if value > 0 and value < current_lowest:
      current_lowest = value
      current_index = i
  return current_index

def divide_vector_by_scalar(vector, scalar):
  return [x / scalar for x in vector]

def primal_problem_to_dual(primal):
  matrix_t = list(transpose([
    row[:-1] for row in primal
  ]))
  ops = [row[-1] for row in primal[-len(matrix_t):]]

  return [
    row + [invert_sign(ops[i])]
      for i, row in enumerate(matrix_t)
  ]

