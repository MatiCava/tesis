import random
import json
import os
from utils import euclidean_distance

# Valores de n
n_values = [5, 10, 15, 20, 25, 30, 35]

# Letras para identificar instancias
instance_labels = ['a', 'b', 'c', 'd', 'e']

# Posibles densidades de incompatibilidad
densities = [0, 0.1, 0.25, 0.5, 0.75]

# Ruta donde guardar las instancias
base_dir = "..\Instances"
os.makedirs(base_dir, exist_ok=True)

# Generar las instancias
for n in n_values:

    # Carpeta correspondiente a las instancias de tamaño n
    n_dir = os.path.join(base_dir, str(n))  # Carpeta específica para cada n
    os.makedirs(n_dir, exist_ok=True)
    
    for label in instance_labels:
        # Carpeta correspondiente para esta instancia
        instance_dir = os.path.join(n_dir, f'prob{n}{label}')
        os.makedirs(instance_dir, exist_ok=True)
        
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(2 * n + 1)]
        
        # Generar un destino final aleatorio que no esté en los puntos ya creados
        final_destination_coord = (random.randint(0, 1000), random.randint(0, 1000))
        while final_destination_coord in points:
            final_destination_coord = (random.randint(0, 1000), random.randint(0, 1000))

        # Creamos el nodo final
        final_destination = {"x": final_destination_coord[0], "y": final_destination_coord[1], "node_type": "final", "id": 2*n+1, "item_id": 0}

        # El primer punto es el depósito
        depot = {"x": points[0][0], "y": points[0][1], "node_type": "depot", "id": 0, "item_id": 0}
        
        pickups = [{"x": points[i][0], "y": points[i][1], "node_type": "pickup", "id": i, "item_id": i} for i in range(1, n+1)]
        deliveries = [{"x": points[i][0], "y": points[i][1], "node_type": "delivery", "id": i, "item_id": i - n} for i in range(n+1, 2*n+1)]

        # Crear lista completa de nodos
        all_nodes = [depot] + pickups + deliveries + [final_destination]

        # Numero total de nodos (deposito + pickups + deliveries + destino final)
        num_nodes = len(all_nodes)

        # Inicializar la matriz con ceros
        travel_costs = [[0] * num_nodes for _ in range(num_nodes)]

        # Rellenar la matriz con las distancias euclidianas
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j:
                    travel_costs[i][j] = euclidean_distance(all_nodes[i], all_nodes[j])


        # Generamos las 5 variantes de incompatibilidades
        for density in densities:

            # Inicializar la matriz de incompatibilidades con ceros
            incompatibility_graph = [[0] * n for _ in range(n)]

            # Cantidad de incompatibilidades a generar
            total_possible_edges = (n * (n - 1)) // 2  # Combinaciones posibles entre items
            num_incompatibilities = round(density * total_possible_edges)  # Proporción de la densidad

            # Generar pares de items incompatibles aleatoriamente
            possible_pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
            selected_pairs = random.sample(possible_pairs, num_incompatibilities)

            for i, j in selected_pairs:
                incompatibility_graph[i][j] = 1
                incompatibility_graph[j][i] = 1  # Simetría

            # Guardar la instancia con incompatibilidades
            instance_data = {
                'depot': depot,
                'final_destination': final_destination,
                'pickup_nodes': pickups,
                'delivery_nodes': deliveries,
                'travel_costs': travel_costs,
                'incompatibilities': incompatibility_graph
            }

            file_name = os.path.join(instance_dir, f'density_{density}.json')
            with open(file_name, 'w') as f:
                json.dump(instance_data, f, indent=4)

            print(f'Instancia con {density*100}% de incompatibilidades creada: {file_name}')
