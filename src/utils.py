from node import Node


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