import socket
import array

MSGLEN = 128

class HLLConnection:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self):
        self.xorkey = None
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        
    def connect(self, host, port, password: str):
        self.sock.connect((host, port))
        self.xorkey = self.sock.recv(MSGLEN)
        self.send(f"login {password}".encode())
        result = self.receive()
        if result != b'SUCCESS':
            raise ValueError('Invalid password')

    def close(self):
        self.sock.close()
        
    def send(self, msg):
        sent = self.sock.send(self._xor(msg))
        if sent != len(msg):
            raise RuntimeError("socket connection broken")
        return sent

    def _xor(self, msg):
        n = []
        for i in range(len(msg)):
            n.append(msg[i] ^ self.xorkey[i % len(self.xorkey)])

        return array.array('B', n).tobytes()

    def receive(self, msglen=MSGLEN):
        buff = self.sock.recv(msglen)
        msg = self._xor(buff)
        
        while len(buff) >= msglen:
            buff = self.sock.recv(msglen)
            msg += self._xor(buff)
            
        return msg



