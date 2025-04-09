import math
from node import Node
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

def euclidean_distance(p1, p2):
    return int(round(math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"]), 0))

def generate_routes_json():
    instance_labels = ['a', 'b', 'c', 'd', 'e']
    densities = ["0.1", "0.5", "0.25", "0.75", "0"]
    folders = ["5", "10", "15", "20", "25", "30", "35", "50", "75", "100"]
    routes_json = []
    for folder in folders:
        for label in instance_labels:
            for sub_label in instance_labels:
                for density in densities:
                    route_label = "../Instances/"+ folder + "/prob" + folder + label + "/" + sub_label + "/density_" + density + ".json"
                    routes_json.append(route_label)
    return routes_json

def calculate_cost(S, travel_costs):
    total = 0
    for i, node in enumerate(S[:-1]): # Evitamos visitar el nodo final
        total += travel_costs[node.id][S[i+1].id]
    return total

def is_feasible_solution(S: list[Node], incompatibilities: list[list[int]]):
    active_items = set()
    if S[0].node_type != "depot" or S[-1].node_type != "final":
        return False

    for node in S[1:-1]:
        if node.node_type == "pickup":
            if any(incompatibilities[i - 1][node.item_id - 1] == 1 for i in active_items):
                return False
            active_items.add(node.item_id)
        else:
            if node.item_id not in active_items:
                return False
            active_items.remove(node.item_id)
    return True

def generate_initial_solution(input):
    depot = input["depot"]
    pickup_nodes = input["pickup_nodes"]
    delivery_nodes = input["delivery_nodes"]
    final_node = input["final_destination"]

    S = [Node(id = depot["id"], item_id = depot["item_id"], x = depot["x"], y = depot["y"], node_type = depot["node_type"])]

    for i in range(0, len(pickup_nodes)):
        # pickup y delivery nodes son simetricas
        p = pickup_nodes[i]
        d = delivery_nodes[i]

        node_p = Node(id = p["id"], item_id = p["item_id"], x = p["x"], y = p["y"], node_type = p["node_type"])
        node_d = Node(id = d["id"], item_id = d["item_id"], x = d["x"], y = d["y"], node_type = d["node_type"])

        S.append(node_p)
        S.append(node_d)

    node_f = Node(id = final_node["id"], item_id = final_node["item_id"], x = final_node["x"], y = final_node["y"], node_type = final_node["node_type"])

    S.append(node_f)

    return S

def generate_table_results(results, who):
    base_dir = "..\Results"
    os.makedirs(base_dir, exist_ok=True)
    df = pd.DataFrame(results)
    csv_path = os.path.join(base_dir, "results_" + who +".csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

def generate_graphic_results(iterations, result_iteration, route, who):
    instance_folder = route.split(".json")[0].split("Instances")[1].split("/")
    file_name = instance_folder[4] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who, instance_folder[1], instance_folder[2], instance_folder[3])
    os.makedirs(output_folder, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(iterations, result_iteration, marker="o", linestyle="-", color="b")
    plt.ylabel("Valor de la solucion")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Progreso de swap local search")
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()

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
    output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who + "_combined_compare_%_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel(f"% sobre la mejor solucion encontrada")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion de " + who + "local search")
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
    color_map = ["#0303ff", "#fca105", "#f51505", "#bd05f5", "#60f702"]
    marker_list = ['o', 's', 'p', 'X', 'D']
    for j in range(len(results[partial_route])):
        result = results[partial_route][j]
        all_iterations, all_results_iterations, final_cost, initial_cost, route = result[0], result[1], result[2], result[3], result[4]
        plt.plot(all_iterations, all_results_iterations, color = color_map[j], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')          

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_" + who + "_combined_compare_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel("Valor de la solucion")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion de " + who + "local search")
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
    color_map = {"swap": ["#0303ff", "#fca105", "#f5e905", "#bd05f5", "#ab0354"], "3-opt": ["#f51505", "#080100", "#60f702", "#02f7d6", "#05dbfc"]}
    marker_list = ['o', 's', 'p', 'X', 'D']
    for j in range(len(results[partial_route])):
        result = results[partial_route][j]
        all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt, route = result[0], result[1], result[2], result[3], result[4]
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
            plt.plot(aux_iterations[i], aux_results[i], color = color_map[heuristics[i]][j], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined_compare_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel("Valor de la solucion")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion del VNS con Swap y 3-Opt")
    legend_elements = [
        Line2D([0], [0], color='#0303ff', lw=1.5, label=""),
        Line2D([0], [0], color='#fca105', lw=1.5, label=""),
        Line2D([0], [0], color='#f5e905', lw=1.5, label="Swap Local Search"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=""),
        Line2D([0], [0], color='#ab0354', lw=1.5, label=""),
        Line2D([0], [0], color='white', lw=0, label=""),
        Line2D([0], [0], color='#f51505', lw=1.5, label=""),
        Line2D([0], [0], color='#080100', lw=1.5, label=""),
        Line2D([0], [0], color='#60f702', lw=1.5, label="3-Opt Local Search"),
        Line2D([0], [0], color='#02f7d6', lw=1.5, label=""),
        Line2D([0], [0], color='#05dbfc', lw=1.5, label="")     
    ]
    plt.legend(handles=legend_elements, fontsize=6)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()

def generate_vns_combined_graphic_results_compare_percentage(results):
    partial_route =  list(results.keys())[0]
    color_map = {"swap": {"0.1":"#0303ff", "0.5":"#fca105", "0.25":"#f5e905", "0.75":"#bd05f5", "0":"#ab0354"}, "3-opt": {"0.1":"#f51505", "0.5":"#080100", "0.25":"#60f702", "0.75":"#02f7d6", "0":"#05dbfc"}}
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
            plt.plot(aux_iterations[i], aux_results[i], color = color_map[heuristics[i]][inc], marker=marker_list[j], markersize=4, alpha=0.6, linestyle='-')

    partial_route_split = partial_route.split("/")
    file_name = "all_densities_" + partial_route_split[1] + "_" + partial_route_split[2] + ".png"
    output_folder = os.path.join("..", "Graphics", "Instances", "results_vns_combined_compare_%_without_limiter", partial_route_split[1], partial_route_split[2], partial_route_split[3])
    print("output_folder ", output_folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.ylabel(f"% sobre la mejor solucion encontrada")
    plt.xlabel("Cantidad de iteraciones")
    plt.title("Evolucion del VNS con Swap y 3-Opt")
    legend_elements = [
        Line2D([0], [0], color='#0303ff', lw=1.5, label=""),
        Line2D([0], [0], color='#fca105', lw=1.5, label=""),
        Line2D([0], [0], color='#f5e905', lw=1.5, label="Swap Local Search"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=""),
        Line2D([0], [0], color='#ab0354', lw=1.5, label=""),
        Line2D([0], [0], color='white', lw=0, label=""),
        Line2D([0], [0], color='#f51505', lw=1.5, label=""),
        Line2D([0], [0], color='#080100', lw=1.5, label=""),
        Line2D([0], [0], color='#60f702', lw=1.5, label="3-Opt Local Search"),
        Line2D([0], [0], color='#02f7d6', lw=1.5, label=""),
        Line2D([0], [0], color='#05dbfc', lw=1.5, label=""),
        Line2D([0], [0], color='white', lw=0, label=""),
        Line2D([0], [0], color='#0303ff', lw=1.5, label=f"10% incompatibilidad"),
        Line2D([0], [0], color='#f51505', lw=1.5, label=f"10% incompatibilidad"),
        Line2D([0], [0], color='#fca105', lw=1.5, label=f"50% incompatibilidad"),
        Line2D([0], [0], color='#080100', lw=1.5, label=f"50% incompatibilidad"),
        Line2D([0], [0], color='#f5e905', lw=1.5, label=f"25% incompatibilidad"),
        Line2D([0], [0], color='#60f702', lw=1.5, label=f"25% incompatibilidad"),
        Line2D([0], [0], color='#bd05f5', lw=1.5, label=f"75% incompatibilidad"),
        Line2D([0], [0], color='#02f7d6', lw=1.5, label=f"75% incompatibilidad"),
        Line2D([0], [0], color='#ab0354', lw=1.5, label=f"0% incompatibilidad"),
        Line2D([0], [0], color='#05dbfc', lw=1.5, label=f"0% incompatibilidad")
    ]
    plt.legend(handles=legend_elements, fontsize=6)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)  
    plt.close()