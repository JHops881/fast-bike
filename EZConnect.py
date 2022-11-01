# code from https://realpython.com/python-sockets/
# documentation https://docs.python.org/3/library/socket.html

import socket, json, time

class EZConnect:

    events: dict = {
        'get_chunk': ['uuid', 'pos'],
        'login' : ['user', 'pass'],
        'logout' : ['uuid']
    }

    def __init__(self, host: str = "localhost", port: int = "8080"):
        """
        Do not call this constructor. Instead do the following:
        
        ```
        with EZConnect(host, port) as conn:
            # code
        ```
        
        - `host` the ip of the host server to connect to (deafult localhost)  
        - `port` the port number (default 8080)
        """

        assert port > 0, "Port must be positive integer"
        assert host != None, "Host must not be null"

        self.host = host
        self.port = port
        self.send_time = 0
        self.resp_time = 0

    def __enter__(self):
        """
        Establishes connection with the `host:port`
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        return self
  
    def __exit__(self, exc_type, exc_value, tb):
        """
        Closes the connection to `host:port`
        """
        if exc_type is not None:
            print(exc_type, exc_value, tb)
            return False
        self.s.close()
        return True

    def send(self, data: dict) -> bool:
        """
        Send a packet of JSON to `host:port`.

        This methods records it's start time in milliseconds in `self.send_time`

        - `data` the data to send as a JSON parsable object. It must contain the key `'event'` with a valid event name. Valid event names are in `self.events`.

        returns  `True` if the data was sent, `False` otherwise.
        """

        assert data != None, "Data cannot be None"
        assert data['event'] != None, "Must specify an event"
        assert data['event'] in self.events.keys(), data['event'] + " is not a valid event"

        self.send_time = time.time() * 1000

        try:
            t = json.dumps(data)
        except (TypeError, OverflowError):
            print(data, 'is not serializable')
            return False

        try:
            self.s.sendall(bytes(t,encoding="utf-8"))
        except Exception:
            print(t, "couldn't be sent to", self.host + ":" + self.port)
            return False

        return True
        
    def get(self, size: int = 16384) -> dict:
        """
        Wait for a packet from `host:port`

        Synchronously waits for data from the connection. If no data is received, this call will softlock. Also, this function records the time delta since the last `this.send()` call into the field `self.resp_time`.

        - `size` the maximum size in bytes to take from the receiving buffer. 
        
        returns the data recieved from the connection as a parsed json
        """
        t = json.loads(self.s.recv(size))
        self.resp_time = time.time() * 1000 - self.send_time
        return t

    def req(self, data: dict) -> dict:
        """
        Sends data to `host:port` and waits for a response.

        This function calls `this.send()` and `this.get()` under the hood. See them for further details.

        - `data` the data to send as a JSON parsable object. It must contain the key `'event'` with a valid event name. Valid event names are in `self.events`.

        if the data was sent, returns the data recieved from the connection as a parsed json else returns `None`
        """
        if(self.send(data)):
            return self.get()
        return None

if __name__ == '__main__':
    with EZConnect() as t:
        data, ping = t.req({
            'event': 'get_chunk',
            'coords': [0, 0]  
        })
        print(data, ping)