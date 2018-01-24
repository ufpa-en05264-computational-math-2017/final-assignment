SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]

def nth_x(i):
  return "x%s" % SUB[i]

def nth_slack_x(i):
  return "xF%s" % SUB[i]
