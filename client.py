import socket
import library
from rsa import RSA

def request_public_key(device_id):
    host = "127.0.0.1"
    port = 5002  # PKA server port
    mySocket = socket.socket()
    mySocket.connect((host, port))
    mySocket.send(device_id.encode())
    public_key_data = mySocket.recv(1024).decode()
    mySocket.close()
    e, n = map(int, public_key_data.split(','))
    return (e, n)

def Main():
    host = "127.0.0.1"
    port = 5001

    # Inisialisasi koneksi ke server
    mySocket = socket.socket()
    mySocket.connect((host, port))

    device_id = "DeviceA"  # Example device ID
    public_key = request_public_key(device_id)

    rsa = RSA()  # Create an instance of RSA with its own keys

    while True:
        message = input("Enter the message you want to send (or 'q' to quit): ")
        if message.lower() == 'q':
            mySocket.send(message.encode())
            break

        # Encrypt DES key with RSA public key
        des_key = "1010101010"  # Example DES key
        encrypted_des_key = rsa.encrypt(des_key)

        # Send encrypted DES key to server
        mySocket.send(str(encrypted_des_key).encode())

        # Enkripsi pesan sebelum dikirim
        encryptedMessage = library.encrypt(message)
        print("Encrypted message to be sent:", encryptedMessage)
        
        # Kirim pesan terenkripsi ke server
        library.sending()
        mySocket.send(encryptedMessage.encode())
        
        # Menerima pesan terenkripsi dari server
        data = mySocket.recv(1024).decode()
        if not data or data.lower() == 'q':
            print("Connection closed by server.")
            break

        # Dekripsi pesan yang diterima
        decryptedMessage = library.decrypt(data)
        print("Received Encrypted Message:", data)
        print("Decrypted Message:", decryptedMessage)
        print("\n")
    
    mySocket.close()
    print("Connection closed by client.")

if __name__ == '__main__':
    Main()
