import sys, re, hashlib, base64, binascii
from MessageBroker import ConnectionMap

my_map = ConnectionMap.ConnectionMap()

my_map.put("192.168.0.1", "my_conn")
my_map.put("192.168.0.2", "my_conn2")
my_map.put("192.168.0.2", "my_conn3")
my_map.print_bucket()
print "-------------"
# my_map.remove("192.168.0.2")
my_map.print_bucket()

print my_map.get("192.168.0.2").connection
