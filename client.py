import socket

c = socket.socket()
# print(socket.gethostname())
c.connect(('192.168.0.105',9999))

name= input('Enter your name')
c.send(bytes(name,'utf-8'))
print(c.recv(1024).decode('utf-8'))
