import sys
import socket
import time


def run_server(port=4658):
    serv_socket = create_serv_socket(port)
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_socket, cid)
        serve_client(client_sock, cid)
        cid += 1


#
def create_serv_socket(port):
    serv_socket = socket.socket(socket.AF_INET,
                                socket.SOCK_STREAM,
                                proto=0)
    serv_socket.bind(('', port))
    serv_socket.listen()
    return serv_socket


#
def accept_client_conn(serv_socket, cid):
    client_sock, client_addr = serv_socket.accept()
    print(f'Client #{cid} connected '
          f'{client_addr[0]}:{client_addr[1]}')
    return client_sock


#
def serve_client(client_sock, cid):
    request = read_request(client_sock)
    if (request is None):
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        responce = handle_request(request)
        write_responce(client_sock, responce, cid)


#
def read_request(client_sock, delimiter=b'!'):
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(4)
            if not chunk:
                return None

            request += chunk
            if delimiter in chunk:
                return request

    except ConnectionResetError:
        return None
    except:
        raise


#
def handle_request(request):
    time.sleep(5)
    return request[::-1]


def write_responce(client_sock, responce, cid):
    client_sock.sandall(responce)
    client_sock.close()
    print(f'Client #{cid} has been served')
