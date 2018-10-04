import socket
import threading
import sys
from time import sleep


class Com:
    base_port = 3000
    read_size = 1024

    def __init__(self, n, pid, recv_cb=None, send_cb=None):
        self.pid = pid
        self.n = n
        self.vector = [0] * n
        self.V_P = [None] * n
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = threading.Thread(target=self.recv)
        self.buffer = []
        self.run = True
        self.active_ses = True
        self.send_cb = send_cb
        self.recv_cb = recv_cb

    def init(self):
        self.sock.bind(('localhost', Com.base_port + self.pid))
        self.receive_thread.start()

    def finalize(self):
        self.run = False
        self.sock.sendto(b'KILL', ('localhost', Com.get_port(self.pid)))
        self.receive_thread.join()
        self.sock.close()

    def sleepy_send(self, delay, to_pid, msg):
        sleep(delay)
        self.sock.sendto(msg.encode(), ('localhost', Com.get_port(to_pid)))

    def send(self, to_pid, user_msg, delay_send=None):
        self.vector[self.pid] += 1
        msg = ''
        for stamp in self.V_P:
            if stamp is not None:
                msg += ','.join(str(t) for t in stamp)
            msg += ';'
        msg += ','.join(str(pid) for pid in self.vector) + ';' + user_msg
        self.V_P[to_pid] = list(self.vector)
        if delay_send is None:
            self.sock.sendto(msg.encode(), ('localhost', Com.get_port(to_pid)))
        else:
            threading.Thread(target=self.sleepy_send, args=(delay_send, to_pid, msg)).start()
        if self.send_cb is not None:
            self.send_cb(user_msg, self.vector)

    def gt(self, t1, t2):
        flag = False
        for t1i, t2i in zip(t1, t2):
            if t1i < t2i:
                return False
            flag = flag or t1i > t2i
        return flag

    def deliver(self, v_m, stamp, user_msg):
        for i in range(self.n):
            if i != self.pid and v_m[i] is not None:
                if self.V_P[i] is None:
                    self.V_P[i] = list(v_m[i])
                else:
                    self.V_P[i] = [max(t1, t2) for t1, t2 in zip(self.V_P[i], v_m[i])]
        self.vector[self.pid] += 1
        for i in range(self.n):
            self.vector[i] = max(stamp[i], self.vector[i])
        if self.recv_cb is not None:
            self.recv_cb(user_msg, self.vector)

    def on_recv(self, from_pid, data_str):
        data = data_str.split(';')
        v_m_str, timestamp, msg = data[:-2], [int(t) for t in data[-2].split(',')], data[-1]
        v_m = []
        for stamp in v_m_str:
            if len(stamp) != 0:
                v_m.append([int(t) for t in stamp.split(',')])
            else:
                v_m.append(None)
        if not self.active_ses or v_m[self.pid] is None or not self.gt(v_m[self.pid], self.vector):
            self.deliver(v_m, timestamp, msg)
            return True
        print(timestamp, msg, '(buffered)')
        return False

    def recv(self):
        while self.run:
            data, address = self.sock.recvfrom(Com.read_size)
            if not self.run:
                break
            from_pid = Com.get_pid(address)
            data_str = str(data.decode())
            if self.on_recv(from_pid, data_str):
                while True:
                    j = 0
                    while j < len(self.buffer):
                        if self.on_recv(self.buffer[j][0], self.buffer[j][1]):
                            break
                        j += 1
                    else:
                        break
                    self.buffer = self.buffer[:j] + self.buffer[j + 1:]
            else:
                self.buffer.append((from_pid, data_str))

    @staticmethod
    def get_port(pid):
        return Com.base_port + pid

    @staticmethod
    def get_pid(address):
        return address[1] - Com.base_port


def main():
    n, pid = int(sys.argv[1]), int(sys.argv[2])

    def cb(msg, timestamp):
        print(timestamp, msg)

    def cb1(msg, timestamp):
        print(timestamp, msg, '(sent)')

    com = Com(n, pid, cb, cb1)
    com.init()
    try:
        while True:
            pid, msg = tuple(input().split(':'))
            com.send(int(pid), msg)
    except KeyboardInterrupt:
        pass
    com.finalize()


def main1():
    n, pid = int(sys.argv[1]), int(sys.argv[2])
    print('P%d' % pid)

    def cb(msg, timestamp):
        print(timestamp, msg)

    def cb1(msg, timestamp):
        print(timestamp, msg, '(sent)')

    com = Com(n, pid, cb, cb1)
    com.init()
    try:
        if pid == 0:
            pass
        if pid == 1:
            sleep(20)
            com.send(0, 'MSG from P1', 5)
        if pid == 2:
            sleep(5)
            com.send(0, 'MSG from P2', 25)
            sleep(5)
            com.send(1, 'MSG from P2', 5)
        input()
    except KeyboardInterrupt:
        pass
    com.finalize()


def main2():
    n, pid = int(sys.argv[1]), int(sys.argv[2])
    print('P%d' % pid)

    def cb(msg, timestamp):
        print(timestamp, msg)

    def cb1(msg, timestamp):
        print(timestamp, msg + ' (sent)')

    com = Com(n, pid, cb, cb1)
    com.init()
    try:
        if pid == 0:
            sleep(5)
            com.send(1, 'MSG from P0', 25)
            sleep(5)
            com.send(2, 'MSG from P0', 5)
        if pid == 1:
            pass
        if pid == 2:
            sleep(20)
            com.send(1, 'MSG from P2', 5)
        input()
    except KeyboardInterrupt:
        pass
    com.finalize()


def main3():
    n, pid = int(sys.argv[1]), int(sys.argv[2])
    print('P%d' % pid)

    def cb(msg, timestamp):
        print(timestamp, msg)

    def cb1(msg, timestamp):
        print(timestamp, msg + ' (sent)')

    com = Com(n, pid, cb, cb1)
    com.init()
    try:
        if pid == 0:
            sleep(40)
            com.send(2, 'MSG from P0', 5)
        if pid == 1:
            sleep(20)
            com.send(2, 'MSG from P1', 30)
            sleep(5)
            com.send(0, 'MSG from P1', 5)
        if pid == 2:
            sleep(5)
            com.send(0, 'MSG from P2', 30)
            sleep(5)
            com.send(1, 'MSG from P2', 5)
        input()
    except KeyboardInterrupt:
        pass
    com.finalize()


if __name__ == '__main__':
    main3()
