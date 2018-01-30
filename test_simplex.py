import unittest
from simplex import solve_simplex

class TestSimplex(unittest.TestCase):
  def test_maximization_1(self):
    objective = [10, 12]
    constraints = [
      [1, 1, 100, '<='],
      [1, 3, 270, '<='],
    ]
    variables = [15, 85]
    solution = 1170

    problem = ["Max", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_2(self):
    objective = [6, 5, 4]
    constraints = [
      [2, 1, 1, 180, '<='],
      [1, 3, 2, 300, '<='],
      [2, 1, 2, 240, '<=']
    ]

    variables = [48, 84, 60]
    solution = 708

    problem = ["Max", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_3(self):
    objective = [2, 3, 4]
    constraints = [
      [1, 1, 1, 100, '<='],
      [2, 1, 0, 210, '<='],
      [1, 0, 0, 80, '<='],
    ]

    variables = [0, 0, 100]
    solution = 400

    problem = ["Max" , objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_4(self):
    objective = [2, 0, 4]
    constraints = [
      [1, 2, 1, 8000, '<='],
      [2, 0, 0, 6000, '<='],
      [0, 1, 1, 620, '<='],
    ]

    variables = [3000, 0, 620]
    solution = 8480

    problem = ["Max" , objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_5(self):
    objective = [6000, 10000]
    constraints = [
      [4, 2, 32, '<='],
      [2, 4, 22, '<='],
      [2, 6, 30, '<='],
    ]

    variables = [7, 2]
    solution = 62000

    problem = ["Max" , objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_6(self):
    objective = [7, 8, 10]
    constraints = [
      [2, 3, 2, 1000, '<='],
      [1, 1, 2, 800, '<='],
    ]
    variables = [200, 0, 300]
    solution = 4400

    problem = ["Max", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_7(self):
    objective = [8, 10, 7]
    constraints = [
      [1, 3, 2, 10, '<='],
      [1, 5, 1, 8, '<='],
    ]
    variables = [8, 0, 0]
    solution = 64

    problem = ["Max", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_maximization_8(self):
    objective = [50, 80]
    constraints = [
      [1, 2, 120, '<='],
      [1, 1, 90, '<='],
    ]
    variables = [60, 30]
    solution = 5400

    problem = ["Max", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_minimization_1(self):
    objective = [14, 20]
    constraints = [
      [1, 2, 4, '>='],
      [7, 6, 20, '>='],
    ]

    variables = [2, 1]
    solution = 48

    problem = ["Min", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_minimization_2(self):
    objective = [0.12, 0.15]
    constraints = [
      [60, 60, 300, '>='],
      [12, 6, 36, '>='],
      [10, 30, 90, '>=']
    ]

    variables = [3, 2]
    solution = 0.66

    problem = ["Min", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_minimization_3(self):
    objective = [3, 2]
    constraints = [
      [2, 1, 6, '>='],
      [1, 1, 4, '>=']
    ]

    variables = [2, 2]
    solution = 10

    problem = ["Min", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_minimization_4(self):
    objective = [2, 10, 8]
    constraints = [
      [1, 1, 1, 6, '>='],
      [0, 1, 2, 8, '>='],
      [-1, 2, 2, 4, '>=']
    ]

    variables = [2, 0, 4]
    solution = 36

    problem = ["Min", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def test_minimization_5(self):
    objective = [-5, -4]
    constraints = [
      [2, 2, 14, '<='],
      [6, 3, 36, '<='],
      [5, 10, 60, '<=']
    ]

    variables = [5, 2]
    solution = -33

    problem = ["Min", objective, constraints]
    self.assertProblem(problem, variables, solution)

  def assertProblem(self, problem, variables, value):
    solution = solve_simplex(*problem)
    round_vars = [round(x) for x in solution["variables"]]
    round_value = round(solution["value"])

    self.assertEqual(round_vars, [round(x) for x in variables])
    self.assertEqual(round_value, round(value))

if __name__ == '__main__':
  unittest.main()
