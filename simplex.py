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
    return iterate_maximization(kind, objective_coefficients, raw_constraints)
  elif kind == "Min":
    if (all(op == ">=" for op in ops)):
      primal_problem = raw_constraints + [
        objective_coefficients + [0, "objective"]
      ]
      dual_problem = primal_problem_to_dual(primal_problem)

      dual_objective = dual_problem[-1][:-2]
      dual_var_number = len(dual_objective)
      dual_constraints = dual_problem[:-1]
      dual_problem = ["Max", dual_objective, dual_constraints]

      dual_solution = iterate_maximization(*dual_problem)

      primal_solution = deepcopy(dual_solution)

      optimal = primal_solution["iterations"][-1]

      primal_solution["variables"] = optimal[-1][dual_var_number:-1]

      return primal_solution
    elif (all(op == "<=" for op in ops)):
      dual_objective = [-coefficient for coefficient in objective_coefficients]
      dual_problem = ["Max", dual_objective, raw_constraints]

      result = iterate_maximization(*dual_problem)

      for i, table in enumerate(result["iterations"]):
        result["iterations"][i][-1][-1] = (-1) * result["iterations"][i][-1][-1]

      result["value"] = result["iterations"][-1][-1][-1]
      return result
  else:
    print("Invalid simplex kind '%s'" % kind)
    raise

def iterate_maximization(kind, objective_coefficients, raw_constraints):
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

  # TODO: handle minimization
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
    # TODO: handle minimization case
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

def multiply_vector_by_scalar(vector, scalar):
  return [x * scalar for x in vector]

# def add_vectors(xs, ys):
#   return [x + ys[i] for i, x in enumerate(xs)]

def subtract_vectors(xs, ys):
  return [x - ys[i] for i, x in enumerate(xs)]

# def solve_simplex(kind, objective, restrictions):
#   n_vars = len(objective)

#   if not kind in ["Max", "Min"]:
#     print("Invalid kind '%s'" % kind)

#   if kind == "Max":
#     return maximization(n_vars, objective, restrictions)
#   else:
#     return minimization(n_vars, objective, restrictions)

def maximization(n, objective, restrictions):
  if n > 3:
    print("Error: Won't handle more than 3 variables")
    raise

  objective_restriction = transform_objective_fn_to_restriction(objective)
  table = start_table(n, restrictions + [objective_restriction])

  iterations = []
  iterations.append(deepcopy(table))

  while have_negatives(table[-1]):
    pivot_col = find_pivot_col(table)
    pivot_row = find_pivot_row(pivot_col, table)

    # Update pivot_row
    pivot = table[pivot_row][pivot_col]
    pivot_inverse = 1 / pivot
    new_pivot_row = list([x * pivot_inverse for x in table[pivot_row]])
    table[pivot_row] = new_pivot_row

    table = update_table_for_new_pivot_row(pivot_row, pivot_col, table)
    iterations.append(deepcopy(table))

  optimal = iterations[-1]
  variables = []

  for i in range(n):
    try:
      j = list([row[i] for row in optimal]).index(1)
      variables.append(optimal[j][-1])
    except:
      variables.append(0)

  solution = optimal[-1][-1]

  return {
    "value": solution,
    "variables": variables,
    "iterations": iterations,
  }

def minimization(n, objective, restrictions):
  ops = [restriction[-1] for restriction in restrictions]

  if (all(op == ">=" for op in ops)):
    primal_problem = restrictions + [objective + [0, "objective"]]
    dual_problem = primal_problem_to_dual(primal_problem)

    dual_objective = dual_problem[-1][:-2]
    dual_var_number = len(dual_objective)
    dual_restrictions = dual_problem[:-1]
    standard_form = True
  elif (all(op == "<=" for op in ops)):
    dual_objective = [-coefficient for coefficient in objective]
    result = maximization(n, dual_objective, restrictions)
    result["value"] = (-1) * result["iterations"][-1][-1][-1]
    return result
  else:
    dual_var_number = n
    dual_objective = [-coefficient for coefficient in objective]
    dual_restrictions = restrictions
    standard_form = False

  dual_problem = [dual_var_number, dual_objective, dual_restrictions]

  iterations = []

  # The dual problem shows us [variables] + [slack] + [Z, b]
  # but for the primal it's [slack] + [variables] + [Z, b]
  # as slack variables in the dual are variables in the primal and so go on.
  START_VARIABLES = dual_var_number # From the right: ignore [Z, b] and move `n` vars left
  END_VARIABLES = -1 # Stops before [Z, b]
  START_SLACK_VARIABLES = 0
  END_SLACK_VARIABLES = START_VARIABLES

  for table in maximization(*dual_problem)["iterations"]:
    if standard_form:
      min_table = [
        row[START_VARIABLES:END_VARIABLES] +
        row[START_SLACK_VARIABLES:END_SLACK_VARIABLES] +
        row[-1:]
        for row in table
      ]

      if not standard_form:
        min_table[-1][-1] = min_table[-1][-1] * (-1)

      iterations.append(deepcopy(min_table))
    else:
      iterations.append(deepcopy(table))

  optimal = iterations[-1]
  variables = [x for x in optimal[-1][:n]] if standard_form else [row[-1] for row in optimal[:n]]
  solution = optimal[-1][-1]

  return {
    "value": solution,
    "variables": variables,
    "iterations": iterations,
  }

