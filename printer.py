from functools import reduce

def print_simplex_problem(problem):
  def equation(coefficients):
    with_var = [
      "%i%s" % (coefficient, nth_x(i + 1))
        for i, coefficient in enumerate(coefficients)
    ]

    return reduce(lambda a, b: 
      a + " - " + b[1:] if b[0] == "-"
      else a + " + " + b
    , with_var)

  n_vars = problem[0]
  objective = problem[1]
  restrictions = problem[2]

  print("Max. Z = %s" % equation(objective))

  for restriction in restrictions:
    op = restriction[-1]
    rhs = str(restriction[-2])
    print(equation(restriction[:-2]) + " " + op + " " + rhs)

  variables = [nth_x(i) for i in range(1, n_vars + 1)]

  print(", ".join(variables) + " >= 0")

def print_simplex_table(n, table):
  formated_table = [
    [ "{0:.2f}".format(x) for x in row
    ] for row in table
  ]

  slack_count = len(table[0]) - n - 1

  variables = [nth_x(i) for i in range(1, n + 1)]
  slack_variables = [nth_slack_x(i) for i in range(1, slack_count)]
  head = variables + slack_variables + ["Z", "b"]

  s = [[str(e) for e in row] for row in [head] + formated_table]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print('\n'.join(table))

# Utils

SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]

def nth_x(i):
  return "x%s" % SUB[i]

def nth_slack_x(i):
  return "xF%s" % SUB[i]
