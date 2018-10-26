import socket
import threading
from multiprocessing import Process
import sys
from time import sleep


class Com:
    base_port = 3000
    read_size = 1024
    time_port = 5000
    quorum_members = [[0, 1], [0, 1, 2], [1, 2]]

    def __init__(self, n, pid, cb):
        self.pid = pid
        self.n = n
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_thread = threading.Thread(target=self.receive)
        self.queue = []
        self.run = True
        self.cb = cb
        self.have_voted = False
        self.have_inquired = False
        self.candidate = None
        self.time = 0
        self.reply_count = 0
        self.callback_thread = None

    def init(self):
        self.time = self.pid
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
        for pid in Com.quorum_members[self.pid]:
            if pid != self.pid:
                if delay_send is None:
                    self.sock.sendto(enc, ('localhost', Com.get_port(pid)))
                else:
                    threading.Thread(target=self.sleepy_send, args=(delay_send[pid], pid, enc)).start()

    def foo(self):
        self.reply_count = 0
        self.cb()
        self.time += 1
        time = Com.get_time()
        msg = 'RELEASE;' + str(time)
        self.broadcast(msg)
        print('Released lock')

    def receive(self):
        self.reply_count = 0
        while self.run:
            data, address = self.sock.recvfrom(Com.read_size)
            if not self.run:
                break
            from_pid = Com.get_pid(address)
            data = str(data.decode()).split(';')
            req_time = int(data[1])
            self.time = max(self.time, req_time) + 1
            if data[0] == 'REPLY':
                self.reply_count += 1
            elif data[0] == 'INQUIRE':
                print('--- Lost Lock ---')
                self.callback_thread.terminate()
                self.reply_count -= 1
                self.time += 1
                time = Com.get_time()
                msg = 'RELINQUISH;' + str(time)
                self.sock.sendto(msg.encode(), ('localhost', Com.get_port(from_pid)))
            elif data[0] == 'REQUEST':
                if self.have_voted:
                    self.queue.append((from_pid, req_time))
                    if req_time < self.candidate[1] and (not self.have_inquired):
                        msg = 'INQUIRE;' + str(self.candidate[1])
                        self.sock.sendto(msg.encode(), ('localhost', Com.get_port(self.candidate[0])))
                        self.have_inquired = True
                else:
                    self.have_voted = True
                    self.candidate = (from_pid, req_time)
                    time = Com.get_time()
                    msg = 'REPLY;' + str(time)
                    self.sock.sendto(msg.encode(), ('localhost', Com.get_port(from_pid)))
            elif data[0] == 'RELINQUISH':
                self.queue.append(self.candidate)
                new_candidate = min(self.queue, key=lambda tup: tup[1])
                self.queue.pop(self.queue.index(new_candidate))
                self.candidate = new_candidate
                self.have_inquired = False
                time = Com.get_time()
                msg = 'REPLY;' + str(time)
                self.sock.sendto(msg.encode(), ('localhost', Com.get_port(new_candidate[0])))
            elif data[0] == 'RELEASE':
                if len(self.queue) != 0:
                    new_candidate = min(self.queue, key=lambda tup: tup[1])
                    self.queue.pop(self.queue.index(new_candidate))
                    self.candidate = new_candidate
                    time = Com.get_time()
                    msg = 'REPLY;' + str(time)
                    self.sock.sendto(msg.encode(), ('localhost', Com.get_port(new_candidate[0])))
                else:
                    self.have_voted = False
                self.have_inquired = False
            if self.reply_count == (len(Com.quorum_members[self.pid]) - 1):
                self.callback_thread = Process(target=self.foo)
                self.callback_thread.start()
            # print(self.queue)

    def lock(self, delay_send=None):
        self.time += 1
        time = Com.get_time()
        request = 'REQUEST;' + str(time)
        self.broadcast(request, delay_send)
        print('Requested lock')

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
        print('Locked')
        print('Using CS')
        sleep(20)
        print('Unlocked')

    com = Com(n, pid, use_cs)
    com.init()
    # try:
    #     if pid == 0:
    #         sleep(5)
    #         com.lock([0, 5, 0])
    #     if pid == 1:
    #         pass
    #     if pid == 2:
    #         sleep(7)
    #         com.lock([0, 8, 0])
    try:
        if pid == 0:
            sleep(5)
            com.lock([0, 10, 0])
        if pid == 1:
            pass
        if pid == 2:
            sleep(10)
            com.lock([0, 0, 0])

        input()
    except KeyboardInterrupt:
        pass
    com.finalize()


if __name__ == '__main__':
    main()
