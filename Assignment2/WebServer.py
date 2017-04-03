import socket, os
from email.utils import formatdate
from ThreadPool import ThreadPool
from tasks import task_get_file
from HttpMessageVerifier import verify_message
from NetworkExceptions import BadRequestException
from ResponseBuilder import ResponseBuilder

HOST = ''
PORT = 50008

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)


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
            message = conn.recv(1024)
            try:
                verify_message(message)
            except BadRequestException:
                user_agent = None
                response = ResponseBuilder()
                response.with_date(formatdate(timeval=None, localtime=False, usegmt=True)) \
                    .with_status(400) \
                    .with_status_en("Bad Request") \
                    .with_content_type("text/html; charset=utf-8") \
                    .with_server("FredServer") \
                    .with_content_length(0) \
                    .with_user_agent(user_agent) \
                    .with_body(None)
                conn.send(response.build())

            file_name = get_file_name_from_header(message)
            thread_pool.submit_task(task_get_file, {
                'connection': conn,
                'file_name': file_name,
                'user_agent': 'Chat2/0.0.1'
            })
        except KeyboardInterrupt:
            raise
        except Exception:
            raise
        finally:
            print "done"
