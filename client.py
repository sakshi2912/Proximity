import socket
import threading
import os
import signal


username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55455))


def receive():
    while True:
        try:

            message = client.recv(1024).decode('utf-8')
            if message == 'Connect':
                client.send(username.encode('utf-8'))

            elif message == 'Server left':
                print('\nServer has disconnected\n')
                os._exit(0)

            elif message[-5:] == 'left!':
                print('\n \t', messge, '\n')

            elif message == 'Connected to server!':
                print('\n \t Connected to the Server! \n')

            else:
                print('\t\t\t\t', message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        try:
            input_val = input()
            if input_val == 'exit':
                client.send('exit'.encode('utf-8'))
                client.close()
                print('You will be disconnected')
                os._exit(0)
            else:
                message = f'[{username}] : {input_val}'
                client.send(message.encode('utf-8'))
        except:
            print('\n \t Error Occoured while Reading input \n')
            client.send('exit'.encode('utf-8'))
            client.close()
            print('You will be disconnected')
            os._exit(0)


def keyboardInterruptHandler(signal, frame):
    print('Interrupted')
    client.send('exit'.encode('utf-8'))
    client.close()
    print('You will be disconnected')
    os._exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