def start_table(n, restrictions):
  def need_variable(restriction):
    return restriction[0] == 1 or restriction[0] == -1

  table = []

  restrictions = list(map(restriction_to_equation, restrictions))

  slack_var_count = len([
    True for restriction in restrictions
    if need_variable(restriction)
  ])

  slack_var_index = 0
  for restriction in restrictions:
    equation = restriction[1]

    slack_vars = [0] * slack_var_count

    if need_variable(restriction):
      sign = restriction[0]
      slack_vars[slack_var_index] = sign
      slack_var_index += 1

    row = equation[:n] + slack_vars + [equation[-1]]
    table.append(row)

  return table

def primal_problem_to_dual(primal):
  matrix_t = list(transpose([
    row[:-1] for row in primal
  ]))
  ops = [row[-1] for row in primal[-len(matrix_t):]]

  return [
    row + [invert_sign(ops[i])]
      for i, row in enumerate(matrix_t)
  ]

def restriction_to_equation(restriction):
  op = restriction[-1]
  coefficients = restriction[:-1]

  if op == "objective":
    return False, coefficients
  elif op == "=":
    return False, coefficients
  elif op == "<=":
    return 1, coefficients
  elif op == ">=":
    return -1, coefficients
  else:
    print("Error: Invalid inequation sign", op)
    raise

def transform_objective_fn_to_restriction(objective):
  negatives = list([-x for x in objective])
  return negatives + [0, "objective"]

def find_pivot_col(table):
  def lowest(a, b): return a if a[1] < b[1] else b
  last_row = table[-1]
  i, _ = reduce(lowest, enumerate(last_row))
  return i

def find_pivot_row(pivot_col, table):
  def row_to_value(row):
    pivot_col_member = row[pivot_col]
    if pivot_col_member == 0:
      return -1
    b = row[-1]
    return b / pivot_col_member

  def lowest(a, b): return b if b[1] > 0 and b[1] < a[1] else a
  restriction_rows = table[:-1]

  # This will be the start value.
  # Since lowest won't check the current value of reduce for zeros
  # It's a must so we won't get 0 pivots therefore x/0 later.
  dummy = [None, float("inf")]
  i, _ = reduce(lowest, [dummy] + list(enumerate(map(row_to_value, restriction_rows))))
  return i

def update_table_for_new_pivot_row(pivot_row, pivot_col, table):
  # def sub(arg): return arg[0] - arg[1]

  # def updater(entry):
  #   i, row = entry
  #   if i == pivot_row:
  #     return row

  #   return list([
  #     zip(
  #       row,
  #       [row[pivot_col] * x for x in table[pivot_row]]
  #     )
  #   ])
  #   return list(map(sub, zip(row,
  #     map(lambda x: row[pivot_col] * x, table[pivot_row])
  #   )))

  new_table = []

  for i, row in enumerate(table):
    if i == pivot_row:
      new_table.append(deepcopy(row))
      continue

    pivot_subtractors = [row[pivot_col] * x for x in table[pivot_row]]

    new_row = list([
      row[i] - pivot_subtractors[i]
        for i in range(len(row))
    ])

    new_table.append(new_row)

    # new_row = list([
    #   a[0] - b[0]
    #   for ((a, b)) in
    #     zip(row, [row[pivot_col] * x for x in table[pivot_row]])
    # ])

  return new_table
  # return list(map(updater, enumerate(table)))



def have_negatives(xs):
  return any(x < 0 for x in xs)
