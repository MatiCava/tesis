from utils import calculate_cost
from swap_local_search import swap_local_search
from three_opt import opt_3


def VNS(P, D, initial_S, travel_costs, Or, Dest, incompatibilities, break_percentage, three_opt_max_intentos, vns_max_intentos):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)

    for _ in range(vns_max_intentos):
        # Primera búsqueda local: Swap
        improved_cost, improved_solution = swap_local_search(current_solution, travel_costs, incompatibilities)

        # Segunda búsqueda local: 3 opt sobre la solución mejorada
        improved_cost, improved_solution = opt_3(P, D, improved_solution, Or, Dest, travel_costs, break_percentage, incompatibilities, three_opt_max_intentos)

        # Si alguna búsqueda mejoró la solución, actualizar
        if improved_cost < current_cost:
            current_cost, current_solution = improved_cost, improved_solution
        else: 
            if improved_solution == initial_S:
                break
    return current_cost, current_solution