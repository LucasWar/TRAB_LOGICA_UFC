from pysat.solvers import Glucose4
import itertools
import numpy as np 


#result,valoracaoFinal = simplifica(fnc,valoracao)

teste = []
string_to_int = {}
int_to_string = {}
entrada = int(input("Digite o tamanho do tabuleiro: "))
#matrizResultado = np.zeros((entrada,entrada), dtype=np.int16)

nClausulas = entrada*entrada
valoracao = {}  
for i in range(1,nClausulas+1):
    valoracao[i] = '*'


chave = 1
for i, j in itertools.product(range(1,entrada+1), range(1,entrada+1)):
        int_to_string[chave] = f"{i}_{j}"
        chave += 1

chave = 1
for i, j in itertools.product(range(1,entrada+1), range(1,entrada+1)):
    string_to_int[f"{i}_{j}"] = chave
    chave+=1


g = Glucose4()

clausula = []

#Clasulas para ao menos um por linha
for x in range(1,entrada+1):
    clausula = []
    for y in range(1,entrada+1):
        clausula.append(string_to_int[f"{x}_{y}"])
    g.add_clause(clausula)
    teste.append(list(clausula))
    clausula = [-k for k in clausula]   
    
    for i in range(len(clausula)):
        clausula[i] = clausula[i] * -1
        teste.append(list(clausula))
        g.add_clause(clausula)
        clausula[i] = clausula[i] * -1
        

clausula = []
#Clasulas para ao menos um por coluna
for x in range(1,entrada+1):
    for y in range(1,entrada+1):
        clausula.append(string_to_int[f"{y}_{x}"])
    teste.append(list(clausula))
    g.add_clause(clausula)
    clausula = [-k for k in clausula]   
    
    for i in range(len(clausula)):
        clausula[i] = clausula[i] * -1
        teste.append(list(clausula))
        g.add_clause(clausula)
        clausula[i] = clausula[i] * -1   
    clausula = []

#Clasulas para somente um por linha
for x in range(1,entrada+1):
    for y in range(1,entrada+1):
        clausula.append(string_to_int[f"{x}_{y}"])
    for x in range(1,len(clausula)+1):
        for y in range(1,len(clausula)+1):
            if(x == 1 and x != y):
                teste.append(list([clausula[x-1]*-1,clausula[y-1]*-1]))
                g.add_clause([clausula[x-1]*-1,clausula[y-1]*-1])
            elif(x != y and y > x):
                teste.append(list([clausula[x-1]*-1,clausula[y-1]*-1]))
                g.add_clause([clausula[x-1]*-1,clausula[y-1]*-1])
    clausula = []        

#Clasulas para somente um por coluna
for x in range(1,entrada+1):
    for y in range(1,entrada+1):
        clausula.append(string_to_int[f"{y}_{x}"])
    for x in range(1,len(clausula)+1):
        for y in range(1,len(clausula)+1):
            if(x == 1 and x != y):
                g.add_clause([clausula[x-1]*-1,clausula[y-1]*-1])
                teste.append(list([clausula[x-1]*-1,clausula[y-1]*-1]))
            elif(x != y and y > x):
                teste.append(list([clausula[x-1]*-1,clausula[y-1]*-1]))
                g.add_clause([clausula[x-1]*-1,clausula[y-1]*-1])
    clausula = [] 

#Clasulas para somente um por diagonal principal
for linha1 in range(1,entrada+1):
    for coluna1 in range(1,entrada+1):        
        for linha2 in range(1,entrada+1):
            for coluna2 in range(1,entrada+1):
                if(linha1 != linha2 and coluna1 != coluna2 and abs(linha1 - linha2) == abs(coluna1 - coluna2)):
                    g.add_clause([string_to_int[f"{linha1}_{coluna1}"]*-1,string_to_int[f"{linha2}_{coluna2}"]*-1])
                    teste.append(list([string_to_int[f"{linha1}_{coluna1}"]*-1,string_to_int[f"{linha2}_{coluna2}"]*-1]))

#Clasulas para somente um por diagonal segundaria
for linha1 in range(1,entrada+1):
    for coluna1 in range(1,entrada+1):        
        for linha2 in range(1,entrada+1):
            for coluna2 in range(1,entrada+1):
                if(linha1 != linha2 and coluna1 != coluna2 and abs(linha1 - linha2) == abs(coluna1 - coluna2)):
                    g.add_clause([string_to_int[f"{linha1}_{entrada - coluna1 + 1}"]*-1,string_to_int[f"{linha2}_{entrada - coluna2 + 1}"]*-1])
                    teste.append(list([string_to_int[f"{linha1}_{entrada - coluna1 + 1}"]*-1,string_to_int[f"{linha2}_{entrada - coluna2 + 1}"]*-1]))



#Criacão do arquivo para entrada
arquivo = open('C:/Users/Lucas/Desktop/clausulas.txt','w')
arquivo.write(str(len(teste))+" "+str(entrada)+'\n')
for i in teste:
    arquivo.writelines((str(i).strip(']').strip('[')+'\n').replace(',',''))
print('Entrada gerada')

# valoracao = {}      
# for i in range(1,atomos+1):
#     valoracao[i] = '*'

# # g.solve()
# # result = g.get_model()
# print(fnc)
# matriz,valoracao = dpll(teste,valoracao)

# resultado = [chave if valor == 'True' else -chave for chave, valor in valoracao.items()]


# for x in resultado:
#     if x > 0:
#         position = int_to_string[x].split('_')
#         matrizResultado[int(position[0])-1][int(position[1])-1] = 1

# print(matrizResultado)

