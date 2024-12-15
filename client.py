import socket
import library
from rsa import RSA
import sys

def request_public_key(device_id, rsa):
    try:
        host = "127.0.0.1"
        port = 5002  # PKA server port
        
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((host, port))
        
        # Send device ID
        mySocket.send(device_id.encode())
        
        # Send own public key (e)
        mySocket.send(str(rsa.get_public_key()[0]).encode())
        
        # Receive encrypted or plain public key
        public_key_data = mySocket.recv(2048).decode()
        
        mySocket.close()
        
        # Try to decrypt if it's an integer (encrypted)
        try:
            encrypted_key = int(public_key_data)
            public_key_str = rsa.decrypt(encrypted_key)
        except:
            public_key_str = public_key_data
        
        # Parse public key
        e, n = map(int, public_key_str.split(','))
        return (e, n)
    except Exception as e:
        print(f"Error requesting public key: {e}")
        sys.exit(1)

def Main():
    host = "127.0.0.1"
    port = 5001

    # Initialize own RSA
    sender_rsa = RSA()

    # Connect to server
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((host, port))
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    # Request receiver's public key
    receiver_device_id = "DeviceB"
    try:
        receiver_public_key = request_public_key(receiver_device_id, sender_rsa)
    except Exception as e:
        print(f"Error getting receiver public key: {e}")
        mySocket.close()
        return

    while True:
        try:
            message = input("Enter the message you want to send (or 'q' to quit): ")
            if message.lower() == 'q':
                mySocket.send(message.encode())
                break

            # Prepare DES key
            des_key = "1010101010"  # Example DES key

            # Double encryption of DES key
            # 1. Encrypt with sender's private key
            encrypted_des_key_1 = sender_rsa.encrypt(des_key)
            
            # 2. Encrypt with receiver's public key
            receiver_rsa = RSA()
            receiver_rsa.e, receiver_rsa.n = receiver_public_key
            encrypted_des_key_2 = receiver_rsa.encrypt(encrypted_des_key_1)

            # Send encrypted DES key
            mySocket.send(str(encrypted_des_key_2).encode())

            # Encrypt message with DES
            encryptedMessage = library.encrypt(message)
            print("Encrypted message to be sent:", encryptedMessage)
            
            # Send encrypted message
            library.sending()
            mySocket.send(encryptedMessage.encode())
            
            # Receive response
            data = mySocket.recv(1024).decode()
            if not data or data.lower() == 'q':
                print("Connection closed by server.")
                break

            # Decrypt received message
            decryptedMessage = library.decrypt(data)
            print("Received Encrypted Message:", data)
            print("Decrypted Message:", decryptedMessage)
            print("\n")
        
        except Exception as e:
            print(f"Error during communication: {e}")
            break
    
    mySocket.close()
    print("Connection closed by client.")

if __name__ == '__main__':
    Main()