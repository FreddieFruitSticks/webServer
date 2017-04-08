from email.utils import formatdate


class ResponseBuilder(object):
    response_data = {}

    response_header = """
HTTP/1.1 {status} {status_en}\r\nDate: {date}\nServer: {server}\nUser-Agent: {user_agent}\nContent-length:{content_length}\nContent-Type:{content_type}\n

{body}"""

    def with_status(self, status):
        self.response_data.update({"status": status})
        return self

    def with_status_en(self, status_en):
        self.response_data.update({"status_en": status_en})
        return self

    def with_date(self, date):
        self.response_data.update({"date": date})
        return self

    def with_server(self, server):
        self.response_data.update({"server": server})
        return self

    def with_user_agent(self, user_agent):
        self.response_data.update({"user_agent": user_agent})
        return self

    def with_content_type(self, type):
        self.response_data.update({"content_type": type})
        return self

    def with_content_length(self, length):
        self.response_data.update({"content_length": length})
        return self

    def with_body(self, body):
        self.response_data.update({"body": body})
        return self

    def build(self):
        return self.response_header.format(**self.response_data)


def build_generic_response(code, message, agent):
    response = ResponseBuilder()
    response.with_date(formatdate(timeval=None, localtime=False, usegmt=True)) \
        .with_status(code) \
        .with_status_en(message) \
        .with_content_type("text/html; charset=utf-8") \
        .with_server("FredServer") \
        .with_content_length(0) \
        .with_user_agent(agent) \
        .with_body(None)
    return response
