class Node:
    __slots__ = ("id", "x", "y", "node_type", "prev", "next")  # Solo permite estos atributos



    def __init__(self, id, x, y, node_type, prev=None, next=None):
        self.id = id
        self.x = x
        self.y = y
        self.node_type = node_type
        self.prev = None
        self.next = None


    def __repr__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, type={self.node_type})"
    
    def __hash__(self):
        return hash((self.id, self.node_type))

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.id == other.id and
                    self.node_type == other.node_type)
        return False