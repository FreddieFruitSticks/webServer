import socket

HOST=''
PORT=50007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST,PORT))
sock.listen(1)
while True:
	conn1, addr1 = sock.accept()
	conn1.send('server')

	conn2, addr2 = sock.accept()
	conn2.send(addr1[0])


