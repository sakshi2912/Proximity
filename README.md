# Proximity

The repo contains a simple implementation of an offline chatroom.



## Usage:

-   
    ``` git clone https://github.com/sakshi2912/Proximity.git ```

- To start the server
  
    ``` python3 server.py ```

    If the web socket is not occupied, the chat server boots up and generates a passkey for the chat room it is hosting.

- To start a client and connect to a chat room.
  
    ``` python3 client.py < chatroom's passkey > ```

## Features/Bugs:

- Works on Windows and Linux
- Can support group chats.
- Anyone in the same network can start/join chatroot.
- A client can exit and reconnect to a chat-room multiple times
- One server can host only one chat-room at a time
- When the server disconnects, all the participants wil be forced to exit.
- Type 'exit' to leave the chat-room
