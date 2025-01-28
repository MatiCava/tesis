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
def create_list_subsolutions(P, D, S):
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
            if shared is empty and next(S): # next(S) es para verificar que todavia no terminamos de recorrer la solucion
                solutions.append(current_solution) # Lista de listas
                current_solution = []
    
    return solutions
