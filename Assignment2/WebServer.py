import socket
from ThreadPool import ThreadPool
from tasks import task_handle_get, task_handle_post_request, task_handle_put_request, task_handle_delete_request
from HttpMessageVerifier import parse_headers
from NetworkExceptions import BadRequestException, HttpVersionException
from ResponseBuilder import build_generic_response

HOST = ''
PORT = 50008

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)


# TODO: Think about putting this in the thread that it calls.
def handle_request(message, conn, thread_pool):
    try:
        headers = parse_headers(message)
        request_operation = headers['request_operation']
        message_body = get_message_body(message)

        if request_operation == 'GET' or request_operation == 'HEAD':
            head_req = False if request_operation == 'GET' else True
            thread_pool.submit_task(task_handle_get, {
                'connection': conn,
                'headers': headers,
                'head_request': head_req
            })
        elif request_operation == 'POST':
            message_body = get_message_body(message)
            thread_pool.submit_task(task_handle_post_request, {
                'message_body': message_body,
                'connection': conn,
                'headers': headers
            })
        elif request_operation == 'PUT':
            thread_pool.submit_task(task_handle_put_request, {
                'message_body': message_body,
                'connection': conn,
                'headers': headers
            })
        elif request_operation == 'DELETE':
            thread_pool.submit_task(task_handle_delete_request, {
                'connection': conn,
                'headers': headers
            })
    except HttpVersionException as e:
        response_builder = build_generic_response(505, e)
        conn.send(response_builder.build())
        conn.close()
    except BadRequestException as e:
        response_builder = build_generic_response(400, e)
        conn.send(response_builder.build())
        conn.close()


def get_message_body(message):
    broken_up = message.split('\r\n')
    return broken_up[len(broken_up) - 1]


if __name__ == "__main__":
    thread_pool = ThreadPool(4)
    thread_pool.start()
    while True:
        try:
            conn, addr = sock.accept()
            fullMessage = ''
            message = conn.recv(1024)
            while len(message) == 1024:
                fullMessage += message
                message = conn.recv(1024)
            fullMessage += message

            print "fullMessage ", fullMessage
            try:
                handle_request(fullMessage, conn, thread_pool)
            except Exception as e:
                response_builder = build_generic_response(500, "Internal server error")
                conn.send(response_builder.build())
                conn.close()
                print e
        except KeyboardInterrupt:
            raise
        finally:
            pass
