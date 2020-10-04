# Proximity

This repository contains a simple implementation of an offline chatroom.



## Usage:

-   
    ``` git clone https://github.com/sakshi2912/Proximity.git ```

- To start the server
  
    ``` python3 server.py ```

    If the web socket is not occupied, the chat server is started and a passkey is generated, for the chat room it is hosting. ( This passkey is to be shared with the participants joining the chat. ) 

- To start a client and connect to a chat room
  
    ``` python3 client.py < chatroom's passkey > ```

## Features/Bugs:

- Works on Windows, Linux and Mac OS
- Can support group chats.
- Anyone in the same network can start/join chatroom.
- A client can exit and re-connect to a chat-room multiple times.
- One server can host only one chat-room at a time.
- When the server disconnects, all the participants wil be forced to exit.
- Type 'exit' to leave the chat-room.
- Needs a User Interface
