# import websocket
# ws = websocket.WebSocket()
# ws.connect("ws://localhost", http_proxy_host="proxy_host_name", http_proxy_port=50008)
# print "connected"
import time
# try:
#     ws = create_connection("ws://localhost:50008")
#     print "connected"
#     # ws.send("Hello, World")
# except Exception as e:
#     print e

from websocket import create_connection
ws = create_connection("ws://localhost:50008")
# ws.send("this is a string that is over 125 chars in length. Well maybe that is not true at this point but it sure is greater than 125 chars at this point.")
ws.send("hello")
# ws.recv()
time.sleep(5)
ws.close()
print "closed"

# from ws4py.websocket import WebSocket
# from ws4py.client.threadedclient import WebSocketClient
#
# class DummyClient(WebSocketClient):
#     def opened(self):
#         print "!!!!!!!!!!!!!"
#         def data_provider():
#             for i in range(1, 200, 25):
#                 yield "#" * i
#
#         self.send(data_provider())
#
#         for i in range(0, 200, 25):
#             print i
#             self.send("*" * i)
#
#     def closed(self, code, reason=None):
#         print "Closed down", code, reason
#
#     def received_message(self, m):
#         print m
#         if len(m) == 175:
#             self.close(reason='Bye bye')
#
# if __name__ == '__main__':
#     try:
#         ws = DummyClient('ws://localhost:50008/', protocols=['http-only', 'chat'])
#         print 'going to connect'
#         ws.connect()
#         print 'CONNECTED'
#         ws.run_forever()
#     except KeyboardInterrupt:
#         ws.close()
