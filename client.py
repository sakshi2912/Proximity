import socket
import threading
import os

nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55455))


def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'Connect':
                client.send(nickname.encode('utf-8'))
            
            elif message == 'Server left':
                print('You will be disconnected')
                os._exit(0)
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
        
def write():
    while True:
        input_val = input()
        if input_val == 'exit':
            client.send('exit'.encode('utf-8'))
            client.close()
            print('You will be disconnected')
            os._exit(0)
        else:
            message = f'{nickname} {input_val}'
            client.send(message.encode('utf-8'))
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()