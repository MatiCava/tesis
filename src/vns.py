from utils import calculate_cost, max_iteration_swap, max_iteration_three_opt
from swap_local_search import swap_local_search
from three_opt import three_opt


def VNS(initial_S, travel_costs, incompatibilities, vns_max_intentos, swap_limit, three_limit):
    current_solution = initial_S
    current_cost = calculate_cost(current_solution, travel_costs)
    vns_iterations = 0
    check_iterations = 0
    all_iterations_swap = []
    all_results_iterations_swap = []
    all_iterations_3_opt = []
    all_results_iterations_3_opt = []
    solution_size = len(initial_S)
    while check_iterations < 2 and vns_max_intentos > 0:
        # Primera búsqueda local: Swap
        swap_cost, swap_solution, list_iterations_swap, result_iteration_swap = swap_local_search(current_solution, current_cost, travel_costs, incompatibilities, swap_limit)

        three_cost, three_solution, list_iterations_3_opt, result_iteration_3_opt = three_opt(swap_solution, swap_cost, travel_costs, max_iteration_three_opt(solution_size, method="linear"))

        vns_iterations += 1
        vns_max_intentos -= 1
        if swap_cost != three_cost or swap_cost < current_cost: 
            check_iterations = 0
        else:
            check_iterations += 1
        all_iterations_swap.append(list_iterations_swap)
        all_results_iterations_swap.append(result_iteration_swap)
        all_iterations_3_opt.append(list_iterations_3_opt)
        all_results_iterations_3_opt.append(result_iteration_3_opt)
        # Por transitividad es igual comparar con swap_cost o con current_cost
        if three_cost < current_cost:
            current_solution = three_solution
            current_cost = three_cost

    return current_cost, current_solution, vns_iterations, all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt