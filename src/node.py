class Node:
    __slots__ = ("id", "item_id", "x", "y", "node_type")  # Solo permite estos atributos

    def __init__(self, id, item_id, x, y, node_type):
        self.id = id
        self.item_id = item_id
        self.x = x
        self.y = y
        self.node_type = node_type

    def __repr__(self):
        return f"Node(id={self.id}, item_id={self.item_id}, x={self.x}, y={self.y}, type={self.node_type})"
    
    def __hash__(self):
        return hash((self.id, self.item_id, self.node_type))

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.id == other.id and
                    self.item_id == other.item_id and
                    self.node_type == other.node_type)
        return False