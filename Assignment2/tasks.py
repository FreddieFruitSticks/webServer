from datetime import datetime
import os
from email.utils import formatdate


def task_get_file(connection, file_name, user_agent, response_header):
    data = {'date': formatdate(timeval=None, localtime=False, usegmt=True), 'user_agent': user_agent,
            'content_length': os.path.getsize(os.getcwd() + "/" + file_name)}
    try:
        my_file = open(file_name)
        l = my_file.read(10)
        data.update({'body': l})
        data = {'date': formatdate(timeval=None, localtime=False, usegmt=True), 'user_agent': user_agent,
                'content_length': os.path.getsize(os.getcwd() + "/" + file_name), 'body': l}
        connection.send(response_header.format(**data))
        while l:
            l = my_file.read(10)
            connection.send(l)
        my_file.close()
    except IOError:
        l = """
<html><body><h1>File Not Found</h1></body></html>
"""
        data.update({'body': l})
        connection.send(response_header.format(**data))
        print 'error'
    finally:
        connection.close()
        print 'finished task_get_file'
