#!/usr/bin/env python3

import sys
from utils import nth_x, equation
from simplex import maximization
from SeiJac import mainJS
import printer

def main():
  algorithms = ["LU", "Gauss", "Jacobi", "Seidel", "Simplex"]
  print(
    "\n".join(
      "Input %i for %s" % (i + 1, algo)
        for i, algo in enumerate(algorithms)
    )
  )

  algorithm_id = ask_number("Algorithm: ")

  if algorithm_id < 1 or algorithm_id > len(algorithms):
    fail("Invalid option")

  algorithm = algorithms[algorithm_id - 1]

  update_line("Algoritm: " + blue(algorithm))
  empty_line()

  options = { 1: lu_handler,
              2: gauss_handler,
              3: jacobi_handler,
              4: seidel_handler,
              5: simplex_handler
            }

  options[algorithm_id]()

def lu_handler():
  pass

def gauss_handler():
  pass

def jacobi_handler():
  print("Starting Jacobi")
  mainJS("J")
  print("Ending Jacobi")
  main()

def seidel_handler():
  print("Starting Seidel")
  mainJS("S")
  print("Ending Seidel")
  main()

def simplex_handler():
  # Assumes maximization. TODO: minimization
  prompt = "Number of variables: "
  n_vars = ask_number(prompt)
  update_line(prompt + blue(str(n_vars)))

  prompt = "Number of restrictions: "
  n_restrictions = ask_number(prompt)
  update_line(prompt + blue(str(n_restrictions)))

  empty_line()

  objective = []

  prompt = "Max. Z = "
  print(prompt)

  for i in range(1, n_vars + 1):
    x = ask_number(nth_x(i) + " = ")
    objective.append(x)
    erase_line()
    update_line(prompt + equation(objective))

  restrictions = []

  for i in range(1, n_restrictions + 1):
    print("Restriction (" + str(i) + "/" + str(n_restrictions) + ")")
    current_restriction = []

    # Ask coefficients

    for j in range(1, n_vars + 1):
      x = ask_number(nth_x(j) + " = ")
      current_restriction.append(x)
      erase_line()
      update_line(equation(current_restriction))

    # Ask operation

    op = input("Operation (<=, =, >=)? ")

    if op not in ["<=", "=", ">="]:
      fail("Invalid operation " + op)

    erase_line()
    update_line(equation(current_restriction) + " " + op)

    # Ask `b`

    b = ask_number("b = ")

    erase_line()
    update_line(equation(current_restriction) + " " + op + " " + str(b))

    restrictions.append(current_restriction + [b, op])

  problem = [n_vars, objective, restrictions]

  empty_line()

  gen = maximization(*problem)

  for table in gen:
    printer.print_simplex_table(n_vars, table)
    empty_line()

  empty_line()

END_COLOR = '\033[0m'
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
def red(str):
  return "\033[91m" + str + END_COLOR
def green(str):
  return "\033[92m" + str + END_COLOR
def blue(str):
  return "\033[94m" + str + END_COLOR

def fail(str):
  sys.stderr.write(red(str) + "\n")
  exit(1)

def erase_line():
  sys.stdout.write(CURSOR_UP_ONE + ERASE_LINE)

def update_line(str):
  print(CURSOR_UP_ONE + ERASE_LINE + str)

def ask_number(prompt):
  received = input(prompt)

  try:
    return int(received)
  except:
    fail("Invalid number")

def empty_line():
  print(ERASE_LINE)

if __name__ == '__main__':
  main()
