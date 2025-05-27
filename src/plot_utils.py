
import json
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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

def save_result_iterations(list_iterations, result_iteration, execution_time, route):
    partial_route = route.split("Instances")[1].split("/den")[0]
    inc = route.split("_")[1].split(".json")[0]
    results_csv = []
    for i in range(len(list_iterations)):
        # results_csv.append({
        #                         "Instancia": partial_route,
        #                         "%Inc": inc,
        #                         "Numero iteracion": list_iterations[i],
        #                         "Costo de iteracion": result_iteration[i],
        #                         "Tiempo de iteracion": execution_time
        #                     })
        results_csv.append([partial_route, inc, list_iterations[i], result_iteration[i], execution_time])
    with open('../Results/results_3_opt_new_limited.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(results_csv)
    return results_csv

def save_result_iterations_vns(vns_iterations, iterations_swap, result_swap, iterations_3_opt, result_3_opt, execution_time, route):
    partial_route = route.split("Instances")[1].split("/den")[0]
    inc = route.split("_")[1].split(".json")[0]
    results_csv = []
    for i in range(vns_iterations):
        for j in range(len(iterations_swap[i])):
            # results_csv.append({
            #                         "Instancia": partial_route,
            #                         "%Inc": inc,
            #                         "Heuristica": "swap",
            #                         "Numero iteracion": iterations_swap[i][j],
            #                         "Costo de iteracion": result_swap[i][j],
            #                         "Tiempo de iteracion": execution_time
            #                     })
            results_csv.append([partial_route, inc, "swap", iterations_swap[i][j], result_swap[i][j], execution_time])
        for j in range(len(iterations_3_opt[i])):
            # results_csv.append({
            #                         "Instancia": partial_route,
            #                         "%Inc": inc,
            #                         "Heuristica": "3-opt",
            #                         "Numero iteracion": iterations_3_opt[i][j],
            #                         "Costo de iteracion": result_3_opt[i][j],
            #                         "Tiempo de iteracion": execution_time
            #                     })
            results_csv.append([partial_route, inc, "3-opt", iterations_3_opt[i][j], result_3_opt[i][j], execution_time])
    with open('../Results/results_vns_new_unlimited.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(results_csv)
    return results_csv

def generate_table_results(results, who):
    base_dir = "..\Results"
    os.makedirs(base_dir, exist_ok=True)
    df = pd.DataFrame(results)
    csv_path = os.path.join(base_dir, "results_" + who +"_without_limiter.csv")
    #csv_path = os.path.join(base_dir, "results_" + who+".csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

def generate_graphic_results_compare_percentage(results, who):
    partial_route =  list(results.keys())[0]
    color_map = {"0.1": "#0303ff", "0.5": "#fca105", "0.25": "#f51505", "0.75": "#bd05f5", "0":"#60f702"}
    marker_list = ['o', 's', 'p', 'X', 'D']
    for j in range(len(results[partial_route])):
        result = results[partial_route][j]
        all_iterations, all_results_iterations, final_cost, initial_cost, route = result[0], result[1], result[2], result[3], result[4]
        percetage_iterations = []
        inc = route.split("_")[1].split(".json")[0]
        for res_cost in all_results_iterations:
            percetage_cost = round(((res_cost - final_cost) / final_cost) * 100, 2)
            percetage_iterations.append(percetage_cost)
        plt.plot(all_iterations, percetage_iterations, color = color_map[inc], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')          

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    #output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who + "_combined_compare_%", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who + "_combined_compare_%_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel(f"% sobre la mejor solucion encontrada")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion de " + who + " local search")
    plt.yticks(range(0, round(percetage_iterations[0]), 10 if percetage_iterations[0] < 200 else 20))
    legend_elements = [
        Line2D([0], [0], color='#0303ff', lw=1.5, label=f"10% incompatibilidad"),
        Line2D([0], [0], color='#fca105', lw=1.5, label=f"50% incompatibilidad"),
        Line2D([0], [0], color='#f51505', lw=1.5, label=f"25% incompatibilidad"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=f"75% incompatibilidad"),
        Line2D([0], [0], color='#60f702', lw=1.5, label=f"0% incompatibilidad")
    ]
    plt.legend(handles=legend_elements, fontsize=6)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()

def generate_graphic_results_compare(results, who):
    partial_route =  list(results.keys())[0]
    color_map = {"0.1": "#0303ff", "0.5": "#fca105", "0.25": "#f51505", "0.75": "#bd05f5", "0":"#60f702"}
    marker_list = ['o', 's', 'p', 'X', 'D']
    for j in range(len(results[partial_route])):
        result = results[partial_route][j]
        all_iterations, all_results_iterations, final_cost, initial_cost, route = result[0], result[1], result[2], result[3], result[4]
        inc = route.split("_")[1].split(".json")[0]
        plt.plot(all_iterations, all_results_iterations, color = color_map[inc], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')          

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    #output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who + "_combined_compare", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who + "_combined_compare_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel("Valor de la solucion")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion de " + who + " local search")
    legend_elements = [
        Line2D([0], [0], color='#0303ff', lw=1.5, label=f"10% incompatibilidad"),
        Line2D([0], [0], color='#fca105', lw=1.5, label=f"50% incompatibilidad"),
        Line2D([0], [0], color='#f51505', lw=1.5, label=f"25% incompatibilidad"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=f"75% incompatibilidad"),
        Line2D([0], [0], color='#60f702', lw=1.5, label=f"0% incompatibilidad")
    ]
    plt.legend(handles=legend_elements, fontsize=6)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()

def generate_vns_combined_graphic(all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt, route):
    instance_folder = route.split(".json")[0].split("Instances")[1].split("/")
    file_name = instance_folder[4] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined", instance_folder[1], instance_folder[2], instance_folder[3])
    os.makedirs(output_folder, exist_ok=True)
    color_map = {"swap": "blue", "3-opt": "red"}
    aux_iterations = [0]
    aux_results = []
    heuristics = []
    for i in range(len(all_iterations_swap)):
        iterations_swap = all_iterations_swap[i]
        results_iterations_swap = all_results_iterations_swap[i]
        iterations_3_opt = all_iterations_3_opt[i]
        results_iterations_3_opt = all_results_iterations_3_opt[i]
        for n in range(aux_iterations[-1] + 1, aux_iterations[-1] + 1 + len(iterations_swap)):
            aux_iterations.append(n)
            heuristics.append("swap")
        for n in range(aux_iterations[-1] + 1, aux_iterations[-1] + 1 + len(iterations_3_opt)):
            aux_iterations.append(n)
            heuristics.append("3-opt")
        aux_results.extend(results_iterations_swap)
        aux_results.extend(results_iterations_3_opt)
    
    for i in range(len(aux_iterations) - 1):
        plt.plot(aux_iterations[i], aux_results[i], color = color_map[heuristics[i]], marker='o', linestyle='-')
    plt.ylabel("Valor de la solucion")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion del VNS con Swap y 3-Opt")
    legend_elements = [
        Line2D([0], [0], color='blue', lw=2, label="Swap Local Search"),
        Line2D([0], [0], color='red', lw=2, label="3-Opt Local Search")
    ]
    plt.legend(handles=legend_elements)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()

def generate_vns_combined_graphic_results(results):
    partial_route =  list(results.keys())[0]
    color_map = {"0.1": "#0303ff", "0.5": "#fca105", "0.25": "#f51505", "0.75": "#bd05f5", "0":"#60f702"}
    marker_list = ['o', 's', 'p', 'X', 'D']
    for j in range(len(results[partial_route])):
        result = results[partial_route][j]
        all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt, final_cost, intial_cost, route = result[0], result[1], result[2], result[3], result[4], result[5], result[6]
        inc = route.split("_")[1].split(".json")[0]
        aux_iterations = [0]
        aux_results = []
        heuristics = []
        for i in range(len(all_iterations_swap)):
            iterations_swap = all_iterations_swap[i]
            results_iterations_swap = all_results_iterations_swap[i]
            iterations_3_opt = all_iterations_3_opt[i]
            results_iterations_3_opt = all_results_iterations_3_opt[i]
            for n in range(aux_iterations[-1] + 1, aux_iterations[-1] + 1 + len(iterations_swap)):
                aux_iterations.append(n)
                heuristics.append("swap")
            for n in range(aux_iterations[-1] + 1, aux_iterations[-1] + 1 + len(iterations_3_opt)):
                aux_iterations.append(n)
                heuristics.append("3-opt")
            aux_results.extend(results_iterations_swap)
            aux_results.extend(results_iterations_3_opt)
        
        for i in range(len(aux_iterations) - 1):
            plt.plot(aux_iterations[i], aux_results[i], color = color_map[inc], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined_compare_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    #output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined_compare", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel("Valor de la solucion")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion del VNS con Swap y 3-Opt")
    legend_elements = [
        Line2D([0], [0], color='#0303ff', lw=1.5, label=f"10% incompatibilidad"),
        Line2D([0], [0], color='#fca105', lw=1.5, label=f"50% incompatibilidad"),
        Line2D([0], [0], color='#f51505', lw=1.5, label=f"25% incompatibilidad"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=f"75% incompatibilidad"),
        Line2D([0], [0], color='#60f702', lw=1.5, label=f"0% incompatibilidad")
    ]
    plt.legend(handles=legend_elements, fontsize=6)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()

def generate_vns_combined_graphic_results_compare_percentage(results):
    partial_route =  list(results.keys())[0]
    color_map = {"0.1": "#0303ff", "0.5": "#fca105", "0.25": "#f51505", "0.75": "#bd05f5", "0":"#60f702"}
    marker_list = ['o', 's', 'p', 'X', 'D']
    for j in range(len(results[partial_route])):
        result = results[partial_route][j]
        all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt, final_cost, intial_cost, route = result[0], result[1], result[2], result[3], result[4], result[5], result[6]
        aux_iterations = [0]
        aux_results = []
        heuristics = []
        inc = route.split("_")[1].split(".json")[0]
        for i in range(len(all_iterations_swap)):
            iterations_swap = all_iterations_swap[i]
            results_iterations_swap = all_results_iterations_swap[i]
            iterations_3_opt = all_iterations_3_opt[i]
            results_iterations_3_opt = all_results_iterations_3_opt[i]
            percetage_iterations = []
            for n in range(aux_iterations[-1] + 1, aux_iterations[-1] + 1 + len(iterations_swap)):
                aux_iterations.append(n)
                heuristics.append("swap")
            for n in range(aux_iterations[-1] + 1, aux_iterations[-1] + 1 + len(iterations_3_opt)):
                aux_iterations.append(n)
                heuristics.append("3-opt")
            for res_cost in results_iterations_swap:
                percetage_cost = round(((res_cost - final_cost) / final_cost) * 100, 2)
                percetage_iterations.append(percetage_cost)
            for res_cost in results_iterations_3_opt:
                percetage_cost = round(((res_cost - final_cost) / final_cost) * 100, 2)
                percetage_iterations.append(percetage_cost)
            aux_results.extend(percetage_iterations)

        for i in range(len(aux_iterations) - 1):
            plt.plot(aux_iterations[i], aux_results[i], color = color_map[inc], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined_compare_%_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    #output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined_compare_%", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel(f"% sobre la mejor solucion encontrada")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion del VNS con Swap y 3-Opt")
    legend_elements = [
        Line2D([0], [0], color='#0303ff', lw=1.5, label=f"10% incompatibilidad"),
        Line2D([0], [0], color='#fca105', lw=1.5, label=f"50% incompatibilidad"),
        Line2D([0], [0], color='#f51505', lw=1.5, label=f"25% incompatibilidad"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=f"75% incompatibilidad"),
        Line2D([0], [0], color='#60f702', lw=1.5, label=f"0% incompatibilidad")
    ]
    plt.legend(handles=legend_elements, fontsize=6)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()



