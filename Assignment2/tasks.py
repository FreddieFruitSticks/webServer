from datetime import datetime
import os
from email.utils import formatdate

def task_get_file(connection, file_name, user_agent):
	response ="""
HTTP/1.1 200 OK\r\nDate: {}\nServer: FreddiesServer/0.0.1\nUser-Agent: {}\nContent-length:{}\nContent-Type:text/html; charset=utf-8

{}"""
	try:
		my_file = open(file_name)
		l = my_file.read(10)
		connection.send(response.format(
						formatdate(timeval=None, localtime=False, usegmt=True),
						user_agent,
						os.path.getsize(os.getcwd()+"/"+file_name),
						l))
		while l:
			l = my_file.read(10)
			connection.send(l)
		my_file.close()
	except IOError:
		message = """
<html><body><h1>File Not Found</h1></body></html>
"""
		connection.send(response.format(message))
		print 'error'
	finally:
		connection.close()
		print 'finished task_get_file'
