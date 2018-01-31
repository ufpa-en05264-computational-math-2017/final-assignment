#!/usr/bin/env python3
from stdio import *
from utils import nth_x, equation
from SeiJac import mainJS
from simplex import solve_simplex
import printer

def main():
  algorithms = ["LU", "Gauss", "Jacobi", "Seidel", "Simplex"]
  print(
    "\n".join(
      "Input %i for %s" % (i + 1, algo)
        for i, algo in enumerate(algorithms)
    )
  )

  algorithm_id = ask_int("Algorithm: ")

  if algorithm_id == 0:
    return

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
  prompt = "Number of variables: "
  n_vars = ask_int(prompt)
  update_line(prompt + blue(str(n_vars)))

  prompt = "Number of restrictions: "
  n_restrictions = ask_int(prompt)
  update_line(prompt + blue(str(n_restrictions)))

  empty_line()

  objective = []

  prompt = "Kind (Max, Min): "
  kind = input(prompt)

  if kind not in ["Max", "Min"]:
    print(red("Invalid kind %s" % kind))
    exit(1)

  erase_line()
  prompt = blue(kind) + ". Z = "
  print(prompt)

  for i in range(1, n_vars + 1):
    x = ask_float(nth_x(i) + " = ")
    objective.append(x)
    erase_line()
    update_line(prompt + equation(objective))

  restrictions = []

  for i in range(1, n_restrictions + 1):
    print("Restriction (" + str(i) + "/" + str(n_restrictions) + ")")
    current_restriction = []

    # Ask coefficients

    for j in range(1, n_vars + 1):
      x = ask_float(nth_x(j) + " = ")
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

    b = ask_float("b = ")

    erase_line()
    update_line(equation(current_restriction) + " " + op + " " + str(b))

    restrictions.append(current_restriction + [b, op])

  problem = [kind, objective, restrictions]

  empty_line()

  gen = solve_simplex(*problem)

  for table in gen["iterations"]:
    printer.print_simplex_table(n_vars, table)
    empty_line()

  empty_line()

  solution = str(round(gen["value"], 2))
  str_vars = [
    green(str(round(x, 2))) if x > 0
    else red(str(round(x, 2)))
    for x in gen["variables"]
  ]
  print("x = (" + ", ".join(str_vars) + ")")
  print(kind + ". Z = " + blue(solution))

if __name__ == '__main__':
  main()
