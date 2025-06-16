import math
import random
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

def generate_initial_solution_random(input):
    incompatibilities = input["incompatibilities"]
    depot = input["depot"]
    all_nodes = input["pickup_nodes"] + input["delivery_nodes"]
    final_node = input["final_destination"]
    random.seed(42)
    random.shuffle(all_nodes)
    active_items = set()

    S = [Node(id = depot["id"], item_id = depot["item_id"], x = depot["x"], y = depot["y"], node_type = depot["node_type"])]

    while all_nodes:
        for node in all_nodes[:]:
            if node["node_type"] == "pickup":
                if not any(incompatibilities[i - 1][node["item_id"] - 1] == 1 for i in active_items):
                    active_items.add(node["item_id"])
                    S.append(Node(id = node["id"], item_id = node["item_id"], x = node["x"], y = node["y"], node_type = node["node_type"]))
                    all_nodes.remove(node)
            else:
                if node["item_id"] in active_items:
                    active_items.remove(node["item_id"])
                    S.append(Node(id = node["id"], item_id = node["item_id"], x = node["x"], y = node["y"], node_type = node["node_type"]))
                    all_nodes.remove(node)
            
    node_f = Node(id = final_node["id"], item_id = final_node["item_id"], x = final_node["x"], y = final_node["y"], node_type = final_node["node_type"])

    S.append(node_f)

    return S

def max_iteration_swap(size, inc):
    coeff = {
        0.0: (0.002718, 3.2131, -21.62),
        0.1: (-0.000089, 2.2967, -4.75),
        0.25: (0.000133, 1.6752, -3.53),
        0.5: (0.000250, 1.0949, 0.49),
        0.75: (0.000219, 0.7725, -1.40)
    }
    if inc not in coeff:
        return 0  
    a, b, c = coeff[inc]
    iterations = int(round(a * size**2 + b * size + c))
    return abs(iterations)
    
def max_iteration_three_opt(size, inc):
    coeff = {
        0.1: (0.000007, -0.0054, 0.97),
        0.25: (0.000019, -0.0136, 2.25),
        0.5: (0.000017, -0.0153, 3.41),
        0.75: (-0.000013, -0.0012, 5.54)
    }
    if inc not in coeff:
        return 1  
    a, b, c = coeff[inc]
    iterations = int(round(a * size**2 + b * size + c)) + 1
    return abs(iterations)