from utils import calculate_cost
from swap_local_search import swap_local_search
from three_opt import three_opt


def VNS(initial_S, travel_costs, incompatibilities, vns_max_intentos):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)

    for _ in range(vns_max_intentos):
        # Primera búsqueda local: Swap
        swap_cost, swap_solution = swap_local_search(current_solution, current_cost, travel_costs, incompatibilities)

        three_cost, three_solution = three_opt(swap_solution, swap_cost, travel_costs)

        if swap_cost == three_cost:
            return three_cost, three_solution
        
        # Por transitividad es igual comparar con swap_cost o con current_cost
        if three_cost < swap_cost:
            current_solution = three_solution
            current_cost = three_cost

    return current_cost, current_solution