from cryptography.fernet import Fernet
import socket
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
                                                
                          
                                                   
secure communication for IOT device the client side ,  \n  monatha  kaddousi \n """, blue_color), end="")



def clear_screen():
    os.system("clear")  # Clear the screen
# Load the encryption key
def load_key():
    return open("key.key", "rb").read()

# Decrypt the encrypted data
def decrypt_data(encrypted_data):
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data
clear_screen()
banner()
# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("localhost", 554))  # Replace "localhost" with the server IP and 554 with the appropriate port number

    while True:
        # Send data to the server
        s.sendall("Hello, IoT device!".encode())

        # Receive encrypted data from the server
        encrypted_data = s.recv(1024)

        # Decrypt the encrypted data
        decrypted_data = decrypt_data(encrypted_data)
        print("Received decrypted data:", decrypted_data)