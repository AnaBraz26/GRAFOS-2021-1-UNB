# Ana Caroline da Rocha Braz - 212008482
# Códigos e pseudo-códigos que serviram de base para o programa:
# https://www.tutorialspoint.com/M-Coloring-Problem
# https://www.geeksforgeeks.org/m-coloring-problem-backtracking-5/
# Além dos sites vários artigos foram pesquisados para tirar dúvidas sobre implementação
# http://ceur-ws.org/Vol-1754/EPoGames_2016_AC_paper_2.pdf (um dos artigos consultados)
# e os slides dados em sala de aula também foram consultados 
        

import math
import random

class SudokuBase:
    # Métodos básicos de um Sudoku:
    # Gerar um grafo vazio, preenchê-lo e imprimi-lo
    
    def __init__(self, base_size):
        self.base_size = base_size
        self.base_color = 0
        self.sudoku_graph = dict()
    
    #Sudoku em forma de matriz 9x9
    def get_pos(self, e, base): 
        quot = e//base
        rest = e%base

        if rest != 0:
            x = quot + 1
            y = rest
        else:
            x = quot
            y = base

        return x, y

    def get_blocks_cord(self, blocks_size):
        blocks = []

        # Um bloco é formado a cada n linhas e n colunas na matriz, onde n é a base do Sudoku
        for i in range(1, blocks_size+1):
            sup_lim_i = (blocks_size*i)+1
            inf_lim_i = sup_lim_i - blocks_size

            for j in range(1, blocks_size+1):
                sup_lim_j = (blocks_size*j)+1
                inf_lim_j = sup_lim_j - blocks_size

                blocks.append([list(range(inf_lim_i, sup_lim_i)), list(range(inf_lim_j, sup_lim_j))])

        return blocks

    def get_block(self, p, blocks, base):
        # Identifica em qual bloco uma célula está na matriz do Sudoku pelo seu índice
        p_x, p_y = self.get_pos(p, base)

        block_c = []

        for b in blocks:
            if (p_x in b[0]) and (p_y in b[1]):
                return b

    def same_blocks(self, a, b, blocks, base):
        return self.get_block(a, blocks, base) == self.get_block(b, blocks, base)

    def same_col(self, a, b, base):
        a_x, a_y = self.get_pos(a, base)
        b_x, b_y = self.get_pos(b, base)

        return a_y == b_y

    def same_row(self, a, b, base):
        a_x, a_y = self.get_pos(a, base)
        b_x, b_y = self.get_pos(b, base)

        return a_x == b_x
        
    def get_col_graph(self, graph):
        if "neighbors" in graph[list(graph.keys())[0]]:
            return {n: {"neighbors": graph[n]["neighbors"], "color": self.base_color} for n in graph.keys()}

        return {n: {"neighbors": graph[n], "color": self.base_color} for n in graph.keys()}
    
    def get_sudoku_redux(self, sudoku_graph):
        # Simplifica um grafo Sudoku, deixando apenas rótulo e cor preenchida
        return {v: sudoku_graph[v]["color"] for v in sudoku_graph.keys()}
        
    def update_col_graph(self):
        # Adiciona a chave "given" para distinguir células dadas de um Sudoku e células que podem ser preenchidas pelo usuário
        self.sudoku_graph = {n: {"neighbors": self.sudoku_graph[n]["neighbors"], "color": self.sudoku_graph[n]["color"], "given": self.sudoku_graph[n]["color"] != self.base_color} for n in self.sudoku_graph.keys()}
        
    def gen_empty_sudoku(self):
        # Gera um grafo Sudoku vazio dentro do próprio objeto da classe
        blocks_size = int(math.sqrt(self.base_size))
        nodes = list(range(1, (self.base_size**2)+1))
        graph = {v: set() for v in nodes}
        bls = self.get_blocks_cord(blocks_size)

        for a in graph.keys():
            for b in graph.keys():
                if (a != b) and (self.same_blocks(a, b, bls, self.base_size) or self.same_col(a, b, self.base_size) or self.same_row(a, b, self.base_size)):
                    graph[a].add(b)

        empty_graph = self.get_col_graph(graph)
        
        self.sudoku_graph = empty_graph
        self.update_col_graph()
        
    def get_empty_sudoku_graph(self):
        # Gera um grafo Sudoku vazio que é retornado como objeto pela função
        blocks_size = int(math.sqrt(self.base_size))
        nodes = list(range(1, (self.base_size**2)+1))
        graph = {v: set() for v in nodes}
        bls = self.get_blocks_cord(blocks_size)

        for a in graph.keys():
            for b in graph.keys():
                if (a != b) and (self.same_blocks(a, b, bls, self.base_size) or self.same_col(a, b, self.base_size) or self.same_row(a, b, self.base_size)):
                    graph[a].add(b)

        return graph
    
    def text_sudoku(self, sudoku_redux):
        text_sudoku = "-"*25 + "\n"

        for i in sudoku_redux.keys():
            lin_i, col_i = self.get_pos(i, 9)

            if col_i == 1:
                text_sudoku += "| "

            text_sudoku += str(sudoku_redux[i])

            # Se for o último elemento da linha, não precisa de espaço, mas de quebramento de linha
            if col_i%9 != 0:
                text_sudoku += " "
            else:
                text_sudoku += " |\n"

            # Imprimir a divisão de blocos nas colunas
            if (col_i%3 == 0) and (col_i != 9):
                text_sudoku += "| "

            # Imprimir a divisão de blocos nas linhas
            if (lin_i%3 == 0) and (col_i%9==0) and (lin_i%9!=0):
                text_sudoku += "-"*25
                text_sudoku += "\n"

        text_sudoku += "-"*25

        return text_sudoku
        
    def print_sudoku(self):
        redux_sudoku_n = self.get_sudoku_redux(self.sudoku_graph)
        text_print = self.text_sudoku(redux_sudoku_n)
        
        print(text_print)

    def fill_cell(self, index, val):
        # Se a célula foi dada, "given", usuário não pode alterá-la
        if self.sudoku_graph[index]["given"]:
            return False

        self.sudoku_graph[index]["color"] = val

        return True

