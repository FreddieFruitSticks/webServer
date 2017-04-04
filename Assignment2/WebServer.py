import socket
from ThreadPool import ThreadPool
from tasks import task_get_file
from HttpMessageVerifier import get_operation
from NetworkExceptions import BadRequestException
from ResponseBuilder import build_error_response

HOST = ''
PORT = 50008

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)


def handle_request(message, conn, thread_pool):
    try:
        request_operation = get_operation(message)
        request_data = message.split("\n")
        request_header = request_data[0]
        file_name = request_header.split(" ")[1].split("/")[1]
        if request_operation == 'GET' or request_operation == 'HEAD':
            head_req = False if request_operation == 'GET' else True
            thread_pool.submit_task(task_get_file, {
                'connection': conn,
                'file_name': file_name,
                'user_agent': user_agent,
                'head_request': head_req
            })
    except BadRequestException as e:
        response_builder = build_error_response(400, e, user_agent)
        conn.send(response_builder.build())
        conn.close()


if __name__ == "__main__":
    thread_pool = ThreadPool(4)
    thread_pool.start()
    user_agent = None
    while True:
        try:
            conn, addr = sock.accept()
            message = conn.recv(1024)
            try:
                handle_request(message, conn, thread_pool)
            except Exception:
                response_builder = build_error_response(500, "Internal server error", user_agent)
                conn.send(response_builder.build())
                conn.close()
        except KeyboardInterrupt:
            raise
        finally:
            print "done"
