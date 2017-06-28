import sys


class ConnectionMap(object):
    def __init__(self):
        self.hash_list = []
        for i in range(0, 255):
            self.hash_list.append(None)

    def get_hash_list(self):
        return self.hash_list

    def put(self, address, connection):
        if address and connection is None:
            raise Exception("address or connection is null in connectionMap put")

        bucket = self.get_hash(address) % len(self.hash_list)
        if self.hash_list[bucket] is None:
            self.hash_list[bucket] = self.Node(address, connection)
        else:
            conn_node = self.hash_list[bucket]
            while conn_node.next_node is not None:
                conn_node = conn_node.next_node
            last_node = self.Node(address, connection)
            conn_node.set_next(last_node)
            last_node.set_previous(conn_node)

    def get(self, address):
        if address is None:
            raise Exception("address is none in connection map get")

        bucket = self.get_hash(address) % len(self.hash_list)
        conn_node = self.hash_list[bucket]
        while conn_node is not None and conn_node.key is not address:
            conn_node = conn_node.next_node
        return conn_node

    def remove(self, address):
        if address is None:
            raise Exception("address is none in connection map get")

        bucket = self.get_hash(address) % len(self.hash_list)
        conn_node = self.hash_list[bucket]

        while conn_node is not None and conn_node.key is not address:
            conn_node = conn_node.next_node

        if conn_node is not None:
            if conn_node.previous_node is not None:
                conn_node.previous_node.next_node = conn_node.next_node
            else:
                self.hash_list[bucket] = conn_node.next_node

            if conn_node.next_node is not None:
                conn_node.next_node.previous_node = conn_node.previous_node

    def print_bucket(self):
        for conn_node in self.hash_list:
            while conn_node is not None:
                print conn_node.key
                conn_node = conn_node.next_node

    def get_hash(self, key):
        my_hash = 0
        n = 1
        for character in key:
            my_hash += ord(character) * (31 ** n)
            n += 1
        return my_hash

    class Node(object):
        next_node = None
        previous_node = None
        key = None
        connection = None

        def __init__(self, key, connection):
            self.connection = connection
            self.key = key

        def set_next(self, node):
            self.next_node = node

        def set_previous(self, node):
            self.previous_node = node
