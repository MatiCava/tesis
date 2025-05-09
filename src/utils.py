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
    folders = ["5", "10", "15", "20", "25", "30", "35", "50", "75", "100", "200", "300", "400", "500"]
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

def max_iteration_swap(size, method="percentile"):
    if method == "linear":
        return 0.462 * size - 6.93
    elif method == "polinomial":
        return 1
    elif method == "percentile":
        return 0.83 * size - 11.24
    
def max_iteration_three_opt(size, method="linear"):
    if method == "linear":
        return 0.121 * size + -0.85
    elif method == "polinomial":
        return 1
    elif method == "percentile":
        return 0.13 * size - 0.55