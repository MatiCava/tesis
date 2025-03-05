import json
import math
import time
from swap_local_search import swap_local_search
from vns import VNS
from utils import generate_initial_solution, generate_routes_json, is_feasible_solution
from three_opt import opt_3

def main():

    routes_json = generate_routes_json()
    total_execution_time = 0
    for route in routes_json:
        print(route)
        start_time = time.time()
        with open(route, "r") as file:
            input = json.load(file)
        break_percentage = 15
        initial_S, P, D = generate_initial_solution(input)
        len_nodes = len(P) + 2
        max_intentos = math.ceil(break_percentage * (len_nodes * len_nodes) / 100)
        cost, sol = opt_3(P, D, initial_S, input["depot"], input["final_destination"], input["travel_costs"], break_percentage, input["incompatibilities"], max_intentos)
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        is_correct_sol = is_feasible_solution(sol, input["incompatibilities"])
        print("Costo: ", cost)
        print("Sol: ", sol)
        print("Es una solucion correcta? ", is_correct_sol)
        print("Tiempo de ejecucion: ", execution_time)
    print("Tiempo total de ejecucion: ", total_execution_time)


def main_2():
    route = generate_routes_json()[0]

    with open(route, "r") as file:
        input = json.load(file)

    initial_S, P, D = generate_initial_solution(input)

    sol = initial_S
    cost = -1

    for _ in range(10):
        cost, sol = swap_local_search(sol, input["travel_costs"], input["incompatibilities"])

    print("Sol final: ", sol)
    print("Costo final: ", cost)

def main_3():
    routes_json = generate_routes_json()
    total_execution_time = 0
    for route in routes_json:
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
        print("Sol final: ", res_sol)
        print("Costo final: ", res_cost)
        print("Es una solucion correcta? ", is_correct_sol)
        print("Tiempo de ejecucion: ", execution_time)
    print("Tiempo total de ejecucion: ", total_execution_time)

main_3()