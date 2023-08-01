def projects_students_lists_from_file(file):
    # Lida com a leitura do arquivo .txt com os dados de estudantes e projetos
    with open(file) as f:
        lines = f.readlines()

    f.close()
    
    # Projetos e estudantes se diferenciam por P (de projeto) e A (de aluno)
    projects_lines = []
    students_lines = []

    for line in lines:
        if line[0:2] == '(P':
            projects_lines.append(line)
        elif line[0:2] == '(A':
            students_lines.append(line)

    # Para criar os dicionários de estudantes e projetos, é preciso extrair as informações dadas no arquivo
    projects = []

    for project_line in projects_lines:
        projects.append(project_line.replace('\n', '').replace('(', '').replace(')', '').replace(' ', '').split(','))

    projects = {p[0]: {"max_stud": int(p[1]), "min_grade": int(p[2])} for p in projects}

    students = []

    for student_line in students_lines:
        student_line = student_line.replace("\n", "").replace(" ", "")

        id_stud = student_line.split(":")[0]
        student_line = student_line.split(":")[1]

        id_stud = id_stud.replace("(", "").replace(")", "")

        grade_stud = student_line.split(")(")[1]
        student_line = student_line.split(")(")[0]

        grade_stud = grade_stud.replace(")", "")

        pref_stud = student_line.replace("(", "").replace(")", "").split(",")

        students.append([id_stud, pref_stud, grade_stud])

    students = {s[0]: {"pref_list": s[1], "grade": int(s[2])} for s in students}
    
    return projects, students

def index_lim_grade(students, st_list, s, p):
    # Retorna índice onde inserir um estudante dado na lista de um projeto, considerando sua nota e sua preferência
    gs = students[s]["grade"]
    ps = students[s]["pref_list"].index(p)
    
    for i in range(len(st_list)-1, -1, -1):
        gsi = students[st_list[i]]["grade"]
        psi = students[st_list[i]]["pref_list"].index(p)
        
        if gs == gsi:
            if ps >= psi:
                return i + 1
        elif gs < gsi:
            return i + 1
    
    return i

def insert_pref_projects(projects, students):
    # Elaboração da lista de preferência dos projetos
    projects_pref = dict()
    
    for p in projects.keys():
        projects_pref[p] = projects[p].copy()
        s_in_p = []
        
        for s in students.keys():
            if p in students[s]["pref_list"]:
                if len(s_in_p) == 0:
                    s_in_p.append(s)
                else:
                    i = index_lim_grade(students, s_in_p, s, p)
                    s_in_p.insert(i, s)
            
        projects_pref[p]["pref_list"] = s_in_p
    
    return projects_pref

def gale_shapley_algorithm_projects(projects, students):
    # O algoritmo aplicado dá prioridade aos projetos, cujas preferências já estão estabelecidas previamente
    # Os projetos preferem alunos com: maiores notas; e que os preferem mais
    
    matchings = []
    p_assigneds = []
    s_assigneds = []
    # Um dicionário é criado para armazenar a lista de estudantes já avaliados em cada projeto
    project_proposals = {p: [] for p in projects.keys()}
    
    print_loop = 0 # Única função dessa variável é controlar a impressão das 10 primeiras iterações do algoritmo

    # O laço do algoritmo é feito até não existir nenhum projeto vazio e com estudantes que não foram avaliados
    p_notassign_nonempty = [p for p in projects.keys() if (p not in p_assigneds) and len(project_proposals[p]) != len(projects[p]["pref_list"])]
    
    while len(p_notassign_nonempty) != 0:
        sub_print = 0 # Para fins de impressão de etapas
        p = p_notassign_nonempty[0]    
        s = [s for s in projects[p]["pref_list"] if s not in project_proposals[p]][0]

        limit_inscriptions_p = projects[p]['max_stud']
        min_grade_p = projects[p]['min_grade']

        # Se o estudante avaliado tiver nota menor que a mínima do projeto, ele é descartado
        if students[s]['grade'] >= min_grade_p:
            sub_print = 1
            if s not in s_assigneds:
                matchings.append([p, s])
                s_assigneds.append(s)
            else:
                s_act_project = [mat for mat in matchings if mat[1] == s][0][0]

                # Se estudante já está em algum projeto, inseri-lo no projeto atual caso prefira o atual
                if students[s]["pref_list"].index(p) < students[s]["pref_list"].index(s_act_project):
                    sub_print = 2
                    if s_act_project in p_assigneds:
                        p_assigneds.pop(p_assigneds.index(s_act_project))

                    matchings.pop(matchings.index([s_act_project, s]))
                    matchings.append([p, s])

                    s_assigneds.append(s)

            act_n_memb = len([mat for mat in matchings if mat[0] == p])
            # Se o projeto tiver alcançado seu número máximo de participantes, deixa de ser considerado livre
            if act_n_memb == limit_inscriptions_p:
                p_assigneds.append(p)

        project_proposals[p].append(s)
        p_notassign_nonempty = [p for p in projects.keys() if (p not in p_assigneds) and len(project_proposals[p]) != len(projects[p]["pref_list"])]
        
        if print_loop < 10:
            if sub_print != 2:
                s_act_project = None
            
            full_p = act_n_memb == limit_inscriptions_p
            all_checked_p = len(project_proposals[p]) == len(projects[p]["pref_list"])
            print_it_alg(print_loop, sub_print, p, s, full_p, all_checked_p, s_act_project)
            
            print_loop = print_loop + 1
    
    return matchings

