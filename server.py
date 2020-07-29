import socket 
# 2 args , ipv4/6 and tcp/udp
s = socket.socket()
print("Socket created")
#one obj : 2 args, ip addr and port number 
s.bind(('localhost',9999))
#queue for connections (number of clients) 
s.listen(3)
print("Waiting for connections")

while(1):
    #c is socket and addr is the address
    c,addr=s.accept()
    print(c.recv(1024).decode('utf-8'))
    print("Connected to :",c)
    

    c.send(bytes('Welcome to sak','utf-8'))
    c.close()