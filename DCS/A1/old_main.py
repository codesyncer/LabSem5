import socket
import threading
from time import sleep
import sys

run = True
BSS = True


def m_sleep(t):
    sleep(t)
    return
    # try:
    #     sleep(t)
    # except KeyboardInterrupt:
    #     raise KeyboardInterrupt


def diff(vector, timestamp, from_id):
    if timestamp[from_id] - vector[from_id] != 1:
        return False
    for i in range(len(vector)):
        if i != from_id and timestamp[i] > vector[i]:
            return False
    return True


def accept(tup, vector):
    print(tup[0], 'RECV: ', tup[1])
    for i in range(len(vector)):
        vector[i] = max(tup[0][i], vector[i])


def receive(sock, vector):
    global run
    base_port = 3000
    n = len(vector)
    buffer = []
    while run:
        data, addr = sock.recvfrom(1024)
        if not run:
            break
        from_id = addr[1] - base_port
        data = str(data.decode())
        data = data.split(';', 1)
        if len(data) < 2:
            print('BAD MSG')
            continue
        timestamp, msg = [int(t) for t in data[0].split(',')], data[1]
        if len(timestamp) != n:
            print('BAD MSG')
            continue
        if not BSS:
            accept((timestamp, msg), vector)
            continue
        if not diff(vector, timestamp, from_id):
            buffer.append((timestamp, msg, from_id))
        else:
            accept((timestamp, msg), vector)
            for _ in range(n):
                j = 0
                while j < len(buffer):
                    if diff(vector, buffer[j][0], buffer[j][2]):
                        accept((buffer[j][0], buffer[j][1]), vector)
                        break
                    j += 1
                else:
                    break
                buffer = buffer[:j] + buffer[j + 1:]


def port(pid):
    base_port = 3000
    return base_port + pid


def send(real_msg, from_id, sock, vector):
    if from_id == 2:
        return
    vector[from_id] += 1
    msg = ','.join(str(pid) for pid in vector) + ';' + real_msg
    for pid in range(len(vector)):
        if pid != from_id:
            if from_id == 0 and pid == 2:
                m_sleep(10)
            sock.sendto(msg.encode(), ('localhost', port(pid)))
    print(vector, 'SENT:', real_msg)


def main():
    global run
    if len(sys.argv) < 3:
        return
    n = int(sys.argv[1])
    sid = int(sys.argv[2])
    vector = [0] * n
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 3000 + sid))
    receive_thread = threading.Thread(target=receive, args=[sock, vector])
    receive_thread.start()
    m_sleep(5)
    if sid == 1:
        m_sleep(5)
    try:
        while True:
            real_msg = 'MSG from %d' % sid
            send(real_msg, sid, sock, vector)
            m_sleep(1000)
    except KeyboardInterrupt:
        pass
    run = False
    sock.sendto(b'KILL', ('localhost', port(sid)))
    receive_thread.join()
    sock.close()


if __name__ == '__main__':
    main()
