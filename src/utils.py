from node import Node

def generate_routes_json():
    instance_labels = ['a', 'b', 'c', 'd', 'e']
    densities = ["0.1", "0.5", "0.25", "0.75", "0"]
    folders = ["5", "10", "15", "20", "25", "30", "35"]
    routes_json = []
    for folder in folders:
        for label in instance_labels:
            for density in densities:
                label_test = "../Instances/"+ folder + "/prob" + folder + label + "/density_" + density + ".json"
                routes_json.append(label_test)
    return routes_json

def calculate_cost(S, travel_costs):
    total = 0
    for i, node in enumerate(S[:-1]): # Evitamos visitar el nodo final
        total += travel_costs[node.id][S[i+1].id]
    return total

def is_feasible_solution(S: list[Node], incompatibilities: list[list[int]]):
    active_items = set()
    if S[0][0].node_type != "depot" or S[-1][0].node_type != "final":
        return False

    for tuple in S[1:-1]:
        for node in tuple:
            if node.node_type == "pickup":
                if any(incompatibilities[i - 1][node.id - 1] == 1 for i in active_items):
                    return False
                active_items.add(node.id)
            else:
                if node.id not in active_items:
                    return False
                active_items.remove(node.id)
    return True

def generate_initial_solution(input):
    depot = input["depot"]
    pickup_nodes = input["pickup_nodes"]
    delivery_nodes = input["delivery_nodes"]
    final_node = input["final_destination"]

    S = [Node(id = depot["id"], x = depot["x"], y = depot["y"], node_type = depot["node_type"])]
    P = []
    D = []

    for i in range(0, len(pickup_nodes)):
        # pickup y delivery nodes son simetricas
        p = pickup_nodes[i]
        d = delivery_nodes[i]

        node_p = Node(id = p["id"], x = p["x"], y = p["y"], node_type = p["node_type"])
        node_d = Node(id = d["id"], x = d["x"], y = d["y"], node_type = d["node_type"])

        S.append(node_p)
        S.append(node_d)
        P.append(node_p)
        D.append(node_d)

    S.append(Node(id = final_node["id"], x = final_node["x"], y = final_node["y"], node_type = final_node["node_type"]))

    return S, P, D