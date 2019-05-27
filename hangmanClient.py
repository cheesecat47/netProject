from socket import *
import hangmanPrint

port = 45454

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))

print('접속 완료')

while True:
    sendData = input('> ')
    clientSock.send(sendData.encode('utf-8'))

    recvData = clientSock.recv(1024).decode('utf-8')
    print(recvData)
    recvData = clientSock.recv(1024).decode('utf-8')
    hangmanPrint.hmprint(recvData)