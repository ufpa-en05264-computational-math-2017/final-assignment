from simplex import maximization
import printer

examples = [
  [
    2,
    [10, 12],
    [
      [1, 1, 100, '<='],
      [1, 3, 270, '<='],
    ]
  ],

  [
    3,
    [6, 5, 4],
    [
      [2, 1, 1, 180, '<='],
      [1, 3, 2, 300, '<='],
      [2, 1, 2, 240, '<=']
    ]
  ],
]

for problem in examples:
  printer.print_simplex_problem(problem)
  gen = maximization(*problem)

  for table in gen:
    printer.print_simplex_table(3, table)
    print()

  print()
  print()
  print()
