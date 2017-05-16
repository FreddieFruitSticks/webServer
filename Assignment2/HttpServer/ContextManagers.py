from cStringIO import StringIO
import sys


class CaptureOutput(dict):
    def parse_headers_to_dict(self, message_split):
        dict = {}
        for header in message_split[0:len(message_split) - 1]:
            split_up = header.split(": ")
            dict[split_up[0]] = split_up[1]
        return dict

    def __enter__(self):
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        headers_dict = self.parse_headers_to_dict(self._stringio.getvalue().splitlines())
        self.update(headers_dict)
        self._stringio.close()
        del self._stringio
        sys.stdout = sys.__stdout__
