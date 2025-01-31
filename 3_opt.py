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
# S solucion
def create_list_subsolutions(P, D, S, Or, Dest):
    # Lista de elementos que estan actualmente en el auto
    shared = []
    # Solucion actual
    current_solution = []
    # Lista de listas, donde cada una representa un subgrafo aislado de la solucion
    solutions = []

    for i in S:
        if i in P:
            shared.append(i)
        if i in D:
            shared.remove(i)
            # Si shared esta vacia, significa que podemos partir la solucion en este punto
            # Lo que sigue en la solucion seria parte de otro subgrafo, ya que no hay items compartidos
            if shared is [] and S[i + 1] != Dest:
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
    return part_1 + part_2 + part_3 + part_4 + part_5


def opt_3(P, D, S, Or, Dest, G, break_percentage):
    # Inicilizamos el costo original de la solucion con la que arrancamos
    original_cost = calculate_cost(S, G)
    # Inicializamos la diferencia con la que vamos a ir checkeando hasta alcanzar el porcentaje de mejora buscado
    difference = original_cost - original_cost
    current_percentage = (100 * difference) / original_cost
    # Buscamos los posibles cambios dentro de la solucion con la que arrancamos
    possible_changes = create_list_subsolutions(P, D, S, Or, Dest)
    n = len(possible_changes)
    
    while current_percentage < break_percentage:
        for i, change in enumerate(possible_changes):
            # Si existen dos posibles cambios hacia delante de donde nos encontramos realizamos una permutacion con ellos
            # En caso de no encontrar uno o ambos trabajamos con los primeros cambios posibles
            if i + 1 < n:
                if i + 2 < n:
                    new_solution = generate_3opt_variation(S, change, possible_changes[i + 1], possible_changes[i + 2])
                else:
                    new_solution = generate_3opt_variation(S, change, possible_changes[i + 1], possible_changes[i - 1])
            else:
                new_solution = generate_3opt_variation(S, change, possible_changes[i - 1], possible_changes[i - 2])

            # Calculamos nuevo costo utilizando la nueva solucion
            new_cost = calculate_cost(new_solution, G)
            S = new_solution
            # Calculamos nueva diferencia entre la solucion original con la que arrancamos y la actual
            difference = original_cost - new_cost
            # Calculamos nuevo porcentaje de mejora
            current_percentage = (100 * difference) / original_cost
            
    return new_cost, S
