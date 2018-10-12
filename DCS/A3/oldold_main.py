import socket
import threading
import sys
from time import sleep


class Com:
    base_port = 3000
    read_size = 1024

    def __init__(self, n, pid, cb):
        self.pid = pid
        self.n = n
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = threading.Thread(target=self.receive)
        self.Q = [('REL', 0) for _ in range(self.n)]
        self.queue = []
        self.run = True
        self.cb = cb
        self.time = 0

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

    def take_cs(self):
        self.cb()
        self.exit_cs()

    def receive(self):
        reply_count = 0
        while self.run:
            data, address = self.sock.recvfrom(Com.read_size)
            if not self.run:
                break
            from_pid = Com.get_pid(address)
            data = str(data.decode()).split(';')
            time = int(data[1])
            self.time = max(self.time, time) + 1
            if data[0] == 'REQ':
                self.queue.append((from_pid, time))
                self.queue.sort(key=lambda tup: tup[1])
                self.Q[from_pid] = (data[0], time)
                msg = 'REP;' + str(self.time)
                self.sock.sendto(msg.encode(), ('localhost', Com.get_port(from_pid)))
            elif data[0] == 'REP':
                reply_count += 1
                if self.Q[from_pid] != 'REQ':
                    self.Q[from_pid] = (data[0], time)
            elif data[0] == 'REL':
                self.Q[from_pid] = (data[0], time)
                i = 0
                while i < len(self.queue):
                    if self.queue[i][0] == from_pid:
                        break
                    i += 1
                self.queue.pop(i)
            if data[0] in ['REP', 'REL']:
                if reply_count == self.n - 1:
                    reply_count = 0

            # if data[0] in ['REP', 'REL']:
            #     for i in range(self.n):
            #         if i != self.pid:
            #             if self.Q[i][1] <= self.Q[self.pid][1]:
            #                 break
            #     else:
            #         threading.Thread(target=self.take_cs).start()

    def enter_cs(self, delay_send=None):
        print('Requesting lock')
        self.time += 1
        request = 'REQ;' + str(self.time)
        self.broadcast(request, delay_send)
        self.Q[self.pid] = ('REQ', self.time)
        self.queue.append((self.pid, self.time))

    def exit_cs(self):
        print('Released lock')
        self.time += 1
        release = 'REL;' + str(self.time)
        self.broadcast(release)
        self.Q[self.pid] = ('REL', self.time)
        i = 0
        while i < len(self.queue):
            if self.queue[i][0] == self.pid:
                break
            i += 1
        self.queue.pop(i)

    @staticmethod
    def get_port(pid):
        return Com.base_port + pid

    @staticmethod
    def get_pid(address):
        return address[1] - Com.base_port


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
            com.enter_cs([0, 2, 15])
        if pid == 1:
            pass
        if pid == 2:
            sleep(5)
            com.enter_cs([15, 10, 0])
        input()
    except KeyboardInterrupt:
        pass
    com.finalize()


if __name__ == '__main__':
    main()
