import socket

HOST = ''
PORT=50009

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST,PORT))
sock.listen(1)

def get_request_header_items(message):
	request_data = message.split("\n")
	request_header = request_data[0]
	return request_header.split(" ")

while True:
	try:
		conn, addr = sock.accept()	
		message = conn.recv(1024)
		items = get_request_header_items(message)
		try:
			my_file = open(items[1].split("/")[1])
			l = my_file.read(100)
			while l:
				conn.send(l)
				l = my_file.read(1024)
			my_file.close()
		except IOError:
			response = """
				File not found
			"""
			conn.send(response)
			print 'error'
		conn.close()		  
	finally:
		print "done"


