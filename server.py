# https://seolin.tistory.com/98

from socket import *
from datetime import datetime as dt


def out(msg):
    print(msg)
    log.write(msg + '\n')


port = 55891
flag = True

while flag:
    fname = './log/' + str(dt.now())[:10] + '-' + str(dt.now().hour) + '-' + str(dt.now().minute) \
            + '-' + str(dt.now().second) + '.txt'
    log = open(fname, 'w')

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(1)

    out(str(dt.now()) + ': %d 포트 대기...' % port)

    connectionSock, addr = serverSock.accept()

    out(str(dt.now()) + ' ' + str(addr) + ' ' + ': 에서 접속되었습니다.')

    while True:
        recvData = connectionSock.recv(1024).decode('utf-8')
        out(str(dt.now()) + ' ' + str(addr) + ' ' + ': ' + recvData)

        if recvData == 'exit':
            flag = False
            break

        sendData = 'server: echo: ' + recvData
        connectionSock.send(sendData.encode('utf-8'))

    log.close()
    #end while flag
