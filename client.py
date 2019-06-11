from socket import *

port = 45454

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('155.230.28.129', port))

print('접속 완료')

while True:
    try:
        recvData = clientSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
    except ConnectionResetError:  # 강제 종료 발생 시
        break

    if len(recvData) > 0:  # null이 아니면
        recvData = recvData.rstrip('\n')  # 개행문자 떼고

    print(recvData)

if input() == 'exit':
    exit(0)