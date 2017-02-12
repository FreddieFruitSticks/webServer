def task(connection, file_name):
	print 'start task'
	try:
		my_file = open(file_name)
		l = my_file.read(100)
		while l:
			connection.send(l)
			l = my_file.read(1024)
	except IOError:
		response = """
File not found
		"""
		connection.send(response)
		print 'error'
	finally:
		my_file.close()
		connection.close()
		print 'finished'
