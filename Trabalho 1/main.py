# Aluna: Ana Caroline da Rocha Braz
# Matrícula: 212008482

# Para realização do trabalho foi utilizado como base, para construir a classe Grafo, o código do site:
# https://algoritmosempython.com.br/cursos/algoritmos-python/algoritmos-grafos/representacao-grafos/
# no entanto, no site o código é mais referente a grafo direcionado, sendo assim foi necessário a adaptação para grafo não direcionado
# Para os Algoritmos, foi utilizado como base o pseudocódigo passado em sala, nos slides da aula 5. 
# Também foi utilizado como base o livro utilizado na matéria de Estrutura de Dados 2021.2 que pode ser visto neste site:
# https://panda.ime.usp.br/pythonds/static/pythonds_pt/index.html


#Grado sem direção e peso
class Grafo:

    # Inicializa a estrutura através de dicionário onde cada vértice será uma chave
    def __init__(self): 
        self.grafo = {}
    
    # Adiciona o vertice no dicionário e após na respectiva adj.
    def adiciona_aresta(self, v1, v2): 
        if v1 not in self.grafo:
            self.grafo[v1] = set()
        if v2 not in self.grafo:
            self.grafo[v2] = set()
        
        self.grafo[v1].add(v2)
        self.grafo[v2].add(v1)
    
    # Retorna a chave
    def get_no(self):
        return set(self.grafo.keys())

#Classe que contem os algoritmos de Bron-Kerbosch e o coeficiente médio de aglomeração do grafo
class Algoritmos:    
    #Seguindo o pseudocodigo disponibilizado na aula 5
    #Bron-Kerbosch sem pivotamento
    def bk_sp(grafo, P, R, X):
        if ((len(P) == 0) or (P is None)) and (len(X) == 0):                  
            print(str(len(R)) + " vértices: ", sorted(list(R)))
            return 1

        cliques = 0

        for i in P:
            cliques += Algoritmos.bk_sp(grafo, P.intersection(grafo[i]), R.union({i}), X.intersection(grafo[i]))
            P = P.difference({i})
            X = X.union({i})
        
        return cliques #retorna a quantidade de cliques maximais achados no algoritmo

    #Seguindo o pseudocodigo disponibilizado na aula 5
    #Bron-Kerbosch com pivotamento
    def bk_cp(grafo, P, R, X):
        if ((len(P) == 0) or (P is None)) and (len(X) == 0):                  
            print(str(len(R)) + " vértices: ", sorted(list(R)))
            return 1

        #Escolha do pivo
        max = 0
        for v in P.union(X):
            max = len(grafo[v])
            pivo = v
        
        cliques = 0

        for i in P.difference(grafo[pivo]):
            cliques += Algoritmos.bk_sp(grafo, P.intersection(grafo[i]), R.union({i}), X.intersection(grafo[i]))
            P = P.difference({i})
            X = X.union({i})
        
        return cliques #retorna a quantidade de cliques maximais achados no algoritmo

    
    #Calculo do coeficiente de aglomeração de cada nó
    #Fórmula dada de acordo com o slide da aula 5
    def coeficiente_aglomeracao(grafo, no):
        k = len(grafo[no])

        #Necessário para não ocorrer divisão por 0 no coeficiente
        if k <= 1:
            return 0
        
        comum = 0

        for adj in grafo[no]:
            comum += len(grafo[adj].intersection(grafo[no]))
        
        n = comum/2

        return (2*n)/(k*(k-1))

    #Calculo do coeficiente médio de aglomeração do grafo
    #Fórmula de acordo com o slide da aula 5
    def coeficiente_medio(grafo):
        coeficiente = 0

        for no in grafo.keys():
            valor = Algoritmos.coeficiente_aglomeracao(grafo, no)
            coeficiente += valor
        
        return coeficiente/len(grafo.keys())

#-----------------Main
arquivo = open('teste.txt')

#Leitura das linhas do arquivo
with arquivo as arq:
    conteudo = arq.readlines()

#Transformação da leitura em uma lista de lista
conteudo = [linha for linha in conteudo if linha[0] != "%"] 
conteudo = conteudo[1:]

conteudo = [linha.strip("\n") for linha in conteudo]
conteudo = [linha.split(" ")for linha in conteudo]

g = Grafo() #Cria o grafo 

# Insere os vertices de acordo com a lista de adj lida no arquivo
for v in conteudo:
    g.adiciona_aresta(int(v[0]), int(v[1]))

clique_sp = Algoritmos.bk_sp(g.grafo, g.get_no(), set(), set())
print("\n" + str(clique_sp) + " cliques maximais encontrador pelo algoritmo de Bron-Kerbosch sem pivotamento.")
print("---------------------------------------------------------------------------------------")
clique_cp = Algoritmos.bk_cp(g.grafo, g.get_no(), set(), set())
print("\n" + str(clique_cp) + " cliques maximais encontrador pelo algoritmo de Bron-Kerbosch com pivotamento.")
print("---------------------------------------------------------------------------------------")
coeficiente_medio = Algoritmos.coeficiente_medio(g.grafo)
print("Coeficiente médio de aglomeração do grafo: {0:.10}".format(coeficiente_medio))
print("---------------------------------------------------------------------------------------")