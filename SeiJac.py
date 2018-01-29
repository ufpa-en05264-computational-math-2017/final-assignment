def Seidel(A,b,x,dr,limite):
    crit = 0
    continua = 1
    converge = 1
    while(continua == 1 & converge == 1):
        xTmp = x[:]
        for i in range(0,len(A)):
            aux = 0
            for j in range(0,len(A)):
                if (i != j):
                    aux += (A[i][j]*x[j])
                    x[i] = (b[i] - aux)/A[i][i]
        continua = testa(xTmp,x,dr)
        converge = conv(xTmp,x)
        if (crit > limite):
            continua = 0
            print("No definitive solution after",crit,"iterations.")
    return x

def Jacobi(A,b,x,dr,limite):
    crit = 0
    continua = 1
    converge = 1
    while(continua == 1 & converge == 1):
        xTmp = x[:]
        for i in range(0,len(A)):
            aux = 0
            for j in range(0,len(A)):
                if (i != j):
                    aux += (A[i][j]*xTmp[j])
                    x[i] = (b[i] - aux)/A[i][i]
        continua = testa(xTmp,x,dr)
        converge = conv(xTmp,x)
        crit += 1
        if (crit > limite):
            continua = 0
            print("No definitive solution after",crit,"iterations.")
    return x

def testa(r1,r2,dr):
    result = 0
    print("\nFor answer array\n",r2)
    for i in range(0,len(r1)):
        print("Deviation x",(i+1),"=",abs(r1[i] - r2[i]))
        if (abs(r1[i] - r2[i]) >= dr ):
            result = 1
    return result

def conv(r1,r2):
    result = 1
    for i in range(0,len(r1)):
        if (abs(r1[i] - r2[i]) > 9999):
            result = 0
            print("Deviation too big, system does not converge.")
            break
    return result

def escolha(A,b,x,dr,limite,swi):
    validade = 1
    if (swi == "J"):
        print("Answer:",Jacobi(A,b,x,dr,limite))
    elif (swi == "S"):
        print("Answer:",Seidel(A,b,x,dr,limite))
    else:
        print("Invalid option, returning. (this message should never appear!)")
        validade = 0
    return validade

def menu(varQ,limite,esco):
    if(varQ >= 1):
        matX = [x[:] for x in [[0.0]*(varQ+1)]*varQ]
        
        for i in range(varQ):
            for j in range(varQ+1):
                print("System:",matX)
                print("Line:",i+1,"Column",j+1,":")
                matX[i][j] = float(input())
        
        res = [0.0]*varQ
        vet = [0.0]*varQ
        mat = [x[:] for x in [[0.0]*(varQ)]*varQ]


        zeroOnDiag = 0
        for i in range(0,varQ):
            vet[i] = matX[i][varQ]
            for j in range(0,varQ):
                mat[i][j] = matX[i][j]

        for i in range(0,varQ):
            if (mat[i][i] == 0.0):
                zeroOnDiag = 1


        if (zeroOnDiag == 0):
            desV = float(input("Max dr:"))

            print("System:",matX)
            
            
            escolha(mat,vet,res,desV,limite,esco)
        else:
            print("Zero at main diagonal. Will not divide by 0")
        

def mainJS(prog):
    limite = 999
    varQ = 1
    while(varQ >= 1):
        varQ = int(input("How many variables? (0 to finalize):"))
        menu(varQ,limite,prog)
        
        

def testeSeidel():
    S = [[7.0, 3.0, -1.0, 2.0], [3.0, 8.0, 1.0, -4.0], [-1.0, 1.0, 4.0, -1.0], [2.0, -4.0, -1.0, 6.0]]
    a = [-1.0, 0.0, -3.0, 1.0]
    y = [0.0]*len(S)
    d = 0.00001
    l = 999
    Seidel(S,a,y,d,l)

def testeJacobi():
    J = [[-0.5, 1.0], [2.0, 5.0]]
    ac= [1.0, -13.0]
    o = [0.0]*len(J)
    b = 0.000000000001
    e = 999
    Jacobi(J,ac,o,b,e)
