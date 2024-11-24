import socket
from rsa import RSA

class PublicKeyAuthority:
    def __init__(self):
        self.public_keys = {}
        self.rsa = RSA()  # Create an instance of RSA

    def add_device(self, device_id):
        self.public_keys[device_id] = self.rsa.get_public_key()

    def get_public_key(self, device_id):
        return self.public_keys.get(device_id)

def Main():
    host = "127.0.0.1"
    port = 5002  # PKA server port

    pka = PublicKeyAuthority()
    pka.add_device("DeviceA")  # Simulate adding Device A's public key
    pka.add_device("DeviceB")  # Simulate adding Device B's public key

    mySocket = socket.socket()
    mySocket.bind((host, port))
    mySocket.listen(2)
    print("PKA Server is running...")

    while True:
        conn, addr = mySocket.accept()
        print("Connection from:", str(addr))

        device_id = conn.recv(1024).decode()  # Receive device ID
        public_key = pka.get_public_key(device_id)

        if public_key:
            conn.send(f"{public_key[0]},{public_key[1]}".encode())  # Send public key
        else:
            conn.send(b"Device not found.")

        conn.close()

if __name__ == '__main__':
    Main()
