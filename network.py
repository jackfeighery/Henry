import socket
import pickle

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.0.15'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        # print(self.id)

    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            # Receive data from the server to confirm connection
            data = self.client.recv(8192*16)
            # Unpickle the received data
            # print("Received pickled data:", data)
            print("size of data: " + str(data.__sizeof__()))
            return pickle.loads(data)
        except Exception as e:
            print("Connection error:", e)
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            response = self.client.recv(8192*16)
            if response:
                return pickle.loads(response)
            else:
                print("Server did not send any data")
                return None
        except Exception as e:
            print("Error sending data:", e)
            return None

# n = Network()
# print(n.send("hello"))
# print(n.send("working"))