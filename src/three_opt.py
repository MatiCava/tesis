from node import Node
from utils import calculate_cost
from itertools import combinations, permutations

# Solucion sin crear el grafo, reduciendo el costo

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
    # No utilizamos deposito ni destino final
    for i in range(1, len(S) - 1):
        node = S[i]
        current_solution.append(node)
        if node in P:
            shared[node.item_id] = node
        if node in D:
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
        if((i, i+1) not in edges and (i+1, i) not in edges):
            edges.add((i, i+1))
            edges.add((i+1, i))

            total -= travel_costs[lst[i][-1].id][lst[i+1][0].id]
            
        if((i, i-1) not in edges and (i-1, i) not in edges):
            edges.add((i, i-1))
            edges.add((i-1, i))
            total -= travel_costs[lst[i-1][-1].id][lst[i][0].id]
        
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
            c = combs.index(a - 1)
            if((a - 1, perms[c]) not in edges and (perms[c], a - 1) not in edges):
                edges.add((a - 1, perms[c]))
                edges.add((perms[c], a - 1))

                total += travel_costs[lst[perms[c]][-1].id][lst[b][0].id]

        # Arista de nuestro nodo hacia adelante
        if((a+1) not in combs):
            if((a + 1, b) not in edges and (b, a + 1) not in edges):
                edges.add((a + 1, b))
                edges.add((b, a + 1))

                total += travel_costs[lst[b][-1].id][lst[a + 1][0].id]
        else:
            c = combs.index(a + 1)
            if((a + 1, perms[c]) not in edges and (perms[c], a + 1) not in edges):
                edges.add((a + 1, perms[c]))
                edges.add((perms[c], a + 1))

                total += travel_costs[lst[b][-1].id][lst[perms[c]][0].id]
        
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

def opt_3(P, D, S, Or, Dest, travel_costs):
    
    # Inicilizamos el costo original de la solucion con la que arrancamos
    original_cost = calculate_cost(S, travel_costs)
    # Inicializamos la diferencia con la que vamos a ir checkeando hasta alcanzar el porcentaje de mejora buscado
    difference = original_cost - original_cost
    current_percentage = (100 * difference) / original_cost
    # Buscamos los posibles cambios dentro de la solucion con la que arrancamos

    possible_changes = create_list_subsolutions(P, D, S, Or, Dest)
    new_cost, combs, perms = three_opt_permutations(possible_changes, original_cost, travel_costs)

    new_s = rearrange_solution(possible_changes, combs, perms)

    return new_cost, new_s
