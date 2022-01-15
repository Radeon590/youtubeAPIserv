from youtube_transcript_api import YouTubeTranscriptApi

class server():

    def start(self):
        import socket

        serv_socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    proto=0)

        serv_socket.bind(('0.0.0.0', 4658))
        serv_socket.listen(10)

        print(serv_socket.getsockname())

        while True:
            client_sock, client_addr = serv_socket.accept()
            print('connected by: ', client_addr)

            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                client_sock.sendall(data)

            client_sock.close()