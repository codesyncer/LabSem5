import socket
import threading
import sys
from time import sleep


class Com:
    base_port = 3000
    read_size = 1024
    time_port = 5000

    def __init__(self, n, pid, cb):
        self.pid = pid
        self.n = n
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = threading.Thread(target=self.receive)
        self.queue = []
        self.run = True
        self.cb = cb
        self.in_cs = False

    def init(self):
        self.sock.bind(('localhost', Com.base_port + self.pid))
        self.receive_thread.start()

    def finalize(self):
        self.run = False
        self.sock.sendto(b'KILL', ('localhost', Com.get_port(self.pid)))
        self.receive_thread.join()
        self.sock.close()

    def sleepy_send(self, delay, to_pid, enc):
        sleep(delay)
        self.sock.sendto(enc, ('localhost', Com.get_port(to_pid)))

    def broadcast(self, msg, delay_send=None):
        enc = msg.encode()
        for pid in range(self.n):
            if pid != self.pid:
                if delay_send is None:
                    self.sock.sendto(enc, ('localhost', Com.get_port(pid)))
                else:
                    threading.Thread(target=self.sleepy_send, args=(delay_send[pid], pid, enc)).start()

    def receive(self):
        reply_count = 0
        while self.run:
            data, address = self.sock.recvfrom(Com.read_size)
            if not self.run:
                break
            from_pid = Com.get_pid(address)
            data = str(data.decode()).split(';')
            time = int(data[1])
            if data[0] == 'REQ':
                self.queue.append((time, from_pid))
                self.queue.sort(key=lambda tup: tup[0])
                msg = 'REP;' + data[1]
                self.sock.sendto(msg.encode(), ('localhost', Com.get_port(from_pid)))
            elif data[0] == 'REP':
                reply_count += 1
            elif data[0] == 'REL':
                self.queue.pop(0)
            if reply_count == self.n - 1 and len(self.queue) != 0 and self.queue[0][1] == self.pid:
                self.cb()
                print('Released')
                self.queue.pop(0)
                self.broadcast('REL')
                reply_count = 0

    def get_lock(self, delay_send=None):
        print('Requesting lock')
        time = Com.get_time()
        request = 'REQ;' + str(time)
        self.broadcast(request, delay_send)
        self.queue.append((time, self.pid))

    @staticmethod
    def get_port(pid):
        return Com.base_port + pid

    @staticmethod
    def get_pid(address):
        return address[1] - Com.base_port

    @staticmethod
    def get_time():
        sock = socket.socket()
        sock.connect(('localhost', Com.time_port))
        msg = sock.recv(8)
        sock.close()
        return int(msg)


def main():
    n, pid = int(sys.argv[1]), int(sys.argv[2])

    def use_cs():
        print('Got lock')
        print('Using CS')
        sleep(10)
        print('Releasing lock')

    com = Com(n, pid, use_cs)
    com.init()
    try:
        if pid == 0:
            sleep(10)
            com.get_lock([0, 2, 15])
        if pid == 1:
            pass
        if pid == 2:
            sleep(5)
            com.get_lock([15, 10, 0])
        input()
    except KeyboardInterrupt:
        pass
    com.finalize()


if __name__ == '__main__':
    main()
