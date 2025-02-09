import random
import math
import json

# Función para calcular la distancia euclidiana
def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Valores de n
n_values = [5, 10, 15, 20, 25, 30, 35]

# Letras para identificar instancias
instance_labels = ['a', 'b', 'c', 'd', 'e']

# Generar las instancias
for n in n_values:
    for label in instance_labels:
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(2 * n + 1)]
        
        # El primer punto es el depósito
        depot = points[0]
        
        # Crear pares de solicitudes y calcular sus costos directamente
        requests = []
        travel_costs = {}

        for i in range(1, n + 1):
            pickup = points[i]
            delivery = points[n + i]
            requests.append((pickup, delivery))
            
            # Calcular la distancia euclidiana para cada solicitud
            cost = euclidean_distance(pickup, delivery)
            travel_costs[f'{i}-{n+i}'] = cost
        
        # Guardar la instancia en un archivo JSON
        instance_data = {
            'depot': depot,
            'requests': requests,
            'travel_costs': travel_costs
        }

        file_name = f'prob{n}{label}.json'
        with open(file_name, 'w') as f:
            json.dump(instance_data, f, indent=4)

        print(f'Instancia {file_name} creada.')
