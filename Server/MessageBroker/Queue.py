import threading
import time


class Queue(object):
    head_node = None
    end_node = None

    my_mutex = threading.Lock()

    def is_empty(self):
        return self.head_node is None and self.end_node is None

    def add(self, a_node_value):
        self.my_mutex.acquire()
        print "adding to the queue: ", a_node_value
        node = self.Node(a_node_value)
        if not self.is_empty():
            self.head_node.prev_node = node
            node.next_node = self.head_node
            self.head_node = node
        else:
            self.head_node = node
            self.end_node = node
        time.sleep(0.5)
        self.my_mutex.release()

    def pop(self):
        self.my_mutex.acquire()

        if not self.is_empty():
            node = self._replace_out_end_node()
            self.my_mutex.release()
            return node
        else:
            self.my_mutex.release()
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
