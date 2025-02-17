def local_search(route, graph, P, D, incompatibilities):
    best_route = route[:] #copia de route
    best_cost = calculate_route_cost(route, graph)
    new_route = route[:]
    new_cost = 0

    #quizas una condicion de corte?
    
    for i in range(1, len(route) - 1):  #excluye origen y destino
        current_node = route[i]
            
        if current_node in P:  #nodo de pickup
            swap_with = route[i - 1]
        elif current_node in D:  #nodo de delivery
            swap_with = route[i + 1]
            
        #checkeo incompatibilidades
        if swap_with not in incompatibilities.get(current_node, []):
            #swap y calcular costo
            new_route[i], new_route[route.index(swap_with)] = (
                new_route[route.index(swap_with)],
                new_route[i]
            )
            new_cost = calculate_route_cost(new_route, graph)
            
        #actualizar si mejora
        if new_cost != 0 and new_cost < best_cost:
            best_route = new_route[:]
            best_cost = new_cost

    return best_route, best_cost