class SudokuAlgorithms(SudokuBase):    
    def __init__(self, base_size):
        super().__init__(base_size)
        self.solutions = []

    def is_valid_color(self, col_graph, v, col):
        for n in col_graph[v]["neighbors"]:
            if col == col_graph[n]["color"]:
                return False

        return True

    def is_safe_v(self, col_graph, v, c):
        for n in col_graph[v]["neighbors"]:
            if c == col_graph[n]["color"]:
                return False

        return True
        
    def m_coloring_effic(self, col_graph, n, colors):
        # A diferença aqui é que na primeira solução encontrada a recursão é interrompida
        # Busca eficiente de uma solução, sem precisar fazer backtracking para todas cores possíveis
        if n == len(col_graph.keys())+1:
            self.sudoku_graph = col_graph
            return True

        random.shuffle(colors)
        for c in colors:
            if self.is_valid_color(col_graph, n, c):
                col_graph[n]["color"] = c

                if self.m_coloring_effic(col_graph, n+1, colors):
                    return True

                col_graph[n]["color"] = 0

        return False
        
    def erase_random_cell(self):
        cell_erase = random.randint(1, len(self.sudoku_graph.keys()))

        while self.sudoku_graph[cell_erase]["color"] == 0:
            cell_erase = random.randint(1, len(self.sudoku_graph.keys()))

        # Quando uma célula é apagada no grafo, a configuração dele muda, precisando ser atualizada
        self.sudoku_graph[cell_erase]["color"] = 0
        self.update_col_graph()
        self.solutions = []
        
    def graph_coloring_v(self, col_graph, n, colors, print_steps=False):
        if n == len(col_graph.keys())+1:
            self.solutions.append({v: col_graph[v]["color"] for v in col_graph.keys()})
            
            if (len(self.solutions) == 1) and print_steps:
                print("Solução encontrada.")

            return

        if not col_graph[n]["given"]:
            if (len(self.solutions) == 0) and print_steps:
                print("Verificando cores possíveis para " + str(n))
            
            for c in colors:
                if self.is_safe_v(col_graph, n, c):
                    
                    if (len(self.solutions) == 0) and print_steps:
                        print("Cor " + str(c) + " é possível para " + str(n))
                        
                    col_graph[n]["color"] = c

                    if (len(self.solutions) == 0) and print_steps:
                        print("Próximo vértice:")
                        
                    self.graph_coloring_v(col_graph, n+1, colors, print_steps)

                    # Na volta da recursão, apaga a cor para testar uma cor diferente e achar todas as combinações possíveis
                    col_graph[n]["color"] = 0
                else:
                    if (len(self.solutions) == 0) and print_steps:
                        print("Cor " + str(c) + " não é possível para " + str(n) + ". Próxima cor.")
        else:
            self.graph_coloring_v(col_graph, n+1, colors, print_steps)

