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
