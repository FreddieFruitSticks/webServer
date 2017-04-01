import socket
from ThreadPool import ThreadPool
from tasks import task_get_file
from HttpMessageVerifier import verify_message
from NetworkExceptions import BadRequestException

HOST = ''
PORT = 50008

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

response_header = """
HTTP/1.1 `{status}` OK\r\nDate: `{date}`\nServer: FreddiesServer/0.0.1\nUser-Agent: '{user_agent}'\nContent-length:'{content_length}'\nContent-Type:text/html; charset=utf-8

'{body}'"""


def get_file_name_from_header(message):
    print message
    request_data = message.split("\n")
    request_header = request_data[0]
    return request_header.split(" ")[1].split("/")[1]


if __name__ == "__main__":
    thread_pool = ThreadPool(4)
    thread_pool.start()
    while True:
        try:
            conn, addr = sock.accept()
            print "accepting connection"
            message = conn.recv(1024)
            verify_message(message)
            file_name = get_file_name_from_header(message)
            thread_pool.submit_task(task_get_file, {
                'connection': conn,
                'file_name': file_name,
                'user_agent': 'Chat2/0.0.1',
                'response_header': response_header,
            })
        except KeyboardInterrupt:
            raise
        except BadRequestException:
            print "asdasdasdasdasd"
        except Exception:
            raise
        finally:
            print "done"
