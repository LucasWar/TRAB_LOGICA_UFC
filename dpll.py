import itertools
import numpy as np
import math 
def lerArquivo():                                       #Função para leitura do arquivo .txt e retornar suas clausulas e tambem valores iniciis como numeor de clausulas e quantidade de atomos
    teste = open('clausulas.txt')
    valoresIniciais = teste.readline()                  #ler primiera linha 
    valoresIniciais = valoresIniciais.split()           #Divide a primeira linha no com referencia no espaço criando um array com o numero de clausulas e seus atomos
    
    completeText = [] 
    clausulas = []
    for i in teste.readlines():                         #Ler os restantes das linhas apos a primera linnha(Clausulas)
        completeText.append(i)                          #Armazena cada linha em completText(Variacel auxiliar)

    
    for i in range(len(completeText)):                  #Script para retirar \n de todas os arrays que estão em completText e juntamente com os espaços em barncos dentro dos arrays dentro da matriz
        completeText[i] = completeText[i].split('\n')   #Quebra completeText em duas apartir \n separando a clausula do \n
        try:                                            #Apos chegar na ultima linha pode ocorrer error de ValueError.
            if completeText[i].index('') != -1:         #Verifica se foi gerado espaco em branco dentro de completText[i]
                del completeText[i][completeText[i].index('')] #Deleta o espaco em branco gerado pela separção do de completText[i]
        except ValueError:
            continue
    
    for i in completeText:                                      #Scipt para transcrever cada array dentro de completText em uma matriz onde cada array tem um conjunto de numero inteiro
        stringCLausula = i[0].split()                           #Separa a string em cada espaço 
        intClausula = [int(valor) for valor in stringCLausula]  #Converte em int cada numero dentro de stringClausula
        clausulas.append(list(intClausula))                     #Adiciona a clausula inteira em clausulas
    return clausulas, math.floor(math.sqrt(int(valoresIniciais[1])))




def copiar_matriz(matriz): #Função usada somente como auxilio para copiar matrizes sem criar ponteiros 
    nova_matriz = []
    for linha in matriz:
        nova_linha = [elemento for elemento in linha if isinstance(elemento, (int, float))]
        nova_matriz.append(nova_linha)
    return nova_matriz



def conferirUni(matriz): #Verifica se existe alguma clausula unitaria dentro de um conjunto de clausulas 
    for i in matriz:
        if len(i) == 1:
            return True
    return False

def remover(matriz,clausulaUni):    #Remove de dentro do conjutno de clausulas a clausulaUni 
    novaMatriz  = []                    
    novaClausula = []
    for i in matriz:                #Script usado para criar uma nova matriz deixando passar clausulas que que não possuem nem 
        if clausulaUni in i:
            continue                #Caso tenha clausulaUni nada dessa clausula sera adicionada a nova matriz e então passara para proxima clausula
        if clausulaUni*-1 in i:     #Caso tenha clausulaUni*-1 sera retirado esse valor da clausula e então sera adicionada a novaMatriz
            novaClausula = i
            delete = novaClausula.index(clausulaUni*-1)
            novaClausula.pop(delete)
            novaMatriz.append(novaClausula)
            continue
        
        novaMatriz.append(i)        #Caso não tenha nenhuma opçao da clausula uni sera adicionado diretamente a novaMatriz
    return novaMatriz      
  

def simplifica(matriz,valoracao):   #Função usada para simplifica o conjunto de clausulas e atribuir suas valorações
    unitarios = []
    novaMatriz = matriz
    for i in matriz:                #Percorre todas matriz em busca das clausulas unitarias presentes dentro da matriz                    
        if len(i) == 1:             
            unitarios.append(i[0])
         
    for i in unitarios:                     #Para cada clausula unitaria e mandando para a função remover() e retornar a nova matriz simplificada
        novaMatriz = remover(novaMatriz,i)
        # if [] in novaMatriz:
        #     return False
        if i < 0:                           #Verica a unitaria se ela for menor que zero seu valor é atribuida como False
            valoracao[abs(i)] = 'False'
        else:                               #Verica a unitaria se ela for menor que zero seu valor é atribuida como True
            valoracao[abs(i)] = 'True'
    if conferirUni(novaMatriz):             #Verifica se apos as simplificações ainda existem clausulas unitarias se sim é enviada novamente para simplificação
        return simplifica(novaMatriz,valoracao) 
    else:
        return novaMatriz,valoracao        #Caso contario retorna a matriz simplificada e as valorações atrbuida a cada atomo


