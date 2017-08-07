import sys
from ContextManagers import CaptureOutput

sys.path.insert(0, '/home/freddie/IdeaProjects/networking/Assignment2/app')
sys.path.insert(0, '/home/freddie/IdeaProjects/networking/Assignment2/CGI')
from run_with_wsgi import run_with_wsgi
from simple_app import simple_app

from ResponseBuilder import ResponseBuilder


# TODO: redirect stdout is not threadsafe.
def wsgi_get(connection, headers, head_request, server_env_vars):
    with CaptureOutput() as output:
        run_with_wsgi(simple_app, server_env_vars)
    app_response = output[0]
    response = ResponseBuilder(200, "OK")
    response = response \
        .with_header({"key": "Content-length", "value": app_response.get('Content-length')}) \
        .with_header({"key": "Host", "value": app_response.get('Host')}) \
        .with_header({"key": "Date", "value": app_response.get('Date')}) \
        .with_header({"key": "Content-type", "value": app_response.get('Content-type')}) \
        .with_body({"body": app_response.get("body")}) \
        .build_response()
    connection.send(response)
