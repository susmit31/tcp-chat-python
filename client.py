import socket
import threading

PORT = 12345
LOCALIP = '127.0.0.1'
IP = '192.168.0.5'

nick = input('Enter your display name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg=='nick':
                print('Sending display name...')
                client.send(nick.encode('utf-8'))
            else:
                if len(msg):
                    print(msg)
        except:
            print('An error occurred.')
            client.close()
            break

def awaitMsg():
    while True:
        try:
            msg = input('')
            if msg=='q':
                break
            client.send(f'\n{nick}: {msg}\n>> '.encode('utf-8'))
        except:
            print('Error.')
            client.close()
            break

rcv_thread = threading.Thread(target=receive)
msg_thread = threading.Thread(target=awaitMsg)

rcv_thread.start()
msg_thread.start()