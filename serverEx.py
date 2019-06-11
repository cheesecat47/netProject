# https://soooprmx.com/archives/8737

from socket import *
import random
import threading

# 소켓 변수
port = 45454

# 게임 관련 변수
chance = 7  # 기회 7번
result = -1
word = 'apple'  # 단어는 나중에 랜덤 선택.
word_now = ''  # 게임 중에 보여줄 문자열
gamestart = False  # 게임 시작 체크
goal = 0
client_list = list()


# 함수 정의
def initgame():  # 게임 초기화
    global chance  # 전역 변수 사용
    global word_now
    global gamestart
    global goal

    chance = 7
    # gamestart = False
    # goal = len(word)
    word_now = ''
    result = -1
    for _ in word:
        word_now += '_ '  # 처음엔 빈 칸으로 초기화, word 길이만큼 _ _ _ _ _
    # print(word_now)


def sendall(sendData):
    global client_list

    print(sendData)
    for (thissock, addr) in client_list:
        thissock.send(sendData.encode('utf-8'))
        print('send to ', addr)


# 메인
while True:
    print('Server waiting for clients')
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(3)

    for i in range(3):  # 클라 3개 받아서
        connectionSock, addr = serverSock.accept()
        client_list.append((connectionSock, addr))
        print('client connected: ', str(addr))

    # 새 연결 후 게임 초기화
    initgame()

    while True:
        if len(client_list) == 3:
            # 모든 클라이언트 이름 보내기
            i = 0
            for (thissock, addr) in client_list:
                sendData2 = str(i)
                print(sendData2, addr)
                thissock.send(sendData2.encode('utf-8'))
                i += 1
        break
    print('Client list done!')

    print(word_now)

    # 첫 턴 / 남은 횟수 /  현재 문자열 / 현재 상황? 슬래시로 보내면 클라가 슬래시로 tokenise.
    turn = random.randrange(len(client_list))  # 첫 턴은 랜덤으로
    sendData = str(turn) + '/' + str(chance) + '/' + word_now + '/' + str(result)
    sendall(sendData)
