from ConnectionMap import ConnectionMap
from Queue import Queue
import time


class Broker(object):
    def __init__(self):
        self.message_queue = Queue()
        self.connections = ConnectionMap()

    def listen_on_queue(self):
        while True:
            message = self.message_queue.pop()
            if message is not None:
                # self._broadcast_message(message)
                print 'message broker got:', message.value
            time.sleep(0.1)

    def _broadcast_message(self, message):
        for connection in self.connections.get_hash_list():
            if connection is not None:
                connection.send(message)

    def add_connection(self, address, connection):
        self.connections.put(address, connection)

    def remove_connection(self, address):
        self.connections.remove(address)

    def add_message_to_queue(self, message):
        self.message_queue.add(message)