from utils import calculate_cost
from swap_local_search import swap_local_search, swap_local_search_2
from three_opt import opt_3, opt_3_2


def VNS(P, D, initial_S, travel_costs, Or, Dest, incompatibilities, vns_max_intentos):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)

    for _ in range(vns_max_intentos):
        # Primera búsqueda local: Swap
        improved_cost, improved_solution = swap_local_search_2(current_solution, travel_costs, incompatibilities)
        # print("SOL SWAP: ", improved_solution)
        # print("COST SWAP: ", improved_cost)
        # print("-----------------")
        # Segunda búsqueda local: 3 opt sobre la solución mejorada
        improved_cost, improved_solution_3_opt = opt_3_2(P, D, improved_solution, Or, Dest, travel_costs)
        # print("SOL 3 OPT: ", improved_solution_3_opt)
        # print("COST 3 OPT: ", improved_cost)
        # print("-----------------")
        # Si alguna búsqueda mejoró la solución, actualizar
        if improved_cost <= current_cost:
            current_cost, current_solution = improved_cost, improved_solution_3_opt 

        if improved_solution == improved_solution_3_opt:
            break     
            
    return current_cost, current_solution