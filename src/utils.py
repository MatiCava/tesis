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

def generate_vns_combined_graphic_results(all_iterations_swap, all_results_iterations_swap, all_iterations_3_opt, all_results_iterations_3_opt, route):
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