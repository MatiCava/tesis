from utils import calculate_cost
from swap_local_search import swap_local_search
from three_opt import three_opt


def VNS(initial_S, travel_costs, incompatibilities, vns_max_intentos, iterations_per_round):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)
    corridas = 1
    check_iterations = 0
    all_iterations_swap = []
    all_results_iterations_swap = []
    all_iterations_3_opt = []
    all_results_iterations_3_opt = []
    while check_iterations < 3 and vns_max_intentos > 0:
        # Primera búsqueda local: Swap
        swap_cost, swap_solution, list_iterations_swap, result_iteration_swap = swap_local_search(current_solution, current_cost, travel_costs, incompatibilities, 0.6 * iterations_per_round)

        three_cost, three_solution, list_iterations_3_opt, result_iteration_3_opt = three_opt(swap_solution, swap_cost, travel_costs, 0.4 * iterations_per_round)

        corridas += 1
        vns_max_intentos -= 1
        if swap_cost == three_cost:
            check_iterations += 1
        else:
            check_iterations = 0
        all_iterations_swap.append(list_iterations_swap)
        all_results_iterations_swap.append(result_iteration_swap)
        all_iterations_3_opt.append(list_iterations_3_opt)
        all_results_iterations_3_opt.append(result_iteration_3_opt)
        # Por transitividad es igual comparar con swap_cost o con current_cost
        if three_cost < current_cost:
            current_solution = three_solution
            current_cost = three_cost

    return current_cost, current_solution, all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt