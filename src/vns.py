from utils import calculate_cost
from swap_local_search import swap_local_search, swap_local_search_2
from three_opt import opt_3, opt_3_2


def VNS(P, D, initial_S, travel_costs, Or, Dest, incompatibilities, vns_max_intentos):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)

    for _ in range(vns_max_intentos):
        # Primera búsqueda local: Swap
        swap_cost, swap_solution = swap_local_search_2(current_solution, travel_costs, incompatibilities)
        # print("SOL SWAP: ", improved_solution)
        # print("COST SWAP: ", improved_cost)
        # print("-----------------")
        # Segunda búsqueda local: 3 opt sobre la solución mejorada
        three_cost, three_solution = opt_3_2(P, D, swap_solution, Or, Dest, travel_costs)
        # print("SOL 3 OPT: ", improved_solution_3_opt)
        # print("COST 3 OPT: ", improved_cost)
        # print("-----------------")
        # Si alguna búsqueda mejoró la solución, actualizar

        if swap_cost == three_cost:
            return three_cost, three_solution
        
        # Por transitividad es igual comparar con swap_cost o con current_cost
        if three_cost < swap_cost:
            current_solution = three_solution
            current_cost = three_cost

    return current_cost, current_solution