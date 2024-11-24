import socket
import library
from rsa import RSA

def Main():
    host = "127.0.0.1"
    port = 5001

    # Inisialisasi server
    mySocket = socket.socket()
    mySocket.bind((host, port))

    print("Waiting for connection.....")
    mySocket.listen(2)
    conn, addr = mySocket.accept()
    print("Connection from:", str(addr))

    rsa = RSA()  # Create an instance of RSA with its own keys

    while True:
        # Menerima encrypted DES key from client
        encrypted_des_key = int(conn.recv(1024).decode())  # Convert received string back to integer
        des_key = rsa.decrypt(encrypted_des_key)  # Decrypt DES key
        print("Received Encrypted DES Key:", encrypted_des_key)
        print("Decrypted DES Key:", des_key)

        # Menerima pesan terenkripsi dari client
        data = conn.recv(1024).decode()
        if not data or data.lower() == 'q':
            print("Connection closed by client.")
            break
        
        # Mendekripsi pesan
        decryptedMessage = library.decrypt(data)
        print("Received Encrypted Message:", data)
        print("Decrypted Message:", decryptedMessage)
        print("\n")
        
        # Mengambil input pesan dari server untuk dikirim ke client
        message = input("Enter the message you want to send (or 'q' to quit): ")
        if message.lower() == 'q':
            conn.send(message.encode())
            break

        # Enkripsi pesan sebelum dikirim
        encryptedMessage = library.encrypt(message)
        print("Encrypted message to be sent:", encryptedMessage)
        
        # Kirim pesan terenkripsi ke client
        library.sending()
        conn.send(encryptedMessage.encode())
    
    conn.close()
    print("Server stopped.")

if __name__ == '__main__':
    Main()
