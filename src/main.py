import json
import math
import time
from swap_local_search import swap_local_search
from vns import VNS
from utils import access_instances_pablo, generate_initial_solution, generate_routes_json, generate_table_results, is_feasible_solution
from three_opt import opt_3

def main():

    routes_json = generate_routes_json()
    total_execution_time = 0
    results = []
    for route in routes_json:
        print(route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S, P, D = generate_initial_solution(input)
        cost, sol = opt_3(P, D, initial_S, input["depot"], input["final_destination"], input["travel_costs"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        #is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
        route_inc = route.split("_")[1].split(".")
        instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", instance_name)
        if len(route_inc) > 2:
            print("%Inc: ", route_inc[1])
            inc = route_inc[1]
        else:
            print("%Inc: ", route_inc[0])
            inc = route_inc[0]
        print("Costo final: ", cost)
        #print("Es una solucion correcta? ", is_correct_sol)
        print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
        results.append({
            "Instancia": instance_name,
            "%Inc": inc,
            "Costo": cost,
            "Tiempo": execution_time
        })
    generate_table_results(results, "3_opt")
    print("Tiempo total de ejecucion: ", total_execution_time)


def main_2():
    routes_json = generate_routes_json()
    total_execution_time = 0
    results = []
    for route in routes_json:
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S, P, D = generate_initial_solution(input)
        cost, sol = swap_local_search(initial_S, input["travel_costs"], input["incompatibilities"])
        #is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        route_inc = route.split("_")[1].split(".")
        instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", instance_name)
        if len(route_inc) > 2:
            print("%Inc: ", route_inc[1])
            inc = route_inc[1]
        else:
            print("%Inc: ", route_inc[0])
            inc = route_inc[0]
        #print("Sol final: ", sol)
        print("Costo final: ", cost)
        #print("Es una solucion correcta? ", is_correct_sol)
        print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
        results.append({
            "Instancia": instance_name,
            "%Inc": inc,
            "Costo": cost,
            "Tiempo": execution_time
        })
    generate_table_results(results, "swap_local_search")
    print("Tiempo total de ejecucion: ", total_execution_time)

def main_3():
    routes_json = generate_routes_json()
    # route = routes_json[40]
    total_execution_time = 0
    results = []
    for route in routes_json:
        instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S, P, D = generate_initial_solution(input)
        vns_max_intentos = 100
        res_cost, res_sol = VNS(P, D, initial_S, input["travel_costs"], input["depot"], input["final_destination"], input["incompatibilities"], vns_max_intentos)
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
        print("--------------------")
        results.append({
            "Instancia": instance_name,
            "%Inc": inc,
            "Costo": res_cost,
            "Tiempo": execution_time
        })
    # generate_table_results(results, "vns")
    print("Tiempo total de ejecucion: ", total_execution_time)

def main_4():
    all_filenames = access_instances_pablo()
    # route = routes_json[40]
    total_execution_time = 0
    results = []
    for route in all_filenames:
        # instance_name = route.split("/")[3]
        print("Instancia ejecutada: ", route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        initial_S, P, D = generate_initial_solution(input)
        vns_max_intentos = 100
        res_cost, res_sol = VNS(P, D, initial_S, input["travel_costs"], input["depot"], input["final_destination"], input["incompatibilities"], vns_max_intentos)
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

        if not is_correct_sol:
            print("---------- SOLUCION INCORRECTA ----------")
        
        print("Tiempo de ejecucion: ", execution_time)
        print("--------------------")
        results.append({
            "Instancia": route,
            "%Inc": inc,
            "Costo": res_cost,
            "Tiempo": execution_time
        })
    # generate_table_results(results, "vns")
    print("Tiempo total de ejecucion: ", total_execution_time)

main_4()