import socket
import threading
import os
import signal
from sys import platform
import sys
import base64

class clientType:

    PORT = 5050
    DISCONNECT_MESSAGE = "exit"
    passkey = ''
    IP = ''
    username = ''
    client = ''

    def __init__(self):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            os.system('clear')
        elif platform == "win32":
            os.system('cls')
        else:
            print('Unsupported OS')
            exit(1)
        self.passkey = sys.argv[1]
        self.IP = self.decode_key(self.passkey)
        self.mainFunc()

    def getName(self):
        self.username = input("Enter your username: ")
        while not self.username.isalpha():
            print(" \n \t ERROR: The username should only contain alphabates. \n")
            self.username = input('Enter server name : ')

    def decode_key(self, valu):
        try:
            decoded_data = base64.b64decode(valu)
            dec_ip = decoded_data.decode('utf-8')
            if len(dec_ip) == 8:
                dec_ip = '192.168' + dec_ip.lstrip('0')
            elif len(dec_ip) == 15:
                dec_ip = dec_ip.lstrip('0')
            elif len(dec_ip) == 0:
                print("Please enter a passkey \n ")
                self.passkey = input(" Re-enter your accesskey : ")
                dec_ip = self.decode_key(self.passkey)
            else:
                print("Please enter the correct passkey \n ")
                self.passkey = input(" Re-enter your accesskey : ")
                dec_ip = self.decode_key(self.passkey)
        except (ConnectionRefusedError, UnicodeDecodeError, UnboundLocalError, base64.binascii.Error):
            print("Please enter the correct passkey \n ")
            self.passkey = input(" Re-enter your accesskey : ")
            dec_ip = self.decode_key(self.passkey)
        finally:
            return dec_ip

    def receive(self):
        #self. username
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'Connect':
                    self.client.send(self.username.encode('utf-8'))
                elif message == 'Server left':
                    print('\nServer has disconnected\n')
                    os._exit(0)
                elif message.startswith("image:"):
                    fname,fsize = message[7:].split()
                    fpath='Proximity_images'
                    if not os.path.exists(fpath):
                        os.mkdir(fpath)
                    
                    fsize = int(fsize)
                    c=0
                    k=(fsize//512)*512
                    fname1 = fpath+'/'+fname
                    try:
                        with open(fname1,"wb") as f:
                            while True:
                                chunk=self.client.recv(512)
                                if not chunk:
                                    break
                                f.write(chunk)
                                c+=512
                                if c==k:
                                    break
                            if fsize-k:
                                chunk=self.client.recv(fsize-k+1)
                                f.write(chunk)

                        print(f"[{self.username} : Sent {fname}]")
                   except:
                    print("An error occured!")
                elif 'Connected to' in message:
                    print('\n \t ', message, '\n')
                elif 'Username updated to [' in message:
                    print(message)
                    self.username = message[25:-1]
                elif message.startswith("file:"):
                    filename, filesize = message[5:].split(";")
                    # remove absolute path if there is
                    filename = os.path.basename(filename)
                    # convert to integer
                    filesize = int(filesize)
                    if not os.path.exists('Proximity_files'):
                        os.mkdir('Proximity_files')
                    filename = os.path.join('Proximity_files', filename)
                    with open(filename, "wb") as f:
                        bytes_read = self.client.recv(filesize)
                        f.write(bytes_read)
                else:
                    print('\t\t\t\t', message)
            except:
                print("An error occured!")
                self.client.close()
                break

    def write(self):
        while True:
            try:
                input_val = input()
                if input_val == self.DISCONNECT_MESSAGE:
                    self.client.send(self.DISCONNECT_MESSAGE.encode('utf-8'))
                    self.client.close()
                    print('You will be disconnected')
                    os._exit(0)

                elif input_val.startswith("image:"):
                    fname = input_val.split()[1]
                    fsize = os.path.getsize(fname)
                    iname=os.path.basename(fname)
                    message='image: '+iname+' '+str(fsize)
                    self.client.send(message.encode('utf-8'))
                    k=(fsize//512)*512
                    c=0
                    try:
                        with open(fname,"rb") as f:
                            while True:
                                chunks = f.read(512)
                                if not chunks:
                                    break
                                c+=512
                                self.client.send(chunks)
                                if c==k:
                                    break
                            if fsize-k:
                                chunks=f.read(fsize-k+1)
                                self.client.send(chunks)
                        print(f'Sent {fname} successfully')
                    except:
                        print("An error occured!")

                elif input_val.startswith("file:"):
                    filename=input_val[5:]
                    filesize=os.path.getsize("Proximity_files/Client/"+filename)
                    message = input_val+";"+str(filesize)
                    self.client.send(message.encode('utf-8'))
                    with open(("Proximity_files/Client/"+filename), "rb") as f:
                        
                        bytes_read = f.read(filesize)
                        self.client.send(bytes_read)
                        
                    print("File sent")
                else:   
                    message = '[{}] : {}'.format(self.username, input_val)
                    self.client.send(message.encode('utf-8'))
            except:
                print('\n \t Error Occoured while Reading input \n')
                self.client.send(self.DISCONNECT_MESSAGE.encode('utf-8'))
                self.client.close()
                print('You will be disconnected')
                os._exit(0)

    def keyboardInterruptHandler(self, signal, frame):
        print('Interrupted')
        self.client.send(self.DISCONNECT_MESSAGE.encode('utf-8'))
        self.client.close()
        print('You will be disconnected')
        os._exit(0)

    def mainFunc(self):
        self.getName()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.IP, self.PORT))
        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()


c1 = clientType()
