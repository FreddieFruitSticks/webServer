import os, sys


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('DOCUMENT_ROOT', environ.get('DOCUMENT_ROOT')),
        ('HTTP_HOST', environ.get('HTTP_HOST')),
        ('REMOTE_ADDR', environ.get('REMOTE_ADDR')),
        ('REMOTE_HOST', environ.get('REMOTE_HOST'))]
    start_response(status, response_headers)
    return ['Hello from simple_app\n']

