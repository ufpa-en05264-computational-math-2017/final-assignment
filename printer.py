from stdio import *
from utils import nth_x, nth_slack_x, equation

def print_simplex_problem(problem):
  kind = problem[0]
  objective = problem[1]
  restrictions = problem[2]

  n_vars = len(objective)

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

  slack_count = len(table[0]) - n

  variables = [blue(nth_x(i)) for i in range(1, n + 1)]
  slack_variables = [green(nth_slack_x(i)) for i in range(1, slack_count)]
  head = variables + slack_variables + [blue("b")]

  s = [[str(e) for e in row] for row in formated_table]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [ERASE_LINE + fmt.format(*row) for row in s]
  print(ERASE_LINE + '\t'.join(head))
  print('\n'.join(table))
