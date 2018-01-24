import sys

def main():
  algorithms = ["LU", "Gauss", "Jacobi", "Seidel", "Simplex"]
  print(
    "\n".join(
      "Digit %i for %s" % (i, algo)
        for i, algo in enumerate(algorithms)
    )
  )

  algorithm_id = ask_number("Algorithm: ")

  if algorithm_id < 1 or algorithm_id > len(algorithms):
    fail("Invalid option")

  algorithm = algorithms[algorithm_id]

  update_line("Algoritm: " + blue(algorithm))
  print()

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
  pass

def seidel_handler():
  pass

def simplex_handler():
  pass

def red(str):
  return "\033[91m" + str
def green(str):
  return "\033[92m" + str
def blue(str):
  return "\033[94m" + str

def fail(str):
  sys.stderr.write(red(str) + "\n")
  exit(1)

def erase_line():
  CURSOR_UP_ONE = '\x1b[1A'
  ERASE_LINE = '\x1b[2K'
  print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

def update_line(str):
  erase_line()
  print(str)

def ask_number(prompt):
  received = input(prompt)

  try:
    return int(received)
  except:
    fail("Invalid number")

if __name__ == '__main__':
  main()
