def task(connection, file_name):
	try:
		my_file = open(file_name)
		l = my_file.read(100)
		while l:
			connection.send(l)
			l = my_file.read(1024)

		my_file.close()
	except IOError:
		response = """
File not found
		"""
		connection.send(response)
		print 'error'
	finally:
		connection.close()
