class ResponseBuilder(object):
    response_header = """
HTTP/1.1 `{status}` `{status_en}`\r\nDate: `{date}`\nServer: FreddiesServer/0.0.1\nUser-Agent: '{user_agent}'\nContent-length:'{content_length}'\nContent-Type:text/html; charset=utf-8

'{body}'"""

    response = """
HTTP/1.1"""

    def with_status(self, status):
        self.response += " " + status
        return self

    def with_status_en(self, status_en):
        self.response += " " + status_en + '\r\n'
        return self

    def with_date(self, date):
        self.response += "Date: " + date + '\r\n'
        return self

    def with_server(self, server):
        self.response += "Server: " + server + '\r\n'
        return self

    def with_user_agent(self, user_agent):
        self.response += "Server: " + user_agent + '\r\n'
        return self

    def with_content_type(self, type):
        self.response += "Content-Type: " + type + '\r\n'
        return self

    def with_body(self, body):
        self.response += "Content-length: " + len(body) + '\r\n\r\n'
        self.response += body
        return self

    def build(self):
        return self.response