class SudokuSolver(SudokuAlgorithms):
    # Métodos que usam os algoritmos do Sudoku para gerar Sudoku, gerar solução e resolver um Sudoku preenchido
    
    def __init__(self, base_size):
        super().__init__(base_size)
        
    def gen_random_solution(self):
        empty_graph = self.get_empty_sudoku_graph()
        colored_empty_graph = self.get_col_graph(self.sudoku_graph)
        
        available_colors = list(range(1, self.base_size+1))
        self.m_coloring_effic(colored_empty_graph, 1, available_colors)
        self.update_col_graph()
        
    def gen_random_sudoku(self):
        # Gera um Sudoku completo aleatoriamente
        
        available_colors = list(range(1, self.base_size+1))
        self.gen_random_solution()
        
        self.erase_random_cell()
        self.graph_coloring_v(self.sudoku_graph, 1, available_colors)
        
        while len(self.solutions) == 1:
            last_graph = {v: self.sudoku_graph[v]["color"] for v in self.sudoku_graph.keys()}
            self.erase_random_cell()
            self.graph_coloring_v(self.sudoku_graph, 1, available_colors)

        for i in last_graph.keys():
            self.sudoku_graph[i]["color"] = last_graph[i]
        
        self.update_col_graph()
        self.solutions = []
        
    def solve_sudoku(self, print_steps=False):
        available_colors = list(range(1, self.base_size+1))
        self.graph_coloring_v(self.sudoku_graph, 1, available_colors, print_steps)
        
        n_solution = self.solutions[0]
        for i in n_solution.keys():
            self.sudoku_graph[i]["color"] = n_solution[i]
    
        self.solutions = []
        
        self.update_col_graph()

class SudokuUser(SudokuSolver):
    # Métodos exclusivos de interação com usuário no programa
    
    def __init__(self, base_size):
        super().__init__(base_size)
        
    def fill_given_sudoku(self, given_sudoku):
        self.gen_empty_sudoku()

        for i in given_sudoku.keys():
            self.sudoku_graph[i]["color"] = given_sudoku[i]

        self.update_col_graph()
        
    def solution_checker(self):
        for v in self.sudoku_graph.keys():
            for n in self.sudoku_graph[v]["neighbors"]:
                if (self.sudoku_graph[v]["color"] == 0) or (self.sudoku_graph[v]["color"] == self.sudoku_graph[n]["color"]):
                    return False

class UserInterface:
    # Interface via terminal com usuário
    
    def __init__(self):
        self.user_on = True
        
    def main(self):
        while self.user_on:
            print("\n----------------SUDOKU EM CORES---------------\n")
            print("Neste trabalho será feito a apresentação de um sudoku gerado automaticamente")
            print("e solucionado pelo algoritmo de colocaração de grafos mostrando seu passo-a-passo")
            print("Escolha uma opção:")
            print()
            print("0 - Sair do programa")
            print("1 - Começar a solução passo-a-passo")
            print()
            print("Sua escolha: ", end="")

            user_in = input()
            user_in = int(user_in)

            if user_in == 0:
                self.user_on = False
            
            elif user_in == 1:
                self.main_sudoku_solver_detailed()

    #Solução Passo-a-Passo
    def main_sudoku_solver_detailed(self):        
        print("-------------------------------------------------------")
        print("Aqui será gerado um Sudoku aleatório e em sequência será mostrada o passo-a-passo da solução.")     
        print("Escolha uma opção:")
        print("")
        print("0 - Retornar")
        print("1 - Iniciar operação")
        print("")        
        print("Sua escolha: ", end="")

        user_in = input()
        user_in = int(user_in)

        if user_in == 0:
            return
        else:
            print("-------------------------------------------------------")
            print("Sudoku gerado:")           

            while True:

                gen_sudoku = SudokuUser(9)
                gen_sudoku.gen_empty_sudoku()
                gen_sudoku.gen_random_sudoku()
                gen_sudoku.print_sudoku()

                print("")
                print("Escolha uma opção:")
                print("")
                print("0 - Voltar para o menu")
                print("1 - Mostrar solução")
                print("2 - Gerar novo Sudoku")
                print()
                    
                print("Sua escolha: ", end="")
                user_in = input()

                if (user_in == "0") or (user_in == "1") or (user_in == "2"):
                    user_in = int(user_in)

                    if user_in == 0:
                        return

                    elif user_in == 1:
                        print("Passo-a-Passo:\n")
                        gen_sudoku.solve_sudoku(print_steps=True)

                        print("")
                        print("Solução Final:")
                        gen_sudoku.print_sudoku()

                        print("")
                        print("Voltando para o inicio....... ")
                                               
                        return

                    elif user_in == 2:
                        print("Novo jogo gerado:")
       
    
###########################################################################
# Principal - Inicio do jogo
game = UserInterface()
game.main()