
from simplex import maximization

SUB = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]

print(maximization(
  3,
  [6, 5, 4],
  [
    [2, 1, 1, 180, '<='],
    [1, 3, 2, 300, '<='],
    [2, 1, 2, 240, '<=']
  ]
))

# print("10x%s" % SUB[1])
