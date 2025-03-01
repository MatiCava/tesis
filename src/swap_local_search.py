from utils import calculate_cost, rearrange_solution


def swap(S, travel_costs, incompatibilities):
    swaps = set()
    # Movemos cada nodo de la lista hacia cada posible posicion, evitando el deposito y el final.
    for node_pos in range(1, len(S) - 1):
        for moves in range(1, len(S) - 1):
            curr_node = S[node_pos]
            prev_pos = max(node_pos - moves, 1)
            prev_node =  S[prev_pos]
            next_pos = min(node_pos + moves, len(S) - 2)
            next_node =  S[next_pos]

            # Tanto los pickups como los deliveries se mueven hacia adelante o hacia atras.
            # La condicion de corte es encontrar su par correspondiente (el otro nodo para el mismo item) o encontrar otro item imcompatible.

            # [0, P1, D1, P3, P2, D2, D3, F]
            # [0, P1, D1, P3, P2, D3, D2, F]

            # Pickup hacia atras hasta encontrar un delivery incompatible
            # Pickup hacia adelante hasta encontrar su delivery
            # Delivery hacia adelante hasta encontrar un pickup incompatible
            # Delivery hacia atras hasta encontrar su pickup

            if(curr_node.node_type == "pickup"):
                # Generamos soluciones hacia atras
                if(prev_node.node_type == "delivery" and incompatibilities[curr_node.id - 1][prev_node.id - 1] == 0 
                   and (curr_node, prev_node) not in swaps and (prev_node, curr_node) not in swaps):
                    # Guardamos la tupla para no repetir la solucion
                    swaps.add((curr_node, prev_node))
                    swaps.add((prev_node, curr_node))

                    curr_node.prev = S[prev_pos - 1]
                    curr_node.next = S[prev_pos]

                    prev_node.prev = S[node_pos]
                    
                    S[prev_pos - 1].next = S[node_pos]

                    S[node_pos + 1].prev = S[node_pos - 1]
                    S[node_pos - 1].next = S[node_pos + 1]

                    yield 1, S

                    curr_node.prev = S[node_pos - 1]
                    curr_node.next = S[node_pos + 1]

                    prev_node.prev = S[prev_pos - 1]
                    
                    S[prev_pos - 1].next = S[prev_pos]

                    S[node_pos + 1].prev = S[node_pos]
                    S[node_pos - 1].next = S[node_pos]





                '''          
                # Generamos soluciones hacia adelante
                if(curr_node.id != next_node.id 
                   and (curr_node, next_node) not in swaps and (next_node, curr_node) not in swaps):
                    # Guardamos la tupla para no repetir la solucion
                    swaps.add((curr_node, next_node))
                    swaps.add((next_node, curr_node))

                    curr_node.prev.next = next_node
                    next_node.next.prev = curr_node
                    curr_node.next = next_node.next
                    next_node.next = curr_node
                    next_node.prev = curr_node.prev
                    curr_node.prev = next_node

                    yield 1, S

                    curr_node.next.prev = next_node
                    next_node.prev.next = curr_node
                    next_node.next = curr_node.next
                    curr_node.prev = next_node.prev
                    curr_node.next = next_node
                    next_node.prev = curr_node

            # En caso de que sea un delivery
            else:
                # Generamos soluciones hacia adelante
                if(next_node.node_type == "pickup" and incompatibilities[curr_node.id - 1][next_node.id - 1] == 0 
                   and (curr_node, next_node) not in swaps and (next_node, curr_node) not in swaps):
                    swaps.add((curr_node, next_node))
                    swaps.add((next_node, curr_node))
                    
                    curr_node.prev.next = next_node
                    next_node.next.prev = curr_node
                    next_node.prev = curr_node.prev
                    curr_node.prev = next_node
                    curr_node.next = next_node.next
                    next_node.next = curr_node

                    yield 1, S

                    curr_node.next.prev = next_node
                    next_node.prev.next = curr_node
                    curr_node.prev = next_node.prev
                    next_node.next = curr_node.next
                    next_node.prev = curr_node
                    curr_node.next = next_node

                # Generamos soluciones hacia atras
                if(curr_node.id != prev_node.id 
                   and (curr_node, prev_node) not in swaps and (prev_node, curr_node) not in swaps):
                    # Guardamos la tupla para no repetir la solucion
                    swaps.add((curr_node, prev_node))
                    swaps.add((prev_node, curr_node))

                    curr_node.next.prev = prev_node
                    prev_node.prev.next = curr_node
                    curr_node.prev = prev_node.prev
                    prev_node.next = curr_node.next
                    curr_node.next = prev_node
                    prev_node.prev = curr_node

                    yield 1, S

                    # [0, P1, D1, P3, P2, D2, D3, F]
                    # [0, P1, D1, P3, P2, D3, D2, F]
                    # Current: D3
                    # Prev: D2

                    curr_node.prev.next = prev_node
                    prev_node.next.prev = curr_node
                    curr_node.next = prev_node.next
                    prev_node.prev = curr_node.prev
                    prev_node.next = curr_node
                    curr_node.prev = prev_node
                 '''

def swap_local_search(S, travel_costs, incompatibilities):

    current_sol = S
    current_cost = calculate_cost(S, travel_costs)
    
    for _, sol in swap(S, travel_costs, incompatibilities):

        new_sol = rearrange_solution(sol)

        #print("Sol: ", new_sol)
        
        new_cost = calculate_cost(new_sol, travel_costs)

        if(new_cost < current_cost):
            current_cost = new_cost
            current_sol = new_sol

    # Reacomodamos la solucion


    return current_cost, current_sol
