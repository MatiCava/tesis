class Node:
    __slots__ = ("id", "x", "y", "node_type", "prev", "next")  # Solo permite estos atributos



    def __init__(self, id, x, y, node_type, prev, next):
        self.id = id
        self.x = x
        self.y = y
        self.node_type = node_type
        self.prev = prev
        self.next = next


    def __repr__(self):
        prev_id = self.prev.id if isinstance(self.prev, Node) else None
        next_id = self.next.id if isinstance(self.next, Node) else None
        return f"Node(id={self.id}, x={self.x}, y={self.y}, type={self.node_type}, prev={prev_id}, next={next_id})"
    
    def __hash__(self):
        return hash((self.id, self.node_type))

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.id == other.id and
                    self.node_type == other.node_type)
        return False