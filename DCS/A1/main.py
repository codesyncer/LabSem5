import socket
import threading
from time import sleep
import sys

run = True


def receive(sock, vector):
    global run
    buffer = []
    while run:
        data, _ = sock.recvfrom(1024)
        if not run:
            break
        data = str(data.decode())
        data = data.split(';', 1)
        if len(data) < 2:
            print('BAD MSG')
            continue
        timestamp, msg = data[0], data[1]
        timestamp = [int(t) for t in timestamp.split(',')]
        print(timestamp)
        for i in range(len(vector)):
            vector[i] = max(timestamp[i], vector[i])
        print('RECV: ', msg)


def port(id):
    base_port = 3000
    return base_port + id


def main():
    global run
    n = 5
    vector = [0] * n
    if len(sys.argv) < 2:
        print('PID missing')
        return
    id = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 3000 + id))
    receive_thread = threading.Thread(target=receive, args=[sock, vector])
    receive_thread.start()
    try:
        while True:
            real_msg = 'MSG from %d' % id
            vector[id] += 1
            msg = ','.join(str(pid) for pid in vector) + ';' + real_msg
            for pid in range(n):
                if pid != id:
                    sock.sendto(msg.encode(), ('localhost', port(pid)))
            print(vector)
            print('SENT: ' + real_msg)
            sleep(3)
    except KeyboardInterrupt:
        pass
    run = False
    sock.sendto(b'KILL', ('localhost', port(id)))
    receive_thread.join()
    sock.close()


if __name__ == '__main__':
    main()
