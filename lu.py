def lu():
	"""Mat_A = [[2, 1, -2, 10], [3, 2, 2, 1], [5, 4, 3, 4]]"""
	"""Mat_A = [[1, 1, 1, -2], [2, 1, -1, 1], [2, -1, 1, 3]]"""
	"""Mat_A = [[3, 2, 4, 1], [1, 1, 2, 2], [4, 3, -2, 3]]"""
	"""Mat_A = [[1, 2, 1, 3], [2, -3, -1, 4], [3, -1, -2, 1]]"""
	"""Mat_A = [[2, 1, -2, 10], [3, 2, 2, 1], [5, 4, 3, 4]]"""
	"""Mat_A = [[1, 1, 1, -2], [2, 1, -1, 1], [2, -1, 1, 3]]"""
	"""Mat_A = [[3, 2, 4, 1], [1, 1, 2, 2], [4, 3, -2, 3]]"""
	"""Mat_A = [[1, 2, 1, 3], [2, -3, -1, 4], [3, -1, -2, 1]]"""
	"""Mat_A = [[1, -2, -3, -4], [4, -2, 3, 5], [2, 4, 2, 8]]"""
	"""Mat_A = [[1, -2, -3, 1], [4, -2, 3, 13], [2, 4, 2, 2]]"""
	"""Mat_A = [[4, 2, 3, 1, 12], [2, 1, 2, 1, 7], [1, 2, -1, -1, 1], [3, -3, 2, -2, 4]]"""
	"""Mat_A = [[2, 3, -1, 4], [1, 0, 2, 3], [0, 3, -1, 2]]"""
	"""Mat_A = [[3, 2, 1, -1, 5], [0, 1, 0, 3, 6], [0, -3, -5, 7, 7], [0, 2, 4, 0, 15]]"""
	"""Mat_A = [[2, -1, 4, 10], [1, 2, -3, 1], [4, -2, 5, 2]]"""
	"""Mat_A = [[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]]"""
	"""Mat_A = [[2, 1, -1, 8], [-2, 1, 2, -3], [-3, -1.5, 2, -11]]"""
	"""Mat_A = [[0, 1, 1], [1, 1, 2]]"""
	"""
	n = 3
	num = n + 1
	Vet_SL = [0] * n
	Vet_SU = [0] * n
	Vet_SL2 = [0] * n
	"""
	# Capturando dados
	n = int(input("Quantidade de variaveis: "))
	num = n+1

	# Construindo Matriz Identidade
	Mat_L = [
		[
			1 if col == row else 0
			for col in range(num)
		]
		for row in range(n)
	]

	Mat_A = [0] * n
	Vet_SL = [0] * n            #construndi vetor resolucao lower
	Vet_SL2 = [0] * n            #construndi vetor resolucao lower 2
	Vet_SU = [0] * n            #construndi vetor resolucao upper


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
		Mat_L[I][n] = Mat_A[I][n]
	print("")

	# Processamento da Eliminação de Gauss
	for I in range(n):
		K = I
		if Mat_A[I][I] == 0:  # Verifica se o Pivo é igual a zero
			for J in range(I + 1, n):
				print("pivot não serve")
			if abs(Mat_A[J][I]) > abs(Mat_A[K][I]):  # Procura um valor maior em modulo na coluna
				K = J

		if K != I:  # Se a coluna com valor maior for diferente, troca as linhas
			Mat_A[I], Mat_A[K] = Mat_A[K], Mat_A[I]

		for J in range(I + 1, n):  # Gauss Agindo
			M = Mat_A[J][I] / Mat_A[I][I]
			if I < J:  # Valores a Low
				Mat_L[J][I] = M

			for K in range(I + 1, num):
				Mat_A[J][K] -= M * Mat_A[I][K]
			Mat_A[J][I] = 0

		for I in range(n):
			print("Matriz Parcial: ", Mat_A[I][:])
		print("")

        # Calcula os valores de UPPER
	for I in range(n-1, -1, -1):
		s = sum([Mat_A[I][J]*Vet_SU[J]
			for J in range(I+1, n)])
		Vet_SU[I] = (Mat_A[I][n] - s)/Mat_A[I][I]

			# Calculando os valores LOWER
	for I in range(n):
		s = sum([Mat_L[I][J]*Vet_SL[J]
			for J in range(n)])
		Vet_SL[I] = (Mat_L[I][n] - s)/Mat_L[I][I]



        # Imprime a Matriz final
	for I in range(n):
		print("Matriz U: ", Mat_A[I][:])
	print("")
	print("Vetor Solucao X: ", Vet_SU, "\n")


	for I in range(n):
		print("Matriz L: ", Mat_L[I][:])
	print("")
	print("Vetor Solucao Y: ", Vet_SL, "\n")

            #ATE AQUI TUDO CERTO



                    #NOVOS VALORES DAS CONSTANTES B PARA MATRIZ L

	for I in range(n):
			Mat_L[I][J+1] = float(input("Digite o valor das novas constantes : "))
	print("")

	for I in range(n):
		print("nova matriz L: ", Mat_L[I][:])
	print("")

        # Calculando os valores LOWER NOVOS
	for I in range(n):
		s = sum([Mat_L[I][J]*Vet_SL2[J]
			for J in range(n)])
		Vet_SL2[I] = (Mat_L[I][n] - s)/Mat_L[I][I]
	print("Vetor Solucao novo Y: ", Vet_SL2, "\n")
        #Adicionando os valores na matriz A
	for I in range(n):
			Mat_A[I][J+1] = float(Vet_SL2[I])

	for I in range(n):
		print("nova matriz A: ", Mat_A[I][:])
	print("")

       # Calcula os valores de UPPER NOVOS
	for I in range(n-1, -1, -1):
		s = sum([Mat_A[I][J]*Vet_SU[J]
		for J in range(I+1, n)])
		Vet_SU[I] = (Mat_A[I][n] - s)/Mat_A[I][I]
	print("Vetor Solucao novo X: ", Vet_SU)
