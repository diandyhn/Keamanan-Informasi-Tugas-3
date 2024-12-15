import socket
import library
from rsa import RSA
import traceback

def Main():
    host = "127.0.0.1"
    port = 5001

    # Initialize server socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocket.bind((host, port))

    print("Waiting for connection.....")
    mySocket.listen(5)
    
    try:
        conn, addr = mySocket.accept()
        print("Connection from:", str(addr))

        # Initialize own RSA
        receiver_rsa = RSA()

        while True:
            try:
                # Receive encrypted DES key
                encrypted_des_key_2 = conn.recv(1024).decode().strip()
                
                if not encrypted_des_key_2 or encrypted_des_key_2.lower() == 'q':
                    print("Connection closed by client.")
                    break
                
                # Decrypt with receiver's private key
                encrypted_des_key_1 = receiver_rsa.decrypt(int(encrypted_des_key_2))
                
                # Decrypt with sender's public key (placeholder)
                sender_rsa = RSA()
                des_key = sender_rsa.decrypt(int(encrypted_des_key_1))
                
                print("Received Encrypted DES Key:", encrypted_des_key_2)
                print("Decrypted DES Key:", des_key)

                # Receive encrypted message
                data = conn.recv(1024).decode()
                if not data or data.lower() == 'q':
                    print("Connection closed by client.")
                    break
                
                # Decrypt message
                decryptedMessage = library.decrypt(data)
                print("Received Encrypted Message:", data)
                print("Decrypted Message:", decryptedMessage)
                print("\n")
                
                # Server's response
                message = input("Enter the message you want to send (or 'q' to quit): ")
                if message.lower() == 'q':
                    conn.send(message.encode())
                    break

                # Encrypt response
                encryptedMessage = library.encrypt(message)
                print("Encrypted message to be sent:", encryptedMessage)
                
                # Send encrypted response
                library.sending()
                conn.send(encryptedMessage.encode())
            
            except Exception as e:
                print(f"Communication error: {e}")
                traceback.print_exc()
                break

    except Exception as e:
        print(f"Server error: {e}")
        traceback.print_exc()
    
    finally:
        conn.close()
        mySocket.close()
        print("Server stopped.")

if __name__ == '__main__':
    Main()