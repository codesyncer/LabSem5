import socket

time_port = 5000
read_size = 1024
time = 0


def main():
    global time
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', time_port))
    sock.listen(5)
    try:
        while True:
            client, address = sock.accept()
            msg = str(time)
            time += 1
            client.send(msg.encode())
            client.close()
    except KeyboardInterrupt:
        pass
    sock.close()


if __name__ == '__main__':
    main()
