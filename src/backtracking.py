from utils import calculate_cost, is_feasible_solution

def is_valid_partial_solution(S, incompatibilities):

    active_items = set()
    if S[0].node_type != "depot":
        return False

    for node in S[1:-1]:
        if node.node_type == "pickup":
            if any(incompatibilities[i - 1][node.item_id - 1] == 1 for i in active_items):
                return False
            active_items.add(node.item_id)
        else:
            if node.item_id not in active_items:
                return False
            active_items.remove(node.item_id)
    return True




def backtracking(current_solution, available_nodes, travel_costs, incompatibilities):

    if not available_nodes:
        return(current_solution, calculate_cost(current_solution, travel_costs))
    
    best_sol = None
    best_cost = float("inf")

    for node in available_nodes[:]:

        # Se agrega el nodo al final de la solucion pero antes del nodo final
        final = current_solution[-1]
        current_solution[-1] = node
        current_solution.append(final)


        if(is_valid_partial_solution(current_solution, incompatibilities)):
            available_nodes.remove(node)

            new_solution, new_cost = backtracking(current_solution, available_nodes, travel_costs, incompatibilities)

            if new_cost < best_cost:
                best_cost = new_cost
                best_sol = new_solution[:]

            available_nodes.append(node)

        current_solution.pop()
        current_solution[-1] = final
    
    return best_sol, best_cost



    '''
    #caso base
    next_nodes vacia
        devuelvo S

    #caso recursivo
    para cada nodo en next_nodes:
        lo agrego a la solucion
        
        si es valida la nueva solucion:
            lo saco de next_nodes
            llamo a la recursion
        sino:
            continue
    '''