def print_it_alg(i, sub, p, s, full_p=False, all_checked_p=False, p_ant_of_s=None):
    if i == 0:
        print("\n------10 primeiras iterações:------\n")
    
    if sub == 0:
        txt_loop = "{0}: {1}     X     {2} (par impossível)".format(i+1, p, s)
    elif sub == 1:
        txt_loop = "{0}: {1} --------> {2} (par formado)".format(i+1, p, s)
    else:
        txt_loop = "{0}: {1} ----/---> {2} (par desfeito)\n     {3} --------> {2} (par formado)".format(i+1, p_ant_of_s, s, p)

    if full_p:
        txt_loop += "\n_____________{0} cheio_____________\n".format(p)
    if all_checked_p:
        txt_loop += "\n_____________{0} checou todos inscritos_____________\n".format(p)

    print(txt_loop)

def order_matchings(mat):
    # Organiza os emparelhamentos feitos, que estavam em lista, para um dicionário, com cada projeto sendo uma chave
    
    matchings = dict()
    
    k_list = set([int(m[0].replace('P', '')) for m in mat])
    k_list = sorted(list(k_list))
    k_list = ['P' + str(k) for k in k_list]
    
    for k in k_list: 
        students = sorted([int(m[1].replace('A', '')) for m in mat if m[0] == k])
        students = ['A' + str(s) for s in students]
        matchings[k] = students
    
    return matchings

def remove_rem_projects(projects_mat, projects):
    # Remove do dicionário projetos que não tenham preenchido todas as vagas
    # Organiza as informações dos projetos descartados por falta de inscrições efetivadas
    
    rem_projects = dict()
    rem_projects_list = []
    
    rem_projects_list = [k for k in projects_mat.keys() if len(projects_mat[k]) < projects[k]["max_stud"]]
    rem_projects_list += [k for k in projects.keys() if k not in projects_mat.keys()]
            
    for r in rem_projects_list:
        if r in projects_mat.keys():
            rem_projects[r] = projects_mat[r]
            projects_mat.pop(r)
        else:
            rem_projects[r] = []
        
    return projects_mat, rem_projects

def print_header_matchings(mat, rem_mat):
    print("\n\n")
    print("----------Emparelhamento estável máximo obtido:----------")
    print("          Número de projetos viáveis: {0}".format(len(mat)))
    print("          Número de projetos descartados: {0}".format(len(rem_mat)))
    print("\n")

def print_matchings_p(mat, projects, full):
    if full:
        print(">-----Projetos viáveis, com todas vagas preenchidas:-----<\n\n")
    else:
        print(">--------Projetos descartados, com vagas sobrando:--------<\n")
    
    for p in mat.keys():
        ef_insc = len(mat[p])
        av_insc = projects[p]["max_stud"]

        txt_insc = "inscrições"
        txt_vag = "vagas"
        if ef_insc == 1:
            txt_insc = "inscrição"
        if av_insc == 1:
            txt_vag = "vaga"

        txt_full = "{0}: ---------> {1}\n    ({2} {3} X {4} {5})\n".format(p, str(mat[p]).replace("'", ""), ef_insc, txt_insc, av_insc, txt_vag)

        print(txt_full)

path_file_txt = "entradaProj2TAG2.txt"
projects, students = projects_students_lists_from_file(path_file_txt)
# As litas de preferências dos projetos são feitas de forma separada
projects = insert_pref_projects(projects, students)

mat = gale_shapley_algorithm_projects(projects, students)
mat = order_matchings(mat)
mat, rem_mat = remove_rem_projects(mat, projects)

# Impressão das informações sobre o emparelhamento estável encontrado
print_header_matchings(mat, rem_mat)
print_matchings_p(mat, projects, full=True)
print_matchings_p(rem_mat, projects, full=False)