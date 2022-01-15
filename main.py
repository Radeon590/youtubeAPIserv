import sys
import socket
import time
import os
from youtube_transcript_api import YouTubeTranscriptApi


def run_server(ip='192.168.0.101', port=4658):
    serv_socket = create_serv_socket(ip, port)
    name = serv_socket.getsockname()
    active_children = set()
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_socket, cid)
        child_pid = serve_client(client_sock, cid)
        active_children.add(child_pid)
        reap_child(active_children)
        cid += 1


#
def create_serv_socket(ip, port):
    serv_socket = socket.socket(socket.AF_INET,
                                socket.SOCK_STREAM,
                                proto=0)
    serv_socket.bind((ip, port))
    serv_socket.listen()
    return serv_socket


#
def accept_client_conn(serv_socket, cid):
    client_sock, client_addr = serv_socket.accept()
    return client_sock


#
def serve_client(client_sock, cid):
    child_pid = os.fork()
    # Parent request
    if child_pid:
        client_sock.close()
        return child_pid
    # Children request
    request = read_request(client_sock)
    if request is None:
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_responce(client_sock, response, cid)
    os._exit(0)


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
    return get_subs()#request[::-1]


def write_responce(client_sock, responce, cid):
    client_sock.sendall(responce)
    client_sock.close()
    print(f'Client #{cid} has been served')


#
def reap_child(active_children):
    for child_pid in active_children.copy():
        child_pid, _ = os.waitpid(child_pid, os.WNOHANG)
        if child_pid:
            active_children.discard(child_pid)


#
def get_subs():
    subs = YouTubeTranscriptApi.get_transcript("SW14tOda_kI")
    subs = str(subs) + '_'
    return bytearray(subs.encode())
#############################################
#hostname = socket.gethostname()
#IP = socket.gethostbyname(hostname)
#print(IP)
#
run_server()
