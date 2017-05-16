import os, sys


def run_with_wsgi(application):
    environ = {}
    environ.update(os.environ)

    headers = []

    def write(data):
        sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status, headers):
        for header in headers:
            sys.stdout.write(header[0])
            sys.stdout.write(": ")
            sys.stdout.write(header[1])
            sys.stdout.write("\n")
        return write

    result = application(environ, start_response)

    try:
        for data in result:
            write(data)
    finally:
        if hasattr(result, 'close'):
            result.close()