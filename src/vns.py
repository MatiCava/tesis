from utils import calculate_cost
from swap_local_search import swap_local_search, swap_local_search_2
from three_opt import opt_3, opt_3_2


def VNS(initial_S, travel_costs, incompatibilities, vns_max_intentos):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)

    for _ in range(vns_max_intentos):
        # Primera búsqueda local: Swap
        swap_cost, swap_solution = swap_local_search_2(current_solution, travel_costs, incompatibilities)

        three_cost, three_solution = opt_3_2(swap_solution, travel_costs)

        if swap_cost == three_cost:
            return three_cost, three_solution
        
        # Por transitividad es igual comparar con swap_cost o con current_cost
        if three_cost < swap_cost:
            current_solution = three_solution
            current_cost = three_cost

    return current_cost, current_solution