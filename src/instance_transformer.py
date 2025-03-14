import os
import json
from utils import euclidean_distance

def parse_input(input):

    lines = input.strip().split("\n")
    
    # Extraer cantidad de pedidos
    num_orders = int(lines[1])
    
    # Extraer nodos
    nodes = [list(map(int, line.split())) for line in lines[2:2 + 2 + 2 * num_orders]]
    
    final_destination = {"x": nodes[1][0], "y": nodes[1][1], "node_type": "final", "id": num_orders + 1, "item_id": 0}
    depot = {"x": nodes[0][0], "y": nodes[0][1], "node_type": "depot", "id": 0, "item_id": 0}
    
    pickups = []
    deliveries = []
    
    # Agregar pickups y deliveries
    for i in range(num_orders):
        pickup = {
            "x": nodes[2 + i][0],
            "y": nodes[2 + i][1],
            "node_type": "pickup",
            "id": i + 1,
            "item_id": i + 1
        }
        delivery = {
            "x": nodes[2 + num_orders + i][0],
            "y": nodes[2 + num_orders + i][1],
            "node_type": "delivery",
            "id": num_orders + 2 + i,
            "item_id": i + 1
        }
        pickups.append(pickup)
        deliveries.append(delivery)
    
    # Crear lista completa de nodos
    all_nodes = [depot] + pickups + deliveries + [final_destination]

    # Inicializar la matriz con ceros
    travel_costs = [[0] * num_orders for _ in range(num_orders)]
    matrix = [[0] * num_orders for _ in range(num_orders)]

    # Rellenar la matriz con las distancias euclidianas
    for i in range(num_orders):
        for j in range(num_orders):
            if i != j:
                travel_costs[i][j] = euclidean_distance(all_nodes[i], all_nodes[j])


    # Procesar incompatibilidades
    incompatibilities = lines[4 + 2 * num_orders:]
    for line in incompatibilities:
        items = list(map(int, line.split()))
        if len(items) > 1:
            base_item = items[0]
            for incompatible in items[1:]:
                matrix[base_item][incompatible] = 1
                matrix[incompatible][base_item] = 1  # Matriz simétrica

    result = {
        "depot": depot,
        "final_destination": final_destination,
        "pickup_nodes": pickups,
        "delivery_nodes": deliveries,
        "travel_costs": travel_costs,
        "incompatibilities": matrix
    }

    return json.dumps(result, indent=4)

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_path): 
            with open(input_path, "r", encoding="utf-8") as file:
                data = file.read()
            
            transformed_data = parse_input(data)

            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w", encoding="utf-8") as json_file:
                json_file.write(transformed_data)
            
input_folder = "../Instances_Pablo_raw"
output_folder = "../Instances_Pablo"

process_folder(input_folder, output_folder)