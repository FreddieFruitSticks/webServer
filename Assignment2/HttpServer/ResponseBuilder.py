from email.utils import formatdate


class ResponseBuilder(object):
    def __init__(self, status_code, status_description):
        self.response = """HTTP/1.1 """
        self.response += str(status_code) + " "
        self.response += status_description + "\n"
        self.body = None

    def with_header(self, dictionary):
        header = """{key}: {value}\n""".format(**dictionary)
        self.response += header
        return self

    def with_body(self, dictionary):
        self.body = """\n{body} """.format(**dictionary)
        return self

    def build_response(self):
        if self.body is not None:
            self.response += self.body
        return self.response


def build_generic_response(code, description, body=None):
    response = ResponseBuilder(code, description)
    response = response.with_header({"key": "Date", "value": formatdate(timeval=None, localtime=False, usegmt=True)}) \
        .with_header({"key": "Content-type", "value": "text/html; charset=utf-8"}) \
        .with_header({"key": "Host", "value": "FredServer"}) \
        .with_header({"key": "Content-length", "value": 0})\
        .with_body({"body": body})\
        .build_response()
    return response
