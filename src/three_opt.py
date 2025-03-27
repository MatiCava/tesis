from node import Node
from utils import calculate_cost
from itertools import combinations, permutations

# Solucion sin crear el grafo, reduciendo el costo

# La intencion de esta funcion es partir la solucion en distintas listas, que en el fondo representan la misma idea de encontrar subgrafos aislados.
# O(n) donde n es el largo de la solucion (2 * cantidad de items)

# S solucion valida
def create_list_subsolutions(S):
    # Lista de elementos que estan actualmente en el auto
    shared = {}
    # Solucion actual
    current_solution = []
    # Lista de listas, donde cada una representa un subgrafo aislado de la solucion
    solutions = []
    # No utilizamos deposito ni destino final
    for i in range(1, len(S) - 1):
        node = S[i]
        current_solution.append(node)
        if node.node_type == "pickup":
            shared[node.item_id] = node
        if node.node_type == "delivery":
            del shared[node.item_id]
            # Si shared esta vacia, significa que podemos partir la solucion en este punto
            # Lo que sigue en la solucion seria parte de otro subgrafo, ya que no hay items compartidos
            if not shared:
                solutions.append(current_solution) # Lista de listas
                current_solution = []
    return [[S[0]]] + solutions + [[S[-1]]]

def rearrange_solution(S, combs, perms):
    new_s = []
    for i in range(0, len(S)):
        if(i in combs):
            # Tengo que poner lo que diga perms
            sublist = S[perms[combs.index(i)]]
            new_s.append(sublist)
        else:
            new_s.append(S[i])
    return [node for sublist in new_s for node in sublist]

def subtract_edges(lst, original_cost, values, travel_costs):
    edges = set()
    total = original_cost

    for i in values:

        if((i, i-1) not in edges and (i-1, i) not in edges):
            edges.add((i, i-1))
            edges.add((i-1, i))
            total -= travel_costs[lst[i-1][-1].id][lst[i][0].id]

        if((i, i+1) not in edges and (i+1, i) not in edges):
            edges.add((i, i+1))
            edges.add((i+1, i))

            total -= travel_costs[lst[i][-1].id][lst[i+1][0].id]

    return total

def add_edges(lst, original_cost, combs, perms, travel_costs):
    edges = set()
    total = original_cost

    for i in range(0, 3):
        a = combs[i]
        b = perms[i]

        # Arista de atras hacia nuestro nodo
        if((a-1) not in combs):
            if((a - 1, b) not in edges and (b, a - 1) not in edges):
                edges.add((a - 1, b))
                edges.add((b, a - 1))

                total += travel_costs[lst[a - 1][-1].id][lst[b][0].id]
        else:
            c = perms[combs.index(a - 1)]

            if((b, c) not in edges and (c, b) not in edges):
                edges.add((b, c))
                edges.add((c, b))

                total += travel_costs[lst[c][-1].id][lst[b][0].id]

        # Arista de nuestro nodo hacia adelante
        if((a+1) not in combs):
            if((a + 1, b) not in edges and (b, a + 1) not in edges):
                edges.add((a + 1, b))
                edges.add((b, a + 1))

                total += travel_costs[lst[b][-1].id][lst[a + 1][0].id]
        else:
            c = perms[combs.index(a + 1)]

            if((b, c) not in edges and (c, b) not in edges):
                edges.add((b, c))
                edges.add((c, b))

                total += travel_costs[lst[b][-1].id][lst[c][0].id]
    
    return total


def three_opt_permutations(lst, original_cost, travel_costs):
    size = len(lst)
    best_result = original_cost
    perms = ()
    combs = ()

    # Hacemos este rango para evitar mover el origen y el final
    for i, j, k in combinations(range(1, size - 1), 3):

        # Se resta el costo de las aristas que eliminamos
        current_cost = subtract_edges(lst, original_cost, [i, j, k], travel_costs)

        for l, m, n in set(permutations([i, j, k])):
            
            # Se suma el costo de las nuevas aristas
            new_cost = add_edges(lst, current_cost, [i, j, k], [l, m, n], travel_costs)

            if(new_cost < best_result):
                best_result = new_cost
                combs = (i, j, k)
                perms = (l, m, n)

    return best_result, combs, perms

# Que reciba el costo por parametro y eliminar linea 153
def three_opt(S, initial_cost, travel_costs):
    
    # Inicilizamos el costo original de la solucion con la que arrancamos
    current_sol = S
    current_cost = initial_cost
    iterations = 0
    result_iteration = [initial_cost]
    list_iterations = [0]

    while True:
        possible_changes = create_list_subsolutions(current_sol)
        new_cost, combs, perms = three_opt_permutations(possible_changes, current_cost, travel_costs)

        if new_cost >= current_cost:
            break
        
        current_cost = new_cost
        current_sol = rearrange_solution(possible_changes, combs, perms)
        iterations += 1
        list_iterations.append(iterations)
        result_iteration.append(current_cost)

    return current_cost, current_sol, list_iterations, result_iteration