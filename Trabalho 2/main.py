# Aluna Ana Caroline da Rocha Braz // Matricula: 212008482

# Para esse trabalho foi utilizado o algoritmo de Gale-Shapley para que 
# fossem feito os emparelhamento estável máximos necessário. Além desse,
# também foi utilizado o artigo disponibilizado na especificação para
# retirada de dúvidas e ideia na construção do código, além dos slides 
# disponibilizados no aprender3 

# Para a compilação do código é necessário apenas que o arquivo de entrada 
# fique no mesmo diretório do código!


#################################################################################################################
#Funcao de abertura e leitura do arquivo
def leitura(file):
    with open(file) as f:
        lines = f.readlines()
    
    f.close()

    # Professores e escolas escolhidas 
    # P = professor
    # E = escola

    professor_lines = []
    escolas_lines = []
    for line in lines:
        if line[0:2] == '(P':
            professor_lines.append(line)
        elif line[0:2] == '(E':
            escolas_lines.append(line)

    #print(professor_lines)
    #print("---------------------------------")
    #print(escolas_lines)
    
    # Criação dos dicionário do professor
    professor = []

    for professor_line in professor_lines:
        professor_line = professor_line.replace('\n','').replace(' ','')
        
        id_professor = professor_line.split(":")[0]
        id_professor = id_professor.replace('(','').replace(')','')

        hab = id_professor.split(',')[1]   # habilidades
        id_professor = id_professor.split(',')[0] #número do prof
        
        professor_pref = professor_line.split(":")[1]        
        professor_pref = professor_pref.replace(')','').replace('(','').split(',')
        
        pref = []

        for p in professor_pref: #inverte a preferência deixando em ordem crescente 
            pref.insert(0,p)            

        professor.append([id_professor, hab, pref])              

    #professor = {p[0]: {"hab": int(p[1]), "pref": p[2]} for p in professor}
    #print(professor)
    # Criação do dicionário da escola
    escolas = []

    for escolas_line in escolas_lines:
        escolas_line = escolas_line.replace('\n','').replace(' ','')
             
        id_escola = escolas_line.replace('(','').replace(')','').replace(':',',').split(',')[0]
        #print(id_escola)

        escola_pref = escolas_line.replace('(','').replace(')','').replace(':',',').split(',')[1:3]
        #print(escola_pref)
        escolas.append([id_escola, escola_pref])

    #escolas = {e[0]:{"pref": e[1]} for e in escolas}
    #print(escolas)
        
    return professor, escolas
#################################################################################################################
#Função que encontra os emparelhamentos
def match(professor, escolas):
    matchings = []
    match = 0

    # Encontra o emparelhamento com a primeira opção de cada professor e comparando a habilidade
    # que a escola escolhida necessita e adiciona na lista de metchings
    for p in range(len(professor)):
        for e in range(len(escolas)):
            if professor[p][2][0] == escolas[e][0]:
                #print("entrei")
                escolas[e].append('0')
                if escolas[e][2] != '1':
                    for i in range(len(escolas[e][1])):
                        if professor[p][1] == escolas[e][1][i]:
                        #   print('entrei2')
                            matchings.append([professor[p][0],escolas[e][0]])
                            escolas[e].insert(2, '1')
                            match += 1
                            escolas[e][1].insert(0, '0')

    #print(professor)

    #Print dos matchings
    #for i in range(len(matchings)):
    #    print(matchings[i][0] + ' -->> ' + matchings[i][1])

    print("Quantidade de matchings encontrados: ")
    print(match)          

#################################################################################################################
#Main

file_txt = 'entradaProj2TAG.txt'
professor, escolas = leitura(file_txt)

mat = match(professor,escolas)

