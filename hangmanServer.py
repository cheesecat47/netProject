from socket import *

# 소켓 변수
port = 45454

# 게임 관련 변수
chance = 10  # 기회 10번
word = 'apple'  # 단어는 나중에 랜덤 선택.
word_now = ''  # 게임 중 문자열
for _ in word:
    word_now += '_ '  # 처음엔 빈 칸으로 초기화
print(word_now)


# 함수 정의
def checkword(ch):
    global chance
    word_temp = ''
    flag = False  # 새로운 알파벳 있는지 확인하기 위해

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
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()

while True:
    recvData = connectionSock.recv(1024).decode('utf-8')  # 문자열로 입력 받음

    if len(recvData) == 1:  # 알파벳 입력이면
        word_now = checkword(recvData[0])  # 그 알파벳 있는지 체크
        print('word_now: ', word_now, ' chance: ', str(chance));

    sendData = word_now
    connectionSock.send(sendData.encode('utf-8'))
    sendData = str(chance)
    connectionSock.send(sendData.encode('utf-8'))
