import sys

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

def ask_int(prompt):
  received = input(prompt)

  try:
    return int(received)
  except:
    fail("Invalid number")

def ask_float(prompt):
  received = input(prompt)

  try:
    return float(received)
  except:
    fail("Invalid number")

def empty_line():
  print(ERASE_LINE)
