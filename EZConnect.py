# code from https://realpython.com/python-sockets/
# documentation https://docs.python.org/3/library/socket.html

import socket, json, time

class EZConnect:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.send_time = 0
        self.resp_time = 0

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        return self
  
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        self.s.close()
        return True

    def send(self, data):
        self.send_time = time.time() * 1000
        t = json.dumps(data)
        self.s.sendall(bytes(t,encoding="utf-8"))
        
    def get(self, size):
        t = json.loads(self.s.recv(size))
        self.resp_time = time.time() * 1000 - self.send_time
        return t

    def req(self, data):
        self.send(data)
        return (self.get(16384), self.resp_time)

if __name__ == '__main__':
    with EZConnect('localhost', 4398) as t:
        data, ping = t.req({
            'event': 'get_chunk',
            'coords': [0, 0]  
        })
        print(data, ping)