import socket, threading, time

HOST='192.168.1.102'
SERVER_PORT=50007
RECV_PORT=50008
exit_app=False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,SERVER_PORT))
server_message = sock.recv(1024)
sock.shutdown(socket.SHUT_RDWR)
sock.close()

if server_message == 'server':
	recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		recv_socket.bind(('',RECV_PORT))
	except socket.error:
		recv_socket.bind(('',RECV_PORT+1))

	recv_socket.listen(1)
	print 'Waiting for connection...'
	conn, addr2 = recv_socket.accept()
	print 'connected to '+addr2[0]
else:
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		conn.connect((server_message,RECV_PORT))
	except socket.error:
		conn.connect((server_message,RECV_PORT+1))

def send_worker():
	while not exit_app:
		message = raw_input()
		conn.send(message)

def recv_worker():
	while not exit_app:
		message = conn.recv(1024)
		print message
	conn.shutdown(socket.SHUT_RDWR)
	conn.close()
	if recv_socket:
		recv_socket.shutdown(socket.SHUT_RDWR)
		recv_socket.close()

if __name__ == "__main__":
	try:	
		send_thread = threading.Thread(target=send_worker)
		recv_thread = threading.Thread(target=recv_worker)
		send_thread.daemon = True
		recv_thread.daemon = True
		send_thread.start()
		recv_thread.start()
		while threading.active_count() > 0:
			time.sleep(0.1)
	except KeyboardInterrupt:
		exit_app = True
		raise




