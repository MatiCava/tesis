import json

# Solucion principal
# Creando el grafo que representa los items que viajan juntos en algun momento

# O(n^2) donde n es el largo de la solucion (2 * cantidad de items)
# P lista nodos de pickups
# D lista nodos de delivery
# S solucion
def create_cotravel_graph(P, D, S):
	# Creamos diccionario para guardar futuros nodos del grafo
	pairs = {}
	# Lista de elementos que estan actualmente en el auto
	shared = []
	n = len(P)
	for i in range(0, n):
		pairs[i] = (P(i),D(i))
		
	cotravel_graph = [[0] * n for _ in range(n)]
			
	for i in S:
		# Si i es un pickup lo agregamos a la lista de items que comparten el auto y marcamos en el grafo
		if i in P:
			shared.append(pairs[i])
			for j in shared:
				cotravel_graph[i][j] = 1
				cotravel_graph[j][i] = 1
		# Si i es un devlivery lo sacamos de la lista de items que comparten el auto
		if i in D:
			shared.remove(pairs[i])
			
	return cotravel_graph

def dfs(node, graph, visited, component):
    # Marca el nodo como visitado
    visited.add(node)
    component.append(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited, component)
			
def find_disconnected_subgraphs(graph):
    # Nodos ya visitados
    visited = set()  
    # Lista para guardar los subgrafos aislados
    subgraphs = []   
    
    for node in graph:
        if node not in visited:
            component = []  # Lista para almacenar el subgrafo actual
            dfs(node, graph, visited, component)
            subgraphs.append(component)
    
    return subgraphs
	
# ---------------------------------------------------------------------------------------------- #

# Solucion alternativa sin crear el grafo, reduciendo el costo

# La intencion de esta funcion es partir la solucion en distintas listas, que en el fondo representan la misma idea de encontrar subgrafos aislados.
# O(n) donde n es el largo de la solucion (2 * cantidad de items)

# P lista nodos de pickups
# D lista nodos de delivery
# S solucion valida
def create_list_subsolutions(P, D, S, Or, Dest):
    # Lista de elementos que estan actualmente en el auto
    shared = {}
    # Solucion actual
    current_solution = []
    # Lista de listas, donde cada una representa un subgrafo aislado de la solucion
    solutions = []
    for i in range(0, len(S)):
        node = S[i]
        node_index = P.index(node) if node in P else D.index(node)
        if node in P:
            shared[node_index] = node
            current_solution.append(node)
        if node in D:
            del shared[node_index]
            # Si shared esta vacia, significa que podemos partir la solucion en este punto
            # Lo que sigue en la solucion seria parte de otro subgrafo, ya que no hay items compartidos
            if not shared:
                current_solution.append(node)
                solutions.append(current_solution) # Lista de listas
                current_solution = []
    return solutions

def generate_3opt_variation(S, change_1, change_2, change_3):
    # Convertir los segmentos en indices para extraer los valores de S
    id_1 = S.index(change_1[0]), S.index(change_1[-1]) + 1
    id_2 = S.index(change_2[0]), S.index(change_2[-1]) + 1
    id_3 = S.index(change_3[0]), S.index(change_3[-1]) + 1

    # Extraer segmentos segun los indices encontrados
    part_1 = S[:id_1[0]]  # Desde el inicio hasta antes de change_1
    part_2 = S[id_1[0]:id_1[1]]  # change_1
    part_3 = S[id_2[0]:id_2[1]]  # change_2
    part_4 = S[id_3[0]:id_3[1]]  # change_3
    part_5 = S[id_3[1]:]  # Desde el final de change_3 hasta el final de S

    # Reorganizar en la nueva permutacion
    return part_1 + part_4 + part_3 + part_2 + part_5

def calculate_cost(S, input):
     return 100

def opt_3(P, D, S, Or, Dest, input, break_percentage, incompatibilities):
    # Inicilizamos el costo original de la solucion con la que arrancamos
    original_cost = calculate_cost(S, input)
    # Inicializamos la diferencia con la que vamos a ir checkeando hasta alcanzar el porcentaje de mejora buscado
    difference = original_cost - original_cost
    current_percentage = (100 * difference) / original_cost
    # Buscamos los posibles cambios dentro de la solucion con la que arrancamos
    possible_changes = create_list_subsolutions(P, D, S, Or, Dest)
    print("possible_changes ", possible_changes)
    # n = len(possible_changes)

    # while current_percentage < break_percentage:
    #     for i, change in enumerate(possible_changes):
    #         # Si existen dos posibles cambios hacia delante de donde nos encontramos realizamos una permutacion con ellos
    #         # En caso de no encontrar uno o ambos trabajamos con los primeros cambios posibles
    #         if i + 1 < n:
    #             if i + 2 < n:
    #                 new_solution = generate_3opt_variation(S, change, possible_changes[i + 1], possible_changes[i + 2])
    #             else:
    #                 new_solution = generate_3opt_variation(S, change, possible_changes[i + 1], possible_changes[i - 1])
    #         else:
    #             new_solution = generate_3opt_variation(S, change, possible_changes[i - 1], possible_changes[i - 2])

    #         # Calculamos nuevo costo utilizando la nueva solucion
    #         new_cost = calculate_cost(new_solution, input)
    #         S = new_solution
    #         # Calculamos nueva diferencia entre la solucion original con la que arrancamos y la actual
    #         difference = original_cost - new_cost
    #         # Calculamos nuevo porcentaje de mejora
    #         current_percentage = (100 * difference) / original_cost
            
    # return new_cost, S

def generate_initial_solution(input):
    S = []
    # for i in range(0, len(input["requests"])):
    #     entry = input["requests"][i]
    #     if not S:
    #         S.append([i, entry])
    #     else:
    #         check_add = True
    #         for request_added in S:
    #             check_add = check_add and input["incompatibilities"][i][request_added[0]] == 0
    #         if check_add:
    #             S.append([i, entry])
    for i in range(0, len(input["requests"])):
        entry = input["requests"][i]
        S.append(entry[0])
        S.append(entry[1])
    return S

def main():
    route_json = "Instances/5/prob5a/density_0.5.json"
    with open(route_json, "r") as file:
        input = json.load(file)
    initial_S = generate_initial_solution(input)
    #initial_S = input["requests"]
    print("initial_S ", initial_S)
    opt_3(input["pickup_nodes"], input["deliviries_nodes"], initial_S, input["depot"], input["final_destination"], input, 5, input["incompatibilities"])

main()
