import socket
from rsa import RSA

class PublicKeyAuthority:
    def __init__(self):
        self.public_keys = {}
        self.rsa = RSA()  # PKA's own RSA instance

    def add_device(self, device_id):
        # Create a new RSA instance for each device
        device_rsa = RSA()
        self.public_keys[device_id] = device_rsa.get_public_key()
        return device_rsa

    def get_public_key(self, device_id, requester_public_key=None):
        target_public_key = self.public_keys.get(device_id)
        
        if target_public_key:
            # Convert public key to string
            key_str = f"{target_public_key[0]},{target_public_key[1]}"
            
            # If requester's public key is provided, encrypt the key
            if requester_public_key:
                rsa_requester = RSA()
                rsa_requester.e, rsa_requester.n = requester_public_key
                encrypted_key = rsa_requester.encrypt(key_str)
                return str(encrypted_key)
            
            # Otherwise, return as is
            return key_str
        
        return "Device not found"

def Main():
    host = "127.0.0.1"
    port = 5002  # PKA server port

    pka = PublicKeyAuthority()
    # Pre-register some devices
    pka.add_device("DeviceA")
    pka.add_device("DeviceB")

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocket.bind((host, port))
    mySocket.listen(5)
    print("PKA Server is running...")

    while True:
        try:
            conn, addr = mySocket.accept()
            print("Connection from:", str(addr))

            # Receive device ID
            device_id = conn.recv(1024).decode().strip()
            
            # Receive requester's public key
            try:
                requester_e = int(conn.recv(1024).decode())
                requester_public_key = (requester_e, None)  # Placeholder for n
            except:
                requester_public_key = None

            # Get public key (potentially encrypted)
            public_key = pka.get_public_key(device_id, requester_public_key)

            # Send public key
            conn.send(public_key.encode())
            conn.close()

        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == '__main__':
    Main()