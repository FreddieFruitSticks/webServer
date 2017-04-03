import os
from email.utils import formatdate
from ResponseBuilder import ResponseBuilder


def task_get_file(connection, file_name, user_agent):
    response = ResponseBuilder()
    response.with_date(formatdate(timeval=None, localtime=False, usegmt=True))\
            .with_content_type("text/html; charset=utf-8")\
            .with_server("FredServer")\
            .with_user_agent(user_agent)

    try:
        my_file = open(file_name)
        l = my_file.read(10)
        response.with_body(l)\
                .with_status(200)\
                .with_content_length(os.path.getsize(os.getcwd() + "/" + file_name))\
                .with_status_en("OK")
        connection.send(response.build())
        while l:
            l = my_file.read(10)
            connection.send(l)
        my_file.close()
    except IOError:
        l = """
<html><body><h1>File Not Found</h1></body></html>
"""
        response.with_body(l)\
                .with_status(404)\
                .with_status_en("File Not Found")\
                .with_content_length(0)

        connection.send(response.build())
    finally:
        connection.close()
