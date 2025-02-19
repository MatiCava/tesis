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
        if node in P:
            shared[node.id] = node
            current_solution.append(node)
        if node in D:
            del shared[node.id]
            # Si shared esta vacia, significa que podemos partir la solucion en este punto
            # Lo que sigue en la solucion seria parte de otro subgrafo, ya que no hay items compartidos
            if not shared:
                current_solution.append(node)
                solutions.append(current_solution) # Lista de listas
                current_solution = []
    return solutions

def generate_3opt_variation(S, change_1, change_2, change_3):
    print("current_S ", S)
    print("change_1 ", change_1)
    print("change_1[0] ", change_1[0])
    print("change_1[-1] ", change_1[-1])
    print("change_2 ", change_2)
    print("change_2[0] ", change_2[0])
    print("change_2[-1] ", change_2[-1])
    print("change_3 ", change_3) 
    print("change_3[0] ", change_3[0])
    print("change_3[-1] ", change_3[-1])
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

def three_opt_permutations(lst):
    n = len(lst)
    results = set()
    results_list = []
    
    for i, j, k in combinations(range(n), 3):
        
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
    possible_changes = create_list_subsolutions(P, D, S, Or, Dest)

    all_permutations = three_opt_permutations(possible_changes)
    while current_percentage < break_percentage and max_intentos > 0:
        for perm in all_permutations:
            new_cost = calculate_cost(perm, travel_costs)
            S = perm
            difference = original_cost - new_cost
            current_percentage = (100 * difference) / original_cost
            max_intentos -= 1
    return new_cost, S
