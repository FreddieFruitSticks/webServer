# Simple Queue object that I wanted to do myself for gees.
class Queue(object):
    head_node = None
    end_node = None

    def is_empty(self):
        return self.head_node == None and self.end_node == None

    def add(self, a_node_value):
        node = self.Node(a_node_value)

        if not self.is_empty():
            self.head_node.prev_node = node
            node.next_node = self.head_node
            self.head_node = node
        else:
            self.head_node = node
            self.end_node = node

    def pop(self):
        if not self.is_empty():
            node = self._replace_out_end_node()
            return node
        else:
            return None

    def _replace_out_end_node(self):
        node = self.end_node
        if self.end_node is not None and self.end_node.prev_node is not None:
            self.end_node.prev_node.next_node = None
            self.end_node = node.prev_node
        else:
            self.end_node = None
            self.head_node = None

        return node

    class Node(object):
        prev_node = None
        next_node = None
        value = None

        def __init__(self, val):
            self.value = val
