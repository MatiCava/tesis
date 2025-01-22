
def reverse_based_local_search(solution, graph, capacity, incompatibilities, calculate_route_cost):
    """
    Aplica de manera inversa la búsqueda local original para generar una vecindad y encontrar
    la mejor solución posible, respetando restricciones de compatibilidad y capacidad.

    Prerrequisitos:
        - La solución inicial debe ser válida, es decir, respetar restricciones de precedencia 
          (pickup antes de delivery) y capacidad del vehículo.
        - La matriz de incompatibilidad debe estar correctamente definida y tener dimensiones 
          consistentes con la cantidad de nodos.

    Args:
        solution (list): Lista ordenada de nodos (Pickup y Delivery).
        grafo (dict): Representación del grafo con información de nodos y aristas.
        capacity (int): Capacidad máxima del vehículo.
        incompatibilities (list[list]): Matriz que indica incompatibilidades entre items.
        calculate_route_cost (callable): Función que calcula el costo de una solución.

    Returns:
        list: La mejor solución encontrada en la vecindad generada.
        float: El costo asociado a la mejor solución.

    Nota:
        La función evalúa soluciones vecinas moviendo pickups hacia atrás y deliveries hacia 
        adelante, generando nuevas configuraciones válidas y seleccionando la de menor costo.
    """

    best_route = solution
    best_cost = calculate_route_cost(solution, graph)

    '''
    Para cada nodo de la solucion actual:
        Si es Pickup:
            Comparar con el anterior (izquierda)
            Si el anterior es Delivery:
                Si son incompatibles:
                    Break
                Si excede la capacidad:
                    Break
                Mover nodo actual hacia atras (intercambiar posiciones)
                Evaluar costo de la nueva solucion
                Si el costo nuevo < mejor costo:
                    La mejor solucion es la nueva
                    El mejor costo es el costo de la nueva solucion
            Si el anterior es el nodo deposito:
                Break

        Si es Delivery:
            Comparar con el siguiente (derecha)
            Si el siguiente es Pikcup:
                Si son incompatibles:
                    Break
                Si se excede la capacidad:
                    Break
                Mover nodo actual hacia adelante (intercambiar posiciones)
                Evaluar costo de la nueva solucion
                Si el costo nuevo < mejor costo:
                    La mejor solucion es la nueva
                    El mejor costo es el costo de la nueva solucion
            Si el siguiente es el nodo deposito:
                Break
    '''