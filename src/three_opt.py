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
    
    for i, j, k in combinations(range(n), 3):
        
        original = (lst[i], lst[j], lst[k])
        original_tuples = tuple(map(tuple, original))
        print("original_tuples", original_tuples)
        if len(set(original_tuples)) > 1:  # Solo permutar si hay diferencias
            unique_perms = set(permutations(original_tuples))
            
            for perm in unique_perms:
                lst[i], lst[j], lst[k] = perm
                snapshot = tuple(tuple(x) for x in lst)
                results.add(snapshot)
                
            lst[i], lst[j], lst[k] = original
    
    for res in results:
        for tup in res:
            print("id ", tup[0].id)
            print("type ", tup[0].node_type)
            print("id ", tup[1].id)
            print("type ", tup[1].node_type)
        print("-------------")
        
    return results

def opt_3(P, D, S, Or, Dest, travel_costs, break_percentage, incompatibilities):
    # Inicilizamos el costo original de la solucion con la que arrancamos
    original_cost = calculate_cost(S, travel_costs)
    print("original_cost", original_cost)
    # Inicializamos la diferencia con la que vamos a ir checkeando hasta alcanzar el porcentaje de mejora buscado
    difference = original_cost - original_cost
    current_percentage = (100 * difference) / original_cost
    # Buscamos los posibles cambios dentro de la solucion con la que arrancamos
    possible_changes = create_list_subsolutions(P, D, S, Or, Dest)

    res = three_opt_permutations(possible_changes)
    return res
    # print("P ", P)
    # print("D ", D)
    # print("initial_solution ", S)
    # print("possible_changes ", possible_changes)
    # n = len(possible_changes)
    # while current_percentage < break_percentage:
    #     for i in range(0, n):
    #         change = possible_changes[i]
    #         print("i actual ", i)
    #         print("change ", change)
    #         # Si existen dos posibles cambios hacia delante de donde nos encontramos realizamos una permutacion con ellos
    #         # En caso de no encontrar uno o ambos trabajamos con los primeros cambios posibles
    #         if i + 1 < n:
    #             if i + 2 < n:
    #                 new_solution = generate_3opt_variation(S, change, possible_changes[i + 1], possible_changes[i + 2])
    #             else:
    #                 new_solution = generate_3opt_variation(S, change, possible_changes[i + 1], possible_changes[i - 1])
    #         else:
    #             new_solution = generate_3opt_variation(S, change, possible_changes[i - 1], possible_changes[i - 2])

    #         print("new_solution ", new_solution)
    #         # Calculamos nuevo costo utilizando la nueva solucion
    #         new_cost = calculate_cost(new_solution, travel_costs)
    #         S = new_solution
    #         # Calculamos nueva diferencia entre la solucion original con la que arrancamos y la actual
    #         difference = original_cost - new_cost
    #         # Calculamos nuevo porcentaje de mejora
    #         current_percentage = (100 * difference) / original_cost
            
    # print("res_solution ", S)
    # print("res_cost ", new_cost)
    # return new_cost, S
