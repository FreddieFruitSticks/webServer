import os, sys


def configureCGIEnvVars(environ, server_env):
    updated_env = dict(environ.items() + server_env.get_env_vars().items())
    return updated_env


def run_with_wsgi(application, server_env):
    environ = {}
    environ.update(os.environ)
    environ = configureCGIEnvVars(environ, server_env)
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.error'] = sys.stderr
    environ['wsgi.multithread'] = True
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True

    # sys.__stdout__.write(str(environ.get('off')))

    headers_set = []

    def write(data):
        if not headers_set:
            raise AssertionError("You cant write body before setting headers")

        sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status, headers):
        sys.stdout.write("status_code: ")
        sys.stdout.write(status.split(" ")[0])
        sys.stdout.write("\n")

        sys.stdout.write("status_description: ")
        sys.stdout.write(status.split(" ")[1])
        sys.stdout.write("\n")

        for header in headers:
            sys.stdout.write(header[0])
            sys.stdout.write(": ")
            sys.stdout.write(header[1])
            sys.stdout.write("\n")

        headers_set[:] = [status, headers]
        return write

    result = application(environ, start_response)
    try:
        for data in result:
            write(data)
    finally:
        if hasattr(result, 'close'):
            result.close()
