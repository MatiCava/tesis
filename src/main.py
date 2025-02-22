import json
import math
from utils import generate_initial_solution, is_feasible_solution
from three_opt import opt_3
import itertools

def main():
    instance_labels = ['a', 'b', 'c', 'd', 'e']
    densities = ["0.1", "0.5", "0.25", "0.75", "0"]
    folders = ["5", "10", "15", "20", "25", "30", "35"]
    routes_json = []
    for folder in folders:
        for label in instance_labels:
            for density in densities:
                label_test = "../Instances/"+ folder + "/prob" + folder + label + "/density_" + density + ".json"
                routes_json.append(label_test)
                
    for route in routes_json:
        with open(route, "r") as file:
            input = json.load(file)
        break_percentage = 15
        initial_S, P, D = generate_initial_solution(input)
        len_nodes = len(P) + 2
        max_intentos = math.ceil(break_percentage * (len_nodes * len_nodes) / 100)
        cost, sol = opt_3(P, D, initial_S, input["depot"], input["final_destination"], input["travel_costs"], break_percentage, input["incompatibilities"], max_intentos)
        print("Costo: ", cost)
        print("Sol: ", sol)

main()