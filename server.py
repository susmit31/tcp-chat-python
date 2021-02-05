import socket
import threading

PORT = 12345
IP = '127.0.0.1'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP,PORT))
server.listen()
print('Listening...')
clients = []
nicknames = []

def getMsgs(client):
    while True:
        try:
            msg = client.recv(1024)
            print(msg.decode('utf-8'))
            broadcast(msg)
        except:
            print('error')
            idx = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[idx]
            nicknames.remove(nickname)

def broadcast(msg):
    for client in clients:
        client.send(msg)
        
def receiveSignal():
    while True:
        client, address = server.accept()
        client.send("nick".encode('utf-8'))
        nick = client.recv(1024).decode('utf-8')
        print(f'Connected with {str(address)}')
        broadcast(f'\n{nick} joined the chat.\n>> '.encode('utf-8'))
        client.send('\nSuccessfully connected with the server\n>> '.encode('utf-8'))
        nicknames.append(nick)
        clients.append(client)
        thread = threading.Thread(target=getMsgs, args=(client,))
        thread.start()
        
def waitKey():
    while input('')!='q':
        continue
    exit()

wait_thread = threading.Thread(target=waitKey)
receiveSignal()
wait_thread.start()