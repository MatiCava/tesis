import json
import math
import time
from backtracking import backtracking
from swap_local_search import swap_local_search
from vns import VNS
from utils import calculate_cost, generate_graphic_results, generate_initial_solution, generate_routes_json, generate_table_results, generate_vns_combined_graphic_results, is_feasible_solution
from three_opt import three_opt

def main():
    routes_json = generate_routes_json()
    total_execution_time = 0
    for route in routes_json:
        print(route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S = generate_initial_solution(input)
        initial_cost = calculate_cost(initial_S, input["travel_costs"])
        cost, sol, list_iterations, result_iteration = three_opt(initial_S, initial_cost, input["travel_costs"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        #is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
        route_inc = route.split("_")[1].split(".")
        # instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", route)
        if len(route_inc) > 2:
            # print("%Inc: ", route_inc[1])
            inc = route_inc[1]
        else:
            # print("%Inc: ", route_inc[0])
            inc = route_inc[0]
        # print("Costo final: ", cost)
        #print("Es una solucion correcta? ", is_correct_sol)
        generate_graphic_results(list_iterations, result_iteration, route, "3_opt_local_search")
        # print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
    #     results.append({
    #         "Instancia": instance_name,
    #         "%Inc": inc,
    #         "Costo": cost,
    #         "Tiempo": execution_time
    #     })
    # generate_table_results(results, "3_opt")
    print("Tiempo total de ejecucion: ", total_execution_time)


def main_2():
    routes_json = generate_routes_json()
    total_execution_time = 0
    for route in routes_json:
        # list_iterations = []
        # result_iteration = []
        if "prob100a/a/density_0.25" in route:
            start_time = time.time()
            with open(route, "r") as file:
                input = json.load(file)
            initial_S = generate_initial_solution(input)
            initial_cost = calculate_cost(initial_S, input["travel_costs"])
            cost, sol, list_iterations, result_iteration = swap_local_search(initial_S, initial_cost, input["travel_costs"], input["incompatibilities"])
            #is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
            end_time = time.time()
            execution_time = end_time - start_time
            total_execution_time += execution_time
            route_inc = route.split("_")[1].split(".")
            # instance_name = route.split("/")[3]
            print("Instancia ejecutada: ", route)
            if len(route_inc) > 2:
                # print("%Inc: ", route_inc[1])
                inc = route_inc[1]
            else:
                # print("%Inc: ", route_inc[0])
                inc = route_inc[0]
            #print("Sol final: ", sol)
            # print("Costo final: ", cost)
            #print("Es una solucion correcta? ", is_correct_sol)
            generate_graphic_results(list_iterations, result_iteration, route, "swap_local_search")
            # print("Tiempo de ejecucion: ", execution_time)
            print("--------------------")
        #     results.append({
        #         "Instancia": instance_name,
        #         "%Inc": inc,
        #         "Costo": cost,
        #         "Tiempo": execution_time
        #     })
        # generate_table_results(results, "swap_local_search")
    print("Tiempo total de ejecucion: ", total_execution_time)

def main_3():
    routes_json = generate_routes_json()
    # route = routes_json[40]
    total_execution_time = 0
    for route in routes_json:
        instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S = generate_initial_solution(input)
        vns_max_intentos = 500
        effort = len(initial_S) / 4
        res_cost, res_sol, iterations_swap, result_swap, iterations_3_opt, result_3_opt = VNS(initial_S, input["travel_costs"], input["incompatibilities"], vns_max_intentos, effort)
        is_correct_sol = is_feasible_solution(res_sol, input["incompatibilities"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        route_inc = route.split("_")[1].split(".")
        
        if len(route_inc) > 2:
            #print("%Inc: ", route_inc[1])
            inc = route_inc[1]
        else:
            #print("%Inc: ", route_inc[0])
            inc = route_inc[0]
        print("Sol final: ", res_sol)
        print("Costo final: ", res_cost)
        print("Es una solucion correcta? ", is_correct_sol)
        print("Tiempo de ejecucion: ", execution_time)
        generate_vns_combined_graphic_results(iterations_swap, result_swap, iterations_3_opt, result_3_opt, route)
        print("--------------------")
        # results.append({
        #     "Instancia": instance_name,
        #     "%Inc": inc,
        #     "Costo": res_cost,
        #     "Tiempo": execution_time
        # })
    # generate_table_results(results, "vns")
    print("Tiempo total de ejecucion: ", total_execution_time)

def main_4():
    all_filenames = generate_routes_json()
    # route = routes_json[40]
    total_execution_time = 0
    results = []
    for route in all_filenames:

        # Esto es solo para ejecutar las primeras instancias
        # Con el objetivo de comparar con las que conocemos el optimo
        if("prob5" not in route or "a.00.json" not in route):
            continue

        # instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S = generate_initial_solution(input)
        vns_max_intentos = 10000
        effort = len(initial_S) / 4
        res_cost, res_sol = VNS(initial_S, input["travel_costs"], input["incompatibilities"], vns_max_intentos, effort)
        is_correct_sol = is_feasible_solution(res_sol, input["incompatibilities"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        route_inc = route.split("_")[1].split(".")
        
        if len(route_inc) > 2:
            #print("%Inc: ", route_inc[1])
            inc = route_inc[1]
        else:
            #print("%Inc: ", route_inc[0])
            inc = route_inc[0]
        # print("Sol final: ", res_sol)
        print("Costo final: ", res_cost)
        print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
        results.append({
            "Instancia": route,
            "%Inc": inc,
            "Costo": res_cost,
            "Tiempo": execution_time
        })

        break

    # generate_table_results(results, "vns")
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
    

# main_backtracking()
# main_2()
# main()
main_3()