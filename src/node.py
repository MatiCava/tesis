class Node:
    __slots__ = ("id", "x", "y", "node_type")  # Solo permite estos atributos

    def __init__(self, id, x, y, node_type):
        self.id = id
        self.x = x
        self.y = y
        self.node_type = node_type

    def __repr__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, type={self.node_type})"