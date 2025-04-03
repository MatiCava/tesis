
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

from utils import generate_initial_solution, generate_routes_json
from vns import VNS

def plot_vns_iterations():
    all_filenames = generate_routes_json()

    vns_max_intentos = 500
    iteration_divisors = [2, 4, 6, 8, 10]
    all_results = []

    for route in all_filenames:
        
        with open(route, "r") as file:
            input = json.load(file)

        initial_S = generate_initial_solution(input)
        instance_size = len(initial_S)
        results = []

        for divisor in iteration_divisors:
            effort = instance_size / divisor
            res_cost, res_sol = VNS(initial_S, input["travel_costs"], input["incompatibilities"], vns_max_intentos, effort)

            results.append({"divisor": divisor, "cost": res_cost})

            instance_name = os.path.relpath(route, "../Instances").replace("\\", "/")
            all_results.append({
                "instance": instance_name,
                "divisor": divisor,
                "cost": res_cost
            })

        relative_path = os.path.relpath(route, "../Instances")  # ruta relativa después de "Instances"
        png_path = os.path.join("../Graphics/Instances/results_vns_interations_divisors", relative_path)
        output_path = png_path.replace(".json", ".png")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plot_vns_costs_bar(results, output_path)
    
    df = pd.DataFrame(all_results)
    df.to_csv("../Graphics/Instances/results_vns_interations_divisors/vns_iteration_results.csv", index=False)

def plot_vns_costs_bar(results, save_path):
    divisors = [int(r["divisor"]) for r in results]
    costs = [float(r["cost"]) for r in results]

    plt.figure(figsize=(8, 5))
    plt.bar(divisors, costs, width=0.5, color='skyblue', edgecolor='black')
    plt.xlabel("Divisor de esfuerzo")
    plt.ylabel("Costo de la solución")
    plt.title("Costo de VNS según el esfuerzo relativo")

    for i, cost in enumerate(costs):
        plt.text(divisors[i], cost + 1, f"{cost:.1f}", ha='center', va='bottom', fontsize=9)

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(save_path)
    plt.close()


plot_vns_iterations()



