def lu():
  Mat_L = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
  """Mat_L = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0],[0, 0, 0, 1, 0]]"""
  """Mat_A = [[0, 1, -2, 10], [3, 2, 2, 1], [5, 4, 3, 4]]"""
  # Mat_A = [[1, 1, 1, -2], [2, 1, -1, 1], [2, -1, 1, 3]]
  """Mat_A = [[3, 2, 4, 1], [1, 1, 2, 2], [4, 3, -2, 3]]"""
  """Mat_A = [[1, 2, 1, 3], [2, -3, -1, 4], [3, -1, -2, 1]]"""
  """Mat_A = [[1, -2, -3, -4], [4, -2, 3, 5], [2, 4, 2, 8]]"""
  """Mat_A = [[1, -2, -3, 1], [4, -2, 3, 13], [2, 4, 2, 2]]"""
  """Mat_A = [[4, 2, 3, 1, 12], [2, 1, 2, 1, 7], [1, 2, -1, -1, 1], [3, -3, 2, -2, 4]]"""
  """Mat_A = [[2, 3, -1, 4], [1, 0, 2, 3], [0, 3, -1, 2]]"""
  """Mat_A = [[3, 2, 1, -1, 5], [0, 1, 0, 3, 6], [0, -3, -5, 7, 7], [0, 2, 4, 0, 15]]"""

  n = 3
  num = n + 1

  # Capturando dados
  n = int(input("Quantidade de variaveis: "))

  Mat_L = [
    [
      1 if col == row else 0
      for col in range(n + 1)
    ]
    for row in range(n)
  ]

  num = n + 1
  Mat_A = [0] * n
  # Construindo a Matriz A
  for I in range(n):
      Mat_A[I] = [0] * num
  for I in range(n):
      for J in range(num):
          Mat_A[I][J] = float(input("Digite o valor das variaveis: "))
  # Tudo igual daqui para baixo
  # Imprime a Matriz A
  for I in range(n):
    print("Matriz A: ", Mat_A[I][:])
  print("")
  # Processamento da Eliminação de Gauss
  for I in range(n):
    K = I

    if Mat_A[I][I] == 0:							# Verifica se o Pivo é igual a zero
      for J in range(I + 1, n):
        print("pivot não serve")
      if abs(Mat_A[J][I]) > abs(Mat_A[K][I]):     # Procura um valor maior em modulo na coluna
        K = J

    if K != I:                                      # Se a coluna com valor maior for diferente, troca as linhas
      Mat_A[I], Mat_A[K] = Mat_A[K], Mat_A[I]
    

    for J in range(I + 1, n):						# Gauss Agindo
      M = Mat_A[J][I] / Mat_A[I][I]
      if I < J:									# Valores a Low
        Mat_L[J][I] = M

      for K in range(I+1, num):
        if num == num: 						# Valores a Low
          Mat_L[I][n] = Mat_A[I][n]
        Mat_A[J][K] -= M * Mat_A[I][K]
      Mat_A[J][I] = 0


    for I in range(n):
      print("Matriz Parcial: ", Mat_A[I][:])		
    print("")
  # Calcula os valores de X, Y , Z Upper
  for L in range(n-1, 1, -1):
    if L == L:
      ZU = Mat_A[L][n] / Mat_A[L][L]
      L = L - 1
    if L == L:
      YU = (Mat_A[L][n] - (Mat_A[L][L+1] * ZU)) / Mat_A[L][L]
      L = L - 1
    if L == L:
      XU = (Mat_A[L][n] - (Mat_A[L][L+2] * ZU) - (Mat_A[L][L+1] * YU)) / Mat_A[L][L]
      break
  # Calculando os valores X, Y, Z Lower
  for L in range(n):
    if L == L: #1
      XL = Mat_L[L][n] / Mat_L[L][L]
      L = L + 1
    if L == L: #2
      YL = Mat_L[L][n] - (Mat_A[L][L-1] * XL) / Mat_A[L][L]
      L = L + 1
    if L == L: #3
      ZL = Mat_A[L][n] - (Mat_A[L][L-1] * YL) - (Mat_A[L][L-2] * XL) / Mat_A[L][L]
      break
  # Imprime a Matriz final
  for I in range(n):
    print("Matriz Upper: ", Mat_A[I][:])
  for I in range(n):
      print("Matriz Low: ", Mat_L[I][:])


  print("Valores de upper: \nX = %s\nY = %s\nZ = %s"%(XU,YU,ZU))
  print("Valores de lower: \nX = %s\nY = %s\nZ = %s"%(XL,YL,ZL))
