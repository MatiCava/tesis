from utils import calculate_cost, rearrange_solution


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
                elif(prev_node.node_type == "delivery"):
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

def swap_local_search(S, travel_costs, incompatibilities):

    current_cost = calculate_cost(S, travel_costs)
    pos_1, pos_2 = 0, 0
    
    solutions = swap(S, current_cost, travel_costs, incompatibilities)

    for cost, a, b in solutions:

        #new_s = rearrange_solution(S, a, b, incompatibilities)
        #new_c = calculate_cost(new_s, travel_costs)

        if(cost < current_cost):
            current_cost = cost
            pos_1, pos_2 = a, b

    return current_cost, rearrange_solution(S, pos_1, pos_2, incompatibilities)
