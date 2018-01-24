def print_simplex_problem(problem):
  objective = [
    "%i%s" % (coefficient, nth_x(i + 1)) for i, coefficient in enumerate(problem[1])
  ]

  print("Max. Z = %s" % " + ".join(objective))
  return 1

def print_simplex_table(n, table):
  formated_table = list(map(lambda row:
    list(map(lambda x: "{0:.2f}".format(round(x, 2)), row))
  , table))

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
