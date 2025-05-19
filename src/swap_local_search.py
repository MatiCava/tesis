import numpy as np
from utils import calculate_cost, is_feasible_solution

def rearrange_solution(S, pos_1, pos_2, incompatibilities):
    new_s = S
    if(pos_2 < pos_1):
        new_s = S[:pos_2] + [S[pos_1]] + S[pos_2 : pos_1] + S[pos_1 + 1:]
    elif(pos_2 > pos_1):
        new_s = S[:pos_1] + S[pos_1 + 1:pos_2] + [S[pos_2]] + [S[pos_1]] + S[pos_2 + 1:]

    return new_s

def swap(S, initial_cost, travel_costs, incompatibilities):

    solutions = set()

    # Movemos cada nodo de la lista hacia cada posible posicion, evitando el deposito y el final.
    # Tanto los pickups como los deliveries se mueven hacia adelante o hacia atras.
    # La condicion de corte es encontrar su par correspondiente (el otro nodo para el mismo item) o encontrar otro item imcompatible.

    # Pickup hacia atras hasta encontrar un delivery incompatible
    # Delivery hacia atras hasta encontrar su pickup
    # Generamos soluciones hacia atras
    for node_pos in range(1, len(S) - 1):
        for moves in range(1, node_pos):
            curr_node = S[node_pos]
            prev_pos = max(node_pos - moves, 1)
            prev_node =  S[prev_pos]

            if(curr_node.node_type == "pickup"):
                if(incompatibilities[curr_node.item_id - 1][prev_node.item_id - 1] == 1):
                    break
                else:
                    cost = initial_cost - \
                        travel_costs[S[prev_pos - 1].id][prev_node.id] - travel_costs[S[node_pos - 1].id][curr_node.id] - travel_costs[curr_node.id][S[node_pos + 1].id] + \
                        travel_costs[S[prev_pos - 1].id][curr_node.id] + travel_costs[curr_node.id][prev_node.id] + travel_costs[S[node_pos - 1].id][S[node_pos + 1].id]
                    
                    solutions.add((cost, node_pos, prev_pos))

            elif(curr_node.node_type == "delivery"):
                if(prev_node.item_id == curr_node.item_id):
                    break
                else:
                    cost = initial_cost - \
                        travel_costs[S[prev_pos - 1].id][prev_node.id] - travel_costs[S[node_pos - 1].id][curr_node.id] - travel_costs[curr_node.id][S[node_pos + 1].id] + \
                        travel_costs[S[prev_pos - 1].id][curr_node.id] + travel_costs[curr_node.id][prev_node.id] + travel_costs[S[node_pos - 1].id][S[node_pos + 1].id]
                    
                    solutions.add((cost, node_pos, prev_pos))


    # Pickup hacia adelante hasta encontrar su delivery
    # Delivery hacia adelante hasta encontrar un pickup incompatible
    # Generamos soluciones hacia adelante
    for node_pos in range(1, len(S) - 1):
        for next_pos in range(node_pos + 1, len(S) - 1):
            curr_node = S[node_pos]
            next_node =  S[next_pos]


            if(curr_node.node_type == "pickup"):
                if(next_node.item_id == curr_node.item_id):
                    break
                else:
                    cost = initial_cost - \
                        travel_costs[S[node_pos - 1].id][curr_node.id] - travel_costs[curr_node.id][S[node_pos + 1].id] - travel_costs[next_node.id][S[next_pos + 1].id] + \
                        travel_costs[S[node_pos - 1].id][S[node_pos + 1].id] + travel_costs[next_node.id][curr_node.id] + travel_costs[curr_node.id][S[next_pos + 1].id]
                    
                    solutions.add((cost, node_pos, next_pos))

            elif(curr_node.node_type == "delivery"):
                if(incompatibilities[curr_node.item_id - 1][next_node.item_id - 1] == 1):
                    break
                else:
                    cost = initial_cost - \
                        travel_costs[S[node_pos - 1].id][curr_node.id] - travel_costs[curr_node.id][S[node_pos + 1].id] - travel_costs[next_node.id][S[next_pos + 1].id] + \
                        travel_costs[S[node_pos - 1].id][S[node_pos + 1].id] + travel_costs[next_node.id][curr_node.id] + travel_costs[curr_node.id][S[next_pos + 1].id]
                    
                    solutions.add((cost, node_pos, next_pos))

    return solutions

def swap_local_search(S, initial_cost, travel_costs, incompatibilities, max_iteraions):

    current_cost = initial_cost
    pos_1, pos_2 = 0, 0
    current_sol = S
    iterations = 0
    result_iteration = [initial_cost]
    list_iterations = [0]

    update_sol = True

    while True and update_sol:        
    # while max_iteraions > 0 and update_sol:
        update_sol = False
        solutions = swap(current_sol, current_cost, travel_costs, incompatibilities)
        for cost, a, b in solutions: 
            if(cost < current_cost):
                current_cost = cost
                pos_1, pos_2 = a, b
                update_sol = True

        if update_sol:
            current_sol = rearrange_solution(current_sol, pos_1, pos_2, incompatibilities)

        iterations += 1
        list_iterations.append(iterations)
        result_iteration.append(current_cost)
            
        max_iteraions -= 1

    return current_cost, current_sol, list_iterations, result_iteration