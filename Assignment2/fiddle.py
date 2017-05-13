from cStringIO import StringIO
import sys, os


# from simple_app import simple_app
def run_with_wsgi(application):
    environ = {}
    environ.update(os.environ)

    headers = []

    def write(data):
        sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status, headers):
        # Here loop through headers and send those to stdout
        for header in headers:
            sys.stdout.write(header[0])
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


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello from simple_app\n']


class Capturing(list):
    def __enter__(self):
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = sys.__stdout__


def printy():
    def printy2():
        sys.stdout.write("hi\n")
        sys.stdout.write("hi again")

    printy2()


with Capturing() as output:
    run_with_wsgi(simple_app)

print output
