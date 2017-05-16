class Header(object):
    def __init__(self, status_code, status_description):
        self.response = """HTTP/1.1 """
        self.response += str(status_code)+" "
        self.response += status_description+"\n"
        self.body = None

    def with_header(self, dic):
        header = """{key}: {value}\n""".format(**dic)
        self.response += header
        return self

    def with_body(self, dictionary):
        self.body = """\n{body} """.format(**dictionary)
        return self

    def build_response(self):
        if self.body is not None:
            self.response += self.body
        return self.response


header = Header(200, "OK")
response = header.with_header({'key': "Content-type", 'value': "text/plain"})\
    .with_header({'key': "Connection", 'value': "keep-alive"})\
    .with_body({"body": "HELLO WORLD"})\
    .build_response()

print response
