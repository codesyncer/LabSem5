import socket
import threading
import sys
from time import sleep


class Com:
    base_port = 3000
    read_size = 1024

    def __init__(self, n, pid, callback):
        self.pid = pid
        self.n = n
        self.vector = [0] * n
        self.V_P = [None] * n
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = threading.Thread(target=self.recv)
        self.buffer = []
        self.run = True
        self.active_ses = True
        self.callback = callback

    def init(self):
        self.sock.bind(('localhost', Com.base_port + self.pid))
        self.receive_thread.start()

    def finalize(self):
        self.run = False
        self.sock.sendto(b'KILL', ('localhost', Com.get_port(self.pid)))
        self.receive_thread.join()
        self.sock.close()

    def send(self, to_pid, user_msg):
        self.vector[self.pid] += 1
        msg = ''
        for stamp in self.V_P:
            if stamp is not None:
                msg += ','.join(str(t) for t in stamp)
            msg += ';'
        msg += ','.join(str(pid) for pid in self.vector) + ';' + user_msg
        self.V_P[to_pid] = list(self.vector)
        self.sock.sendto(msg.encode(), ('localhost', Com.get_port(to_pid)))

    def gt(self, t1, t2):
        return True

    def lt(self, t1, t2):
        return True

    def deliver(self, v_m, stamp, user_msg, from_pid):
        for i in range(self.n):
            if i != self.pid and v_m[i] is not None:
                if self.V_P[i] is None:
                    self.V_P[i] = list(v_m[i])
                else:
                    self.V_P[i] = [max(t1, t2) for t1, t2 in zip(self.V_P[i], v_m[i])]
        for i in range(self.n):
            self.vector[i] = max(stamp[i], self.vector[i])
        self.vector[self.pid] += 1
        self.callback(user_msg, stamp)

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
            self.deliver(v_m, timestamp, msg, from_pid)
            return True
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

    com = Com(n, pid, cb)
    com.init()
    try:
        while True:
            com.send(input())
    except KeyboardInterrupt:
        pass
    com.finalize()


def main1():
    # 3 processes,
    n, pid = int(sys.argv[1]), int(sys.argv[2])

    def cb(msg, timestamp):
        print(timestamp, msg)

    com = Com(n, pid, cb)
    com.init()
    try:
        if pid == 0:
            sleep(5)
            print('SENT: MSG from P0')
            com.send('MSG from P0', [0, 5, 15])
        if pid == 1:
            sleep(5)
            sleep(10)
            print('SENT: MSG from P1')
            com.send('MSG from P1')
        if pid == 2:
            sleep(5)
            sleep(20)
            print('SENT: MSG from P2')
            com.send('MSG from P2')
    except KeyboardInterrupt:
        pass
    sleep(10)
    com.finalize()


if __name__ == '__main__':
    main1()
