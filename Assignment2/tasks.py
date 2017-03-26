
def task_get_file(connection, file_name):
	response = """
	HTTP/1.1 200 OK
	Date: Mon, 27 Jul 2017 12:28:53 GMT
	Server: FreddiesServer
	Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
	Content-Length: 88
	Content-Type: text/html
	Connection: Closed

{}
	"""
	try:
		my_file = open(file_name)
		l = my_file.read(100)
		while l:
			connection.send(response.format(l))
			l = my_file.read(1024)
	except IOError:
		response = """
HTTP/1.1 200 OK
Date: Mon, 27 Jul 2017 12:28:53 GMT
Server: FreddiesServer
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: 88
Content-Type: text/html
Connection: Closed

<html><body><h1>File Not Found</h1></body></html>
"""
		connection.send(response)
		print 'error'
	finally:
		my_file.close()
		connection.close()
		print 'finished task_get_file'
