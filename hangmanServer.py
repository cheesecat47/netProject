from socket import *

# 소켓 변수
port = 45454

# 게임 관련 변수
chance = 7  # 기회 7번
word = 'apple'  # 단어는 나중에 랜덤 선택.
word_now = ''  # 게임 중에 보여줄 문자열


# 함수 정의
def initgame():
    global chance
    global word_now

    chance = 7
    for _ in word:
        word_now += '_ '  # 처음엔 빈 칸으로 초기화
    print(word_now)


def checkword(ch):
    global chance
    word_temp = ''
    flag = False  # 새로운 알파벳 있는지 확인하기 위해

    # 알파벳인지 단어인지 구별

    for i in range(len(word)):
        if ch == word[i]:  # 알파벳 같은게 있으면
            word_temp += ch + ' '  # 알파벳 붙이고
            flag = True
        else:  # 알파벳 다르면
            word_temp += word_now[i * 2] + ' '  # 이전에 그 자리에 있던 거 붙임.

    if flag == False:
        chance -= 1

    return word_temp


# 메인
while True:
    print('Server waiting for clients')
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(1)
    connectionSock, addr = serverSock.accept()

    # 새 연결 후 게임 초기화
    initgame()

    while True:
        try:
            recvData = connectionSock.recv(1024).decode('utf-8')  # 문자열로 입력 받음
        except ConnectionResetError:  # 강제 종료 발생 시
            print('client 강제 종료,  게임 초기화')
            break

        if len(recvData) > 0:  # null이 아니면
            recvData = recvData.rstrip('\n')  # 개행문자 떼고
            print(recvData, type(recvData), len(recvData))
            word_now = checkword(recvData)  # 체크
            print('word_now: ', word_now, ' chance: ', str(chance));

        elif len(recvData) == 0:
            break

        sendData = str(chance) + '/' + word_now
        connectionSock.send(sendData.encode('utf-8'))
