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


def diff(vector, timestamp):
    m_count = 0
    for i in range(len(vector)):
        m_count += max(0, timestamp[i] - vector[i])
    return m_count


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
        m_count = diff(vector, timestamp)
        if m_count != 1:
            buffer.append((timestamp, msg))
        else:
            accept((timestamp, msg), vector)
            for _ in range(n):
                for j in range(len(buffer)):
                    if diff(vector, buffer[j][0]) == 1:
                        accept(buffer[j], vector)
                        buffer = buffer[:j] + buffer[j + 1:]
                        break
                else:
                    break


def port(pid):
    base_port = 3000
    return base_port + pid


def send(real_msg, from_id, sock, vector):
    if from_id == 2:
        return
    vector[from_id] += 1
    msg = ','.join(str(pid) for pid in vector) + ';' + real_msg
    if from_id == 1:
        m_sleep(5)
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
    try:
        while True:
            real_msg = 'MSG from %d' % sid
            send(real_msg, sid, sock, vector)
            m_sleep(1)
    except KeyboardInterrupt:
        pass
    run = False
    sock.sendto(b'KILL', ('localhost', port(sid)))
    receive_thread.join()
    sock.close()


if __name__ == '__main__':
    main()
