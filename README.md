# Proximity

This repository contains a simple implementation of an offline chatroom.



## Usage:

-   
    ``` git clone https://github.com/sakshi2912/Proximity.git ```

- To start the server
  
    ``` python3 server.py ```

    Choose an IP address in the list of IP adresses presented, to start the server in the respective network.

    If the web socket is not occupied, the chat server is started and a passkey is generated, for the chat room it is hosting. ( This passkey is to be shared with the participants joining the chat. ) 

- To start a client and connect to a chat room
  
    ``` python3 client.py < chatroom's passkey > ```

- To send a file from client to server and vice-versa  <br>

    ``` file:full_path_to_file ``` 

   Files are stored in the folder: Proximity_files
   
- To send an image from client to server and vice-versa <br>

    ``` image:full_path_to_image ```<br>

   Images are stored in the folder: Proximity_images

## Features/Bugs:

- Works on Windows, Linux and Mac OS
- Can support group chats.
- Can support media transfer between client and server.<br>
    a. Files (.txt,.py , .pdf etc.) are stored in Proximity_files <br>
    b. Images (.png, .jpg etc. ) are stored in Proximity_images
- Anyone in the same network can start/join chatroom.
- A client can exit and re-connect to a chat-room multiple times.
- A server can host multiple chatrooms, but only one chat-room per network interface.
- When the server disconnects, all the participants wil be forced to exit.
- Type 'exit' to leave the chat-room.
- Needs an User Interface (Refer v2 branch to checkout the previous work done on Terminal UI)
