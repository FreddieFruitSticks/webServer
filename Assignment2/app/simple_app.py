import os, sys
from email.utils import formatdate


def simple_app(environ, start_response):
    status = '200 OK'
    message = '\nHello from simple_app'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-length', str(len(message))),
        ('Date', formatdate(timeval=None, localtime=False, usegmt=True)),
        ('Host', 'FredServer')]
    start_response(status, response_headers)
    return [message]

