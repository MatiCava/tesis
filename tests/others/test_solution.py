from node import Node
from utils import calculate_cost, is_feasible_solution

def test_solution():
    solution = [
        Node(id=0, item_id=0, x=454, y=42, node_type="depot"),
        Node(id=3, item_id=3, x=990, y=188, node_type="pickup"),
        Node(id=5, item_id=5, x=573, y=351, node_type="pickup"),
        Node(id=2, item_id=2, x=2, y=565, node_type="pickup"),
        Node(id=4, item_id=4, x=366, y=750, node_type="pickup"),
        Node(id=1, item_id=1, x=336, y=835, node_type="pickup"),
        Node(id=7, item_id=2, x=154, y=951, node_type="delivery"),
        Node(id=9, item_id=4, x=140, y=807, node_type="delivery"),
        Node(id=10, item_id=5, x=211, y=622, node_type="delivery"),
        Node(id=8, item_id=3, x=217, y=585, node_type="delivery"),
        Node(id=6, item_id=1, x=64, y=133, node_type="delivery"),
        Node(id=11, item_id=0, x=454, y=42, node_type="final")
    ]

    travel_costs = [
        [
            0,
            802,
            691,
            556,
            713,
            331,
            400,
            957,
            592,
            827,
            629,
            0
        ],
        [
            802,
            0,
            429,
            920,
            90,
            539,
            753,
            216,
            277,
            198,
            247,
            802
        ],
        [
            691,
            429,
            0,
            1057,
            408,
            610,
            436,
            415,
            216,
            279,
            217,
            691
        ],
        [
            556,
            920,
            1057,
            0,
            840,
            448,
            928,
            1132,
            869,
            1052,
            892,
            556
        ],
        [
            713,
            90,
            408,
            840,
            0,
            449,
            687,
            292,
            222,
            233,
            201,
            713
        ],
        [
            331,
            539,
            610,
            448,
            449,
            0,
            554,
            732,
            426,
            629,
            452,
            331
        ],
        [
            400,
            753,
            436,
            928,
            687,
            554,
            0,
            823,
            477,
            678,
            511,
            400
        ],
        [
            957,
            216,
            415,
            1132,
            292,
            732,
            823,
            0,
            371,
            145,
            334,
            957
        ],
        [
            592,
            277,
            216,
            869,
            222,
            426,
            477,
            371,
            0,
            235,
            37,
            592
        ],
        [
            827,
            198,
            279,
            1052,
            233,
            629,
            678,
            145,
            235,
            0,
            198,
            827
        ],
        [
            629,
            247,
            217,
            892,
            201,
            452,
            511,
            334,
            37,
            198,
            0,
            629
        ],
        [
            0,
            802,
            691,
            556,
            713,
            331,
            400,
            957,
            592,
            827,
            629,
            0
        ]
    ]

    incompatibilities = [
        [
            0,
            0,
            0,
            0,
            0
        ],
        [
            0,
            0,
            0,
            0,
            0
        ],
        [
            0,
            0,
            0,
            0,
            0
        ],
        [
            0,
            0,
            0,
            0,
            0
        ],
        [
            0,
            0,
            0,
            0,
            0
        ]
    ]

    assert is_feasible_solution(solution, incompatibilities)

    assert calculate_cost(solution, travel_costs) == 3585

