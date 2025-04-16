import json
import math
import time
from backtracking import backtracking
from swap_local_search import swap_local_search
from vns import VNS
from utils import calculate_cost, generate_graphic_results_compare_percentage, generate_initial_solution, generate_routes_json, generate_graphic_results_compare, generate_table_results, generate_vns_combined_graphic, generate_vns_combined_graphic_results, generate_vns_combined_graphic_results_compare_percentage, is_feasible_solution, save_result_iterations, save_result_iterations_vns
from three_opt import three_opt

def main():
    routes_json = generate_routes_json()
    total_execution_time = 0
    results = {}
    results_csv = []
    for route in routes_json:
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S = generate_initial_solution(input)
        initial_cost = calculate_cost(initial_S, input["travel_costs"])
        effort = (len(initial_S) / 4)  * 0.4
        cost, sol, list_iterations, result_iteration = three_opt(initial_S, initial_cost, input["travel_costs"], effort)
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        #is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
        inc = route.split("_")[1].split(".json")[0]
        print("Instancia ejecutada: ", route)
        partial_route = route.split("Instances")[1].split("/den")[0]
        if partial_route not in results.keys():
            if results.keys():
                generate_graphic_results_compare(results, "3-opt")
                generate_graphic_results_compare_percentage(results, "3-opt")
            results = {}
            results[partial_route] = [[list_iterations, result_iteration, cost, initial_cost, route]]
        else:
            results[partial_route].append([list_iterations, result_iteration, cost, initial_cost, route])
        
        # print("Costo final: ", cost)
        #print("Es una solucion correcta? ", is_correct_sol)
        # generate_graphic_results(list_iterations, result_iteration, route, "3_opt_local_search")
        # print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
        result_csv_all_iterations = save_result_iterations(list_iterations, result_iteration, route)
        results_csv.extend(result_csv_all_iterations)
    generate_table_results(results_csv, "3_opt")
    print("Tiempo total de ejecucion: ", total_execution_time)


def main_2():
    routes_json = generate_routes_json()
    total_execution_time = 0
    results = {}
    results_csv = []
    for route in routes_json:
        # list_iterations = []
        # result_iteration = []
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S = generate_initial_solution(input)
        initial_cost = calculate_cost(initial_S, input["travel_costs"])
        effort = (len(initial_S) / 4)  * 0.6
        cost, sol, list_iterations, result_iteration = swap_local_search(initial_S, initial_cost, input["travel_costs"], input["incompatibilities"], effort)
        #is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        print("Instancia ejecutada: ", route)
        partial_route = route.split("Instances")[1].split("/den")[0]
        if partial_route not in results.keys():
            if results.keys():
                generate_graphic_results_compare(results, "swap")
                generate_graphic_results_compare_percentage(results, "swap")
            results = {}
            results[partial_route] = [[list_iterations, result_iteration, cost, initial_cost, route]]
        else:
            results[partial_route].append([list_iterations, result_iteration, cost, initial_cost, route])
        inc = route.split("_")[1].split(".json")[0]
        #print("Sol final: ", sol)
        print("Costo final: ", cost)
        #print("Es una solucion correcta? ", is_correct_sol)
        # generate_graphic_results(list_iterations, result_iteration, route, "swap_local_search")
        # print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
        result_csv_all_iterations = save_result_iterations(list_iterations, result_iteration, route)
        results_csv.extend(result_csv_all_iterations)
    generate_table_results(results_csv, "swap_local_search")
    print("Tiempo total de ejecucion: ", total_execution_time)

def main_3():
    routes_json = generate_routes_json()
    # route = routes_json[40]
    total_execution_time = 0
    results = {}
    results_csv = []
    for route in routes_json:
        instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S = generate_initial_solution(input)
        initial_cost = calculate_cost(initial_S, input["travel_costs"])
        vns_max_intentos = 500
        res_cost, res_sol, vns_iterations, iterations_swap, result_swap, iterations_3_opt, result_3_opt = VNS(initial_S, input["travel_costs"], input["incompatibilities"], vns_max_intentos)
        is_correct_sol = is_feasible_solution(res_sol, input["incompatibilities"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        partial_route = route.split("Instances")[1].split("/den")[0]
        inc = route.split("_")[1].split(".json")[0]
        if partial_route not in results.keys():
            # if results.keys():
                # generate_vns_combined_graphic_results(results)
                # generate_vns_combined_graphic_results_compare_percentage(results)
            results = {}
            results[partial_route] = [[iterations_swap, result_swap, iterations_3_opt, result_3_opt, res_cost, initial_cost, route]]
        else:
            results[partial_route].append([iterations_swap, result_swap, iterations_3_opt, result_3_opt, res_cost, initial_cost, route])
        
        # print("Sol final: ", res_sol)
        print("Costo final: ", res_cost)
        # print("Es una solucion correcta? ", is_correct_sol)
        # print("Tiempo de ejecucion: ", execution_time)
        # generate_vns_combined_graphic(iterations_swap, result_swap, iterations_3_opt, result_3_opt, route)
        print("--------------------")
        result_csv_all_iterations = save_result_iterations_vns(vns_iterations, iterations_swap, result_swap, iterations_3_opt, result_3_opt, route)
        results_csv.extend(result_csv_all_iterations)
    generate_table_results(results_csv, "vns")
    print("Tiempo total de ejecucion: ", total_execution_time)

def main_backtracking():
    all_filenames = generate_routes_json()
    for route in all_filenames:
    # route = '../Instances_Pablo/prob10a.a.00.json'
    # print("Instancia ejecutada: ", route)
        if "prob5" in route:
            with open(route, "r") as file:
                input = json.load(file)
            S = generate_initial_solution(input)

            initial_solution = [S[0], S[-1]]
            available_nodes = S[1:-1]


            start_time = time.time()

            best_sol, best_cost = backtracking(initial_solution, available_nodes, input["travel_costs"], input["incompatibilities"])    

            execution_time = time.time() - start_time
            print("Instancia ejecutada: ", route)
            print("Costo final: ", best_cost)
            print("")
            print("Solucion final: ", best_sol)
            print("")
            print("Solucion valida: ", is_feasible_solution(best_sol, input["incompatibilities"]))
            print("")
            print("Tiempo de ejecucion: ", execution_time)
            print("--------------------")
    
def main_vns():
    routes_json = generate_routes_json()

    start_time = time.time()

    for route in routes_json:

        with open(route, "r") as file:
            input = json.load(file)
        
        initial_S = generate_initial_solution(input)
        
        print("Instancia ejecutada: ", route)

        vns_max_intentos = 500
        res_cost, res_sol, vns_interations, swap_iterations, _, three_opt_iterations, _ = VNS(initial_S, input["travel_costs"], input["incompatibilities"], vns_max_intentos)

        #is_correct_sol = is_feasible_solution(res_sol, input["incompatibilities"])
        
        print("Costo final: ", res_cost)
        print("--------------------")
        #print("Solucion valida: ", is_feasible_solution(res_sol, input["incompatibilities"]))
        #print("Iteraciones de Swap: ", swap_iterations)
        #print("Iteraciones de 3-opt: ", three_opt_iterations)
        #print("Iteraciones de VNS: ", vns_interations)
    execution_time = time.time() - start_time

    print("Tiempo total de ejecucion: ", execution_time)


# main_backtracking()
# main_2()
# main()
main_3()
# main_vns()