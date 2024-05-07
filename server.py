from cryptography.fernet import Fernet
import os
import socket
import threading
import logging
import os
from termcolor import colored

def banner():
    """Prints a blue banner with author information."""

    blue_color = 'blue'  # Define the desired blue color
    red_color = 'red'
    print(colored("""


 _____    _____                                 
|_   _|  |_   _|                                
  | |  ___ | |    ___  ___  ___ _   _ _ __ ___  
  | | / _ \| |   / __|/ _ \/ __| | | | '__/ _ \ 
 _| || (_) | |   \__ \  __/ (__| |_| | | |  __/ 
 \___/\___/\_/   |___/\___|\___|\__,_|_|  \___| 
                                                
                          
                                                   
secure communication for IOT device the server side ,  \n  monatha  kaddousi \n """, blue_color), end="")



def clear_screen():
    os.system("clear")  # Clear the screen

# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open("key.key", "rb").read()

# Encrypt the IoT device's data
def encrypt_data(data):
    key = load_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# Decrypt the IoT device's data
def decrypt_data(encrypted_data):
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

# Locate the IoT device on the network
def locate_iot_device():
    # Implement network scanning or other methods to locate the IoT device
    # For example, you can use a port scanning library like nmap
    # and check for open ports or other indicators that indicate the device's presence
    # Return the IP address or other identifier of the IoT device
    return "127.0.0.1"

# Check if the connection is still active
def is_connection_active(s):
    try:
        # Send a ping message to check if the connection is still active
        s.sendall("ping".encode())
        return True
    except BrokenPipeError:
        return False

# Handle client connections
def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                # Receive data from the IoT device
                data = conn.recv(1024).decode()

                # Encrypt the received data
                encrypted_data = encrypt_data(data)
                print("Encrypted data:", encrypted_data)

                # Decrypt the encrypted data
                decrypted_data = decrypt_data(encrypted_data)
                print("Decrypted data:", decrypted_data)

                # Send the encrypted data back to the IoT device
                conn.sendall(encrypted_data)
            except BrokenPipeError:
                print(f"Connection closed by {addr}")
                break
            except Exception as e:
                logging.error("An unexpected error occurred: %s", str(e))
                break
clear_screen()
banner()
# Example usage
if __name__ == "__main__":
    # Generate a key (run this only once)
    generate_key()

    # Locate the IoT device
    iot_device_ip = locate_iot_device()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the IP and port
        s.bind((iot_device_ip, 554))  # Replace 8888 with the appropriate port number
        # Listen for incoming connections
        s.listen()
        print(f"Server is listening on {iot_device_ip}:554")

        while True:
            # Accept a client connection
            conn, addr = s.accept()
            # Handle the client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()