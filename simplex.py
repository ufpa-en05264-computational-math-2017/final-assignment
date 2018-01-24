from functools import reduce
import operator

def maximization(n, objective, restrictions):
  print(n)
  print(objective)
  print(restrictions)

  if n > 3:
    print("Error: Won't handle more than 3 variables")
    raise

  objective_restriction = transform_objective_fn_to_restriction(objective)
  table = start_table(n, restrictions + [objective_restriction])

  while have_negatives(table[-1]):
    print_table(n, table)

    pivot_col = find_pivot_col(table)
    pivot_row = find_pivot_row(pivot_col, table)
    print("pivot col", pivot_col)
    print("pivot row", pivot_row)
    new_pivot_row = list(generate_new_pivot_row(pivot_row, pivot_col, table))
    table[pivot_row] = new_pivot_row
    print("new pivot row", new_pivot_row)
    # print_table(n, table)

    table = update_table_for_new_pivot_row(pivot_row, pivot_col, table)

    print_table(n, table)

  return 10

def start_table(n, restrictions):
  table = []
  slack_var_count = 0

  restrictions = list(map(restriction_to_equation, restrictions))

  for need_variable, _ in restrictions:
    if need_variable:
      slack_var_count += 1

  slack_var_index = 0
  for need_variable, equation in restrictions:
    slack_vars = [0] * slack_var_count

    if need_variable:
      slack_vars[slack_var_index] = need_variable
      slack_var_index += 1

    row = equation[:n] + slack_vars + [equation[-1]]
    table.append(row)

  return table

def restriction_to_equation(restriction):
  op = restriction[-1]
  coefficients = restriction[:-1]

  if op == "objective":
    return 1, coefficients
  elif op == "=":
    return False, coefficients
  elif op == "<=":
    return 1, coefficients
  elif op == ">=":
    return -1, coefficients
  else:
    print("Error: Invalid inequation")
    raise

def transform_objective_fn_to_restriction(objective):
  negatives = list([-x for x in objective])
  return negatives + [0, "objective"]

def print_table(n, table):
  formated_table = list(map(lambda row:
    list(
      map(lambda x: "{0:.2f}".format(round(x,2)), row)
    )
  , table))

  SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]
  slack_count = len(table[0]) - n - 1

  head = [("x%s" % SUB[i]) for i in range(1, n + 1)] + [("xF%s" % SUB[i]) for i in range(1, slack_count)] + ["Z", "b"]

  s = [[str(e) for e in row] for row in [head] + formated_table]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print('\n'.join(table))

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

  i, _ = reduce(lowest, enumerate(map(row_to_value, restriction_rows)))
  return i

def generate_new_pivot_row(pivot_row, pivot_col, table):
  pivot = table[pivot_row][pivot_col]
  pivot_inverse = 1 / pivot
  return map(lambda x: x * pivot_inverse, table[pivot_row])

def update_table_for_new_pivot_row(pivot_row, pivot_col, table):
  def sub(arg): return arg[0] - arg[1]

  def updater(entry):
    i, row = entry
    if i == pivot_row:
      return row

    return list(map(sub, zip(row,
      map(lambda x: row[pivot_col] * x, table[pivot_row])
    )))

  return list(map(updater, enumerate(table)))

def have_negatives(xs):
  return any(x < 0 for x in xs)

