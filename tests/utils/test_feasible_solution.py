from node import Node
from utils import is_feasible_solution

def test_valid_solution():
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "pickup"),
        Node(2, 200, 200, "pickup"),
        Node(1, 150, 150, "delivery"),
        Node(2, 250, 250, "delivery"),
        Node(3, 300, 300, "final"),
    ]
    incompatibilities = [[0, 0], [0, 0]]  # No hay incompatibilidades
    assert is_feasible_solution(S, incompatibilities) == True

def test_delivery_before_pickup():
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "delivery"),  # Mal ordenado
        Node(1, 150, 150, "pickup"),
        Node(2, 200, 200, "pickup"),
        Node(2, 250, 250, "delivery"),
        Node(3, 300, 300, "final"),
    ]
    incompatibilities = [[0, 0], [0, 0]]
    assert is_feasible_solution(S, incompatibilities) == False

def test_incompatible_items():
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "pickup"),
        Node(2, 200, 200, "pickup"),  # Incompatible con 1
        Node(1, 150, 150, "delivery"),
        Node(2, 250, 250, "delivery"),
        Node(3, 300, 300, "final"),
    ]
    incompatibilities = [[0, 1], [1, 0]]  # 1 y 2 son incompatibles
    assert is_feasible_solution(S, incompatibilities) == False

def test_missing_depot_or_final():
    S1 = [  # Falta "depot"
        Node(1, 100, 100, "pickup"),
        Node(2, 200, 200, "pickup"),
        Node(1, 150, 150, "delivery"),
        Node(2, 250, 250, "delivery"),
        Node(3, 300, 300, "final"),
    ]
    S2 = [  # Falta "final"
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "pickup"),
        Node(2, 200, 200, "pickup"),
        Node(1, 150, 150, "delivery"),
        Node(2, 250, 250, "delivery"),
    ]
    incompatibilities = [[0, 0], [0, 0]]

    assert is_feasible_solution(S1, incompatibilities) == False
    assert is_feasible_solution(S2, incompatibilities) == False

def test_extra_delivery():
    S = [
        Node(0, 0, 0, "depot"),
        Node(1, 100, 100, "pickup"),
        Node(1, 150, 150, "delivery"),
        Node(2, 200, 200, "delivery"),  # Falta el pickup
        Node(3, 300, 300, "final"),
    ]
    incompatibilities = [[0, 0], [0, 0]]
    assert is_feasible_solution(S, incompatibilities) == False