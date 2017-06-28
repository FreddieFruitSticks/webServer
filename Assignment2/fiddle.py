import sys, re, hashlib, base64, binascii, threading, time
from MessageBroker import ConnectionMap
from MessageBroker import Queue, Broker

# my_map = ConnectionMap.ConnectionMap()
#
# my_map.put("192.168.0.1", "my_conn")
# my_map.put("192.168.0.2", "my_conn2")
# my_map.put("192.168.0.2", "my_conn3")
# my_map.print_bucket()
# print "-------------"
# my_map.remove("192.168.0.2")
# my_map.print_bucket()
#
# print my_map.get("192.168.0.2").connection

# my_q = Queue.Queue()
# thread = threading.Thread(target=my_q.add(10))
# thread.start()
#
# val = my_q.pop()
#
# print val.value
# my_q.add(10)
# my_q.add(11)
#
#
# print my_q.pop().value

broker = Broker.Broker()
thread = threading.Thread(target=broker.listen_on_queue)
thread.daemon = True
thread.start()

broker.add_message_to_queue("conn1")

# time.sleep(2)

broker.add_message_to_queue("conn2")
# time.sleep(2)
