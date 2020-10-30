import socket
import subprocess
import threading
import os
import signal
from sys import platform
import sys
import base64

class serverType:

    clients_dict = {}
    PORT = 5050
    DISCONNECT_MESSAGE = "exit"
    IP = ''
    server_name = ''
    server = ''

    def __init__(self):
        if platform == "linux" or platform == "linux2":
            os.system('clear')
            cmd = "ip -4 addr | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'"
            IPoutput = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            IPs = IPoutput.split("\n")
            if len(IPs) == 1:
                self.IP = IPs[0]
            else:
                print("List of IPs to use for server:")
                for i in range(len(IPs)):
                    print("[{}] {}".format(i+1, IPs[i]))
                choice = input("\nChoose an option [{} - {}]: ".format(1,len(IPs)))

                try:
                    choice = int(choice)-1
                    if choice < 0 or choice > len(IPs)-1:
                        print("Invalid choice, defaulting to", IPs[0])
                        self.IP = IPs[0]
                    else:
                        self.IP = IPs[choice]
                except:
                    print("Invalid choice, defaulting to", IPs[0])
                    self.IP = IPs[0]

            print("Server will be running at", self.IP)

        elif platform == "darwin":
            os.system("clear")
            cmd = "ifconfig | grep -oE \"\\binet ([0-9]{1,3}\\.){3}[0-9]{1,3}\\b\" | awk '{print $2}'"
            IPoutput = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            IPs = IPoutput.split("\n")
            if len(IPs) == 1:
                self.IP = IPs[0]
            else:
                print("Select IP to use for server 0 to", len(IPs)-1)
                for i in range(len(IPs)):
                    print("[{}] {}".format(i, IPs[i]))
                choice = input()

                try:
                    choice = int(choice)
                    if choice < 0 or choice > len(IPs)-1:
                        print("Invalid choice, defaulting to", IPs[0])
                        self.IP = IPs[0]
                    else:
                        self.IP = IPs[choice]
                except:
                    print("Invalid choice, defaulting to", IPs[0])
                    self.IP = IPs[0]

            print("Server will be running at", self.IP)

        elif platform == "win32":
            os.system('cls')
            self.IP = socket.gethostbyname(socket.gethostname())
        else:
            print('Unsupported OS')
            exit(1)
        self.mainFunc()

    def getName(self):
        self.server_name = input("\nEnter server name : ")
        while not self.server_name.isalpha():
            print(" \n \t ERROR: The Server name should only contain a set of alphabets. \n")
            self.server_name = input('Enter server name : ')
        self.clients_dict['Server'] = self.server_name

    def encodefunc(self, val):
        encoded_data = base64.b64encode(bytes(val, 'utf-8'))
        print("\n\n-------- {}'s Chat-Room accesskey : ( {} ) --------".format(self.server_name, encoded_data.decode('utf-8')))

    def getpasskey(self, str1):
        if str1[0:7] == '192.168':
            self.encodefunc(str1[7:].zfill(8))
        else:
            self.encodefunc(str1.zfill(15))

    def broadcast(self, message, current_client):
        send_client_list = [x for x in list(
            self.clients_dict.keys()) if x != current_client and x != 'Server']
        for client in send_client_list:
            try:
                client.send(message)
            except:
                print('\n \t Could not send message \n')

    def rec_message(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == self.DISCONNECT_MESSAGE:
                    user = self.clients_dict[client]
                    print('\n \t [{}] disconnected \n'.format(user))
                    del self.clients_dict[client]
                    client.close()
                    self.broadcast('\n \t [{}] left! \n'.format(user).encode('utf-8'), client)
                    break

                ## Receiving images and files

                elif message.startswith('image:'):
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
                                chunk=client.recv(512)
                                if not chunk:
                                    break
                                f.write(chunk)
                                c+=512
                                if c==k:
                                    break
                            if fsize-k:
                                chunk=client.recv(fsize-k+1)
                                f.write(chunk)
                        print('Received Image successfully')
                    except:
                        print("An error occurred!")

                elif message.startswith("file:"):
                    fname, fsize = message[5:].split(";")
                    fname = os.path.basename(fname)
                    fsize = int(fsize)

                    if not os.path.exists('Proximity_files'):
                        os.mkdir('Proximity_files')

                    fname1 = 'Proximity_files/' + fname
                    try:
                        with open(fname1, "wb") as f:
                            bytes_read = client.recv(fsize)
                            f.write(bytes_read)
                        print(f"File {fname} received ")
                    
                    except:
                        print("An error occurred!")

                else:
                    print('\t\t\t\t', message)
                    self.broadcast(message.encode('utf-8'), client)
            except:
                user = self.clients_dict[client]
                print('\n \t [{}] disconnected \n'.format(user))
                client.close()
                del self.clients_dict[client]
                self.broadcast('\n \t [{}] left! \n'.format(user).encode('utf-8'), client)
                break


    def send_message(self):
        while True:
            try:
                message = input('')
                b_message = "[{}] : {}".format(self.server_name, message)
                if message == self.DISCONNECT_MESSAGE:
                    self.broadcast('Server left'.encode('utf-8'), 'Server')
                    os._exit(0)

                ## Sending images and files
                              
                elif message.startswith('image:'):
                    fname = message[6:]
                    fsize = os.path.getsize(fname)
                    iname=os.path.basename(fname)
                    message='image: '+iname+' '+str(fsize)
                    self.broadcast(message.encode('utf-8'),'Server')
                    k=(fsize//512)*512
                    c=0
                    try:
                        with open(fname,"rb") as f:
                            while True:
                                chunks = f.read(512)
                                if not chunks:
                                    break
                                c+=512
                                self.broadcast(chunks,'Server')
                                if c==k:
                                    break
                            if fsize-k:
                                chunks=f.read(fsize-k+1)
                                self.broadcast(chunks,'Server')
                        print('Sent Image successfully')
                    except:
                        print("An error occurred!")

                elif message.startswith("file:"):
                    fname=message[5:]
                    fsize=os.path.getsize(fname)
                    message = message+";"+str(fsize)
                    
                    self.broadcast(message.encode('utf-8'), 'Server')
                    
                    try:
                        with open(fname, "rb") as f:
                            
                            bytes_read = f.read(fsize)
                            self.broadcast(bytes_read, 'Server')
                            
                        print("File sent")
                        
                    except:
                        print("An error occurred!")

                else:
                    self.broadcast(b_message.encode('utf-8'), 'Server')
            except:
                print('\n \t Error Occurred while Reading input \n')
                # self.broadcast('Server left'.encode('utf-8'), 'Server')
                # os._exit(0)


    def accept_conn(self):
        while True:
            client, address = self.server.accept()
            client.send('Connect'.encode('utf-8'))
            client_name = client.recv(1024).decode('utf-8')
            final_client_name = client_name
            i = 1
            while final_client_name in self.clients_dict.values():
                final_client_name = "{}{}".format(client_name, i)
                i += 1
            if client_name != final_client_name:
                message = ('\n \t Username updated to ['+final_client_name+']').encode('utf-8')
                client.send(message)
            self.clients_dict[client] = final_client_name
            print("\n \t [{}] joined the server \n".format(self.clients_dict[client]))
            self.broadcast("\n \t [{}] joined! \n".format(self.clients_dict[client]).encode('utf-8'), client)
            client.send("Connected to [{}]!".format(self.server_name).encode('utf-8'))
            thread = threading.Thread(target=self.rec_message, args=(client,))
            thread.start()
            #print('Active threads : ' + str(threading.active_count()-1))

    def keyboardInterruptHandler(self, signal, frame):
        print('Interrupted')
        self.broadcast('Server left'.encode('utf-8'), 'Server')
        os._exit(0)

    def mainFunc(self):
        self.getName()
        self.getpasskey(self.IP)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IP, self.PORT))
        self.server.listen()
        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        thread2 = threading.Thread(target=self.send_message)
        thread2.start()
        print("Server created Successfully!\n")
        self.accept_conn()


s1 = serverType()
