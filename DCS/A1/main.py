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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = threading.Thread(target=self.recv)
        self.buffer = []
        self.run = True
        self.active_bss = True
        self.callback = callback

    def init(self):
        self.sock.bind(('localhost', Com.base_port + self.pid))
        self.receive_thread.start()

    def finalize(self):
        self.run = False
        self.sock.sendto(b'KILL', ('localhost', Com.get_port(self.pid)))
        self.receive_thread.join()
        self.sock.close()

    def broadcast(self, user_msg, sleeps=None):
        self.vector[self.pid] += 1
        msg = ','.join(str(pid) for pid in self.vector) + ';' + user_msg
        for pid in range(self.n):
            if pid != self.pid:
                if sleeps:
                    sleep(sleeps[pid])
                self.sock.sendto(msg.encode(), ('localhost', Com.get_port(pid)))

    def test_accept(self, timestamp, from_pid):
        if timestamp[from_pid] - self.vector[from_pid] != 1:
            return False
        for i in range(len(self.vector)):
            if i != from_pid and timestamp[i] > self.vector[i]:
                return False
        return True

    def recv(self):
        def deliver(vector, stamp, user_msg):
            for i in range(len(vector)):
                vector[i] = max(stamp[i], vector[i])
            self.callback(user_msg, stamp)

        while self.run:
            data, address = self.sock.recvfrom(Com.read_size)
            if not self.run:
                break
            from_pid = Com.get_pid(address)
            data = str(data.decode())
            data = data.split(';', 1)
            timestamp, msg = [int(t) for t in data[0].split(',')], data[1]
            if not self.active_bss:
                deliver(self.vector, timestamp, msg)
                continue
            if not self.test_accept(timestamp, from_pid):
                self.buffer.append((timestamp, msg, from_pid))
            else:
                deliver(self.vector, timestamp, msg)
                while True:
                    j = 0
                    while j < len(self.buffer):
                        if self.test_accept(self.buffer[j][0], self.buffer[j][2]):
                            deliver(self.vector, self.buffer[j][0], self.buffer[j][1])
                            break
                        j += 1
                    else:
                        break
                    self.buffer = self.buffer[:j] + self.buffer[j + 1:]

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
            com.broadcast(input())
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
            com.broadcast('MSG from P0', [0, 5, 15])
        if pid == 1:
            sleep(5)
            sleep(10)
            print('SENT: MSG from P1')
            com.broadcast('MSG from P1')
        if pid == 2:
            sleep(5)
            sleep(20)
            print('SENT: MSG from P2')
            com.broadcast('MSG from P2')
    except KeyboardInterrupt:
        pass
    sleep(10)
    com.finalize()


if __name__ == '__main__':
    main1()
