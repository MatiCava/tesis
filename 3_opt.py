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
