import copy
import itertools
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

def three_opt_permutations_2(lst, original_cost, travel_costs):
    size = len(lst)
    
    # Hacemos este rango para evitar mover el origen y el final
    for i, j, k in combinations(range(1, size - 1), 3):
        original = (lst[i], lst[j], lst[k])
 
        # Se resta el costo de las aristas que eliminamos
        current_cost = original_cost - \
            travel_costs[lst[i-1][-1].id][lst[i][0].id] - travel_costs[lst[i][-1].id][lst[i+1][0].id] - \
            travel_costs[lst[j-1][-1].id][lst[j][0].id] - travel_costs[lst[j][-1].id][lst[j+1][0].id] - \
            travel_costs[lst[k-1][-1].id][lst[k][0].id] - travel_costs[lst[k][-1].id][lst[k+1][0].id]

        for l, m, n in set(permutations([i, j, k])):
            val_l, val_m, val_n = lst[l], lst[m], lst[n]
            lst[l], lst[m], lst[n] = original
            lst[i], lst[j], lst[k] = val_l, val_m, val_n
            
            # Se suma el costo de las nuevas aristas
            new_cost = current_cost + \
                travel_costs[lst[l-1][-1].id][lst[l][0].id] + travel_costs[lst[l][-1].id][lst[l+1][0].id] + \
                travel_costs[lst[m-1][-1].id][lst[m][0].id] + travel_costs[lst[m][-1].id][lst[m+1][0].id] + \
                travel_costs[lst[n-1][-1].id][lst[n][0].id] + travel_costs[lst[n][-1].id][lst[n+1][0].id]

            yield new_cost, lst

            lst[i], lst[j], lst[k] = original
            lst[l], lst[m], lst[n] = val_l, val_m, val_n


def three_opt_permutations(lst):
    n = len(lst)
    results = set()
    results_list = []
    
    # Hacemos este rango para evitar mover el origen y el final
    for i, j, k in combinations(range(1, n - 1), 3):
        original = (lst[i], lst[j], lst[k])
        original_tuples = tuple(map(tuple, original))
        if len(set(original_tuples)) > 1:  # Solo permutar si hay diferencias
            unique_perms = set(permutations(original_tuples))
            for perm in unique_perms:
                lst[i], lst[j], lst[k] = perm
                snapshot = tuple(tuple(x) for x in lst)
                results.add(snapshot)
                
            lst[i], lst[j], lst[k] = original

    for res in results:
        perm_list = []
        for tup in res:
            perm_list.append(tup[0])
            perm_list.append(tup[1])
        results_list.append(perm_list)
    
    return results_list

def opt_3(P, D, S, Or, Dest, travel_costs, break_percentage, incompatibilities, max_intentos):
    
    # Inicilizamos el costo original de la solucion con la que arrancamos
    original_cost = calculate_cost(S, travel_costs)
    # Inicializamos la diferencia con la que vamos a ir checkeando hasta alcanzar el porcentaje de mejora buscado
    difference = original_cost - original_cost
    current_percentage = (100 * difference) / original_cost
    # Buscamos los posibles cambios dentro de la solucion con la que arrancamos
    print("SOL RECIBIDA 3 OPT")
    print(S)
    print("-----------")
    possible_changes = create_list_subsolutions(P, D, S, Or, Dest)
    print("POSIBLES CMABIOS")
    print(possible_changes)
    print("-----------")
    new_cost = original_cost
    res_S = None
    print("OG COST")
    print(original_cost)
    print("-----------")
    while current_percentage < break_percentage and max_intentos > 0:
        for perm_cost, perm in three_opt_permutations_2(possible_changes, original_cost, travel_costs):
            max_intentos -= 1

            print("PERM COST y PERM")
            print("PERM: ", perm)
            print("Actual: ", res_S)
            print(perm_cost)
            print(new_cost)
            print(perm_cost < new_cost)
            print("-----------")
            if perm_cost < new_cost:
                new_cost = perm_cost
                res_S = copy.deepcopy(perm)
                difference = original_cost - new_cost
                current_percentage = (100 * difference) / original_cost
                if max_intentos == 0 or current_percentage > break_percentage:
                    break
    print("RES 3OPT ")
    print(res_S)
    return new_cost, res_S
