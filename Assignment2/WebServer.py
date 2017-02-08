import socket
from ThreadPool import ThreadPool

HOST = ''
PORT=50009

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST,PORT))
sock.listen(1)

def get_file_name_from_header(message):
	request_data = message.split("\n")
	request_header = request_data[0]
	return request_header.split(" ")[1].split("/")[1]

def task(connection, file_name):
	try:
		my_file = open(file_name)
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

if __name__ == "__main__":
	thread_pool = ThreadPool(4)
	thread_pool.start()
	while True:
		try:
			conn, addr = sock.accept()
			message = conn.recv(1024)
			file_name = get_file_name_from_header(message)
			thread_pool.submit_task(task, {'connection':conn,'file_name':file_name})		
			conn.close()
		except KeyboardInterrupt:
			thread_pool.close()
			raise		  
		finally:
			print "done"


