import pytest
from node import Node
from three_opt import add_edges, rearrange_solution, subtract_edges
from utils import calculate_cost


@pytest.fixture
def setup():
    solution = [
        [Node(id=0, item_id=0, x=101, y=567, node_type="depot")], 
        [Node(id=4, item_id=4, x=109, y=812, node_type="pickup"), Node(id=9, item_id=4, x=950, y=596, node_type="delivery")], 
        [Node(id=2, item_id=2, x=705, y=161, node_type="pickup"), Node(id=7, item_id=2, x=172, y=533, node_type="delivery")], 
        [Node(id=5, item_id=5, x=277, y=412, node_type="pickup"), Node(id=10, item_id=5, x=641, y=335, node_type="delivery")], 
        [Node(id=3, item_id=3, x=512, y=509, node_type="pickup"), Node(id=8, item_id=3, x=449, y=618, node_type="delivery")], 
        [Node(id=1, item_id=1, x=246, y=925, node_type="pickup"), Node(id=6, item_id=1, x=262, y=267, node_type="delivery")], 
        [Node(id=6, item_id=0, x=907, y=595, node_type="final")]
    ]

    travel_costs = [
        [0, 386, 728, 415, 245, 235, 340, 79, 352, 849, 588, 806],
        [386, 0, 891, 494, 178, 514, 658, 399, 368, 777, 710, 739],
        [728, 891, 0, 398, 883, 496, 456, 650, 524, 499, 185, 479],
        [415, 494, 398, 0, 504, 254, 348, 341, 126, 447, 217, 404],
        [245, 178, 883, 504, 0, 434, 566, 286, 391, 868, 715, 827],
        [235, 514, 496, 254, 434, 0, 146, 160, 268, 698, 372, 656],
        [340, 658, 456, 348, 566, 146, 0, 281, 398, 763, 385, 724],
        [79, 399, 650, 341, 286, 160, 281, 0, 290, 781, 509, 738],
        [352, 368, 524, 126, 391, 268, 398, 290, 0, 501, 342, 459],
        [849, 777, 499, 447, 868, 698, 763, 781, 501, 0, 404, 43],
        [588, 710, 185, 217, 715, 372, 385, 509, 342, 404, 0, 372],
        [806, 739, 479, 404, 827, 656, 724, 738, 459, 43, 372, 0]
    ]

    flatten_solution = [node for sublist in solution for node in sublist]
    original_cost = calculate_cost(flatten_solution, travel_costs)

    return solution, original_cost, travel_costs


def test_substract_edges(setup):
    lst, original_cost, travel_costs = setup

    combs = [1, 3, 4]
    
    sub_cost = subtract_edges(lst, original_cost, combs, travel_costs)

    assert sub_cost == 2674


def test_add_edges(setup):
    lst, original_cost, travel_costs = setup
    combs = [1, 3, 4]
    perms = [4, 1, 3]

    new_cost = subtract_edges(lst, original_cost, combs, travel_costs)

    total_cost = add_edges(lst, new_cost, combs, perms, travel_costs)

    assert total_cost == 5307