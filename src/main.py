import json
import math
from utils import generate_initial_solution, is_feasible_solution
from three_opt import opt_3
import itertools

def main():
    route_json = "../Instances/5/prob5a/density_0.5.json"
    with open(route_json, "r") as file:
        input = json.load(file)
    break_percentage = 15
    initial_S, P, D = generate_initial_solution(input)
    len_nodes = len(P) + 2
    max_intentos = math.ceil(break_percentage * (len_nodes * len_nodes) / 100)
    _, res = opt_3(P, D, initial_S, input["depot"], input["final_destination"], input["travel_costs"], break_percentage, input["incompatibilities"], max_intentos)
    print(res)

main()