def dpll(matriz,valoracao):                                 #Função principal dpll
    novaMatriz,novaValoracao = simplifica(matriz,valoracao) #Inica vericação de clausulas unitarias
    # while conferirUni(novaMatriz) == True:
    #     novaMatriz,novaValoracao = simplifica(matriz,valoracao)    
    literal = None
    if novaMatriz == []:                                    #Se a matriz ja estiver vazia siguinifica que a valoração esta correta e ja pode ser retornada
        return novaMatriz,valoracao
        
    # for linha in novaMatriz:
    #     for elemento in linha:
    #         if literal is None or abs(elemento) < literal:
    #             literal = abs(elemento)
    
    #Pega o primeiro literal presente na prmeira clausula, em caso de só existir uma unica clausula passa para o except
    try:
        literal = novaMatriz[0][0]
    except IndexError:
        literal = novaMatriz[0]

    #Inicialmente verifica se existe clausulas vazias dentro da matriz se existir retorna falso,indicando que a escolha de litral falhou
    if [] in novaMatriz:
        return False
    else: #Backtraking
        testeMatriz =copiar_matriz(novaMatriz)          #Copio a matriz para caso necessario tenho a matriz original antes de realizar alterações
        testeMatriz.append([literal])                   #Adiciono o literal ao conjunto de clausulas 
        if dpll(testeMatriz,novaValoracao) == False:    #Com isso envio para dpll novamente para que ocorar a simplificação e todos esse processo ate que se chegue em um resultado
            testeMatriz = copiar_matriz(novaMatriz)     #Caso tenha ocorrido do simplifica levar a uma clausula vazia tentaremos com outro literal na matriz que não foi alterada, e mando para testeMatriz
            testeMatriz.append([literal*-1])            #Agora adiciono o literal * -1 para testa sua outra valoração

            if dpll(testeMatriz,novaValoracao) == False: #Caso retorne falso não possivel resolver o conjunto de clausulas então será retornado falso
                return False
            else:                
                return dpll(testeMatriz,novaValoracao)   #Caso contrario sera retornado a resposta do simplidica com o literal testado 
        else:
            return dpll(testeMatriz,novaValoracao)       #Mesmo caso anterior porem com a primiera valoração o literal 
        
fnc, atomos= lerArquivo() #Atribuir os valores lidos no arquivo      
string_to_int = {}
int_to_string = {}

#Mapeamento da matriz para apresentação do resultado para todas as possiveis posições do tabuleiro, cada posição receve um valor de chave exemplo posição 1:1 tem como chave 1 e assim segue para todas posições do tabuleiro
chave = 1
for i, j in itertools.product(range(1,atomos+1), range(1,atomos+1)):
        int_to_string[chave] = f"{i}_{j}"
        chave += 1

#Mapeamento da matriz para apresentação do resultado, funciona como o loop anterior porem trocando as posições pelas chaves
chave = 1
for i, j in itertools.product(range(1,atomos+1), range(1,atomos+1)):
    string_to_int[f"{i}_{j}"] = chave
    chave+=1

#Variavel responsavel pela valorações dos atomos 
valoracao = {}

#Matriz que irá apresentar as posições das rainhas
matrizResultado = np.zeros((atomos,atomos), dtype=np.int16)

#Incia as valorações de todos atomos como indefinido
for i in range(1,(atomos*atomos)+1):
    valoracao[i] = '*'

#Clausulas, representado pela variavel fnc, e a valoração são enviadas para dpll para sejam resolvidas
matriz,valoracao = dpll(fnc,valoracao)

#Passa os resultados das valoração para resuktado criando seus atomos e seus respectivos sinais com base na valora~ção recebida
resultado = [chave if valor == 'True' else -chave for chave, valor in valoracao.items()]

#Alterar os valores na matriz resultado de acordo com cada valoração recebida nos atomos 
for x in resultado:
    if x > 0:
        position = int_to_string[x].split('_')
        matrizResultado[int(position[0])-1][int(position[1])-1] = 1

print(matrizResultado)
