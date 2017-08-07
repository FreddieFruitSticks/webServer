from ConnectionMap import ConnectionMap
from Queue import Queue
import time


class Broker(object):
    def __init__(self, send_ws_message):
        self.message_queue = Queue()
        self.connections = ConnectionMap()
        self.send = send_ws_message

    def listen_on_queue(self):
        while True:
            try:
                message = self.message_queue.pop()
                if message is not None:
                    self._broadcast_message(message)
                    print 'message broker got:', message.value
                time.sleep(0.1)
            except Exception as e:
                print "Something went wrong ", e

    def _broadcast_message(self, message):
        for connection in self.connections.get_hash_list():
            while connection is not None:
                try:
                    self.send(connection.connection, message.value)
                except Exception as e:
                    print "exception in broadcasting to this connection, closing it ", e
                    connection.connection.close()
                    self.connections.remove(connection.key)
                connection = connection.next_node

    def add_connection(self, address, connection):
        self.connections.put(address, connection)

    def remove_connection(self, address):
        self.connections.remove(address)

    def add_message_to_queue(self, message):
        self.message_queue.add(message)
