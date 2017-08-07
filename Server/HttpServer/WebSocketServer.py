from Utils import int_as_hex, recvall_websocket
from NetworkExceptions import ConnectionAbruptlyClosedException
import time


def send_close_frame(connection, reason):
    payload = []
    payload.insert(0, '\x81')
    message_length = 2
    payload.insert(1, int_as_hex(message_length))
    payload.insert(2, int_as_hex((reason >> 8) & 255))
    payload.insert(3, int_as_hex(reason & 255))

    map(lambda frame: connection.sendall(frame), payload)


# I leave it hardcoded this way to be clear how the protocol works
def send_web_sock_message(connection, message):
    payload = []
    payload.insert(0, '\x81')  # 1000 0001 -> first 1 for FIN, 3 0's for RSV's and 0001 (0x01) for text
    message_length = len(message)

    if message_length <= 125:
        payload.insert(1, int_as_hex(message_length))
        payload.insert(2, message)
    elif 125 < message_length <= 65535:
        payload.insert(1, int_as_hex(126))
        payload.insert(2, int_as_hex((message_length >> 8) & 255))
        payload.insert(3, int_as_hex(message_length & 255))
        payload.insert(4, message)
    elif message_length > 65535:
        payload.insert(1, int_as_hex(127))
        payload.insert(2, int_as_hex((message_length >> 56) & 255))
        payload.insert(3, int_as_hex((message_length >> 48) & 255))
        payload.insert(4, int_as_hex((message_length >> 40) & 255))
        payload.insert(5, int_as_hex((message_length >> 32) & 255))
        payload.insert(6, int_as_hex((message_length >> 24) & 255))
        payload.insert(7, int_as_hex((message_length >> 16) & 255))
        payload.insert(8, int_as_hex((message_length >> 8) & 255))
        payload.insert(9, int_as_hex(message_length & 255))
        payload.insert(10, message)

    map(lambda frame: connection.sendall(frame), payload)


def recv_web_sock_message(connection, broker, address):
    closed = False
    try:
        while not closed:
            print "waiting for websocket message"
            payload_byte, payload_length, starting_position = recvall_websocket(connection, 4096)
            if len(payload_byte) != 0:
                data_type = ord(payload_byte[0])
                mask = payload_byte[starting_position:starting_position + 4]
                masked_message = payload_byte[starting_position + 4:]

                if data_type == 136:
                    print "!!CLOSING!!!"
                    closed = True
                    message = [ord(byte) ^ ord(mask[index % 4]) for index, byte in
                               enumerate(masked_message)]
                    if len(message) > 0:
                        first_byte = message[0] << 8
                        second_byte = message[1]
                        shutdown_reason = first_byte + second_byte
                        send_close_frame(connection, shutdown_reason)
                    else:
                        send_close_frame(connection, 1000)
                    connection.close()
                    broker.remove_connection(address)
                else:
                    message = [chr(ord(byte) ^ ord(mask[index % 4])) for index, byte in enumerate(masked_message)]
                    # print ''.join(message)
                    broker.add_message_to_queue(''.join(message))

            else:
                print "connection closed on other side!"
                shutdown_reason = 1000
                send_close_frame(connection, shutdown_reason)
                connection.close()
                closed = True
                broker.remove_connection(address)

    except ConnectionAbruptlyClosedException:
        print "Connection has abruptly closed while listening for message"
        connection.close()
        broker.remove_connection(address)
    except Exception:
        print "Exception in recv web sock message"
        raise
