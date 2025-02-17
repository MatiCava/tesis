from node import Node
from utils import calculate_cost

def test_valid_route():
    # Definimos una lista de nodos
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "pickup"),
        Node(2, 200, 200, "delivery"),
        Node(3, 300, 300, "final"),
    ]

    # Definimos una matriz de costos de viaje
    travel_costs = [
        [0, 10, 20, 30],
        [10, 0, 15, 25],
        [20, 15, 0, 35], 
        [30, 25, 35, 0], 
    ]

    # Total: 10 + 15 + 35 = 60
    assert calculate_cost(S, travel_costs) == 60

def test_single_node_route():
    # Solo hay un nodo (depósito y final)
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 0, 0, "final"),
    ]

    # Matriz de costos
    travel_costs = [
        [0, 5],
        [5, 0],
    ]

    # El costo debería ser 5 (depósito -> final)
    assert calculate_cost(S, travel_costs) == 5

def test_zero_cost_route():
    # Todos los costos son cero
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "pickup"),
        Node(2, 200, 200, "delivery"),
        Node(3, 300, 300, "final"),
    ]

    # Matriz de costos con todos los valores en cero
    travel_costs = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    # El costo total debería ser 0
    assert calculate_cost(S, travel_costs) == 0