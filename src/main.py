import json
from utils import generate_initial_solution, is_feasible_solution
from three_opt import opt_3
import itertools

def main():
    route_json = "../Instances/5/prob5a/density_0.5.json"
    with open(route_json, "r") as file:
        input = json.load(file)
    initial_S, P, D = generate_initial_solution(input)
    _, res = opt_3(P, D, initial_S, input["depot"], input["final_destination"], input["travel_costs"], 15, input["incompatibilities"])
    print(res)

main()