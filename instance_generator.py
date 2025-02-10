import random
import math
import json
import os

# Función para calcular la distancia euclidiana
def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Valores de n
n_values = [5, 10, 15, 20, 25, 30, 35]

# Letras para identificar instancias
instance_labels = ['a', 'b', 'c', 'd', 'e']

# Ruta donde guardar las instancias
base_dir = "Instances"
os.makedirs(base_dir, exist_ok=True)

# Generar las instancias
for n in n_values:

    # Carpeta correspondiente a las instancias
    n_dir = os.path.join(base_dir, str(n))  # Carpeta específica para cada n
    os.makedirs(n_dir, exist_ok=True)
    
    for label in instance_labels:
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(2 * n + 1)]
        
        # El primer punto es el depósito
        depot = points[0]
        
        # Crear pares de solicitudes y calcular sus costos directamente
        requests = []

        pickups = points[1:n+1]
        deliveries = points[n+1:(n*2)+1]
        requests = list(zip(pickups, deliveries))

        # Generar un destino final aleatorio que no esté en los puntos ya creados
        final_destination = (random.randint(0, 1000), random.randint(0, 1000))
        while final_destination in points:
            final_destination = (random.randint(0, 1000), random.randint(0, 1000))

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


        # Guardar la instancia en un archivo JSON
        instance_data = {
            'depot': depot,
            'final_destination': final_destination,
            'requests': requests,
            'travel_costs': travel_costs
        }


        # Guardar las instancias
        file_name = os.path.join(n_dir, f'prob{n}{label}.json')
        with open(file_name, 'w') as f:
            json.dump(instance_data, f, indent=4)

        print(f'Instancia {file_name} creada.')
