# https://soooprmx.com/archives/8737

from socket import *

# 소켓 변수
port = 45454

# 게임 관련 변수
chance = 7  # 기회 7번
result = 0
word = 'apple'  # 단어는 나중에 랜덤 선택.
word_now = ''  # 게임 중에 보여줄 문자열
gamestart = False  # 게임 시작 체크


# 함수 정의
def initgame():  # 게임 초기화
    global chance  # 전역 변수 사용
    global word_now
    global gamestart

    chance = 7
    gamestart = False
    word_now = ''
    for _ in word:
        word_now += '_ '  # 처음엔 빈 칸으로 초기화, word 길이만큼 _ _ _ _ _
    print(word_now)


def checkword(ch):
    global chance
    global result
    word_temp = ''
    flag = False  # 새로운 알파벳 있는지 확인하기 위해

    # 알파벳인지 단어인지 구별
    # 단어일 때
    if ch == word:
        flag = True
        result = 1  # 맞췄다고 알림
        for i in range(len(word)):
            word_temp += word[i] + ' '  # 알파벳 띄어쓰기 포함해서 붙임

    # 알파벳일 때
    elif ch != word:
        for i in range(len(word)):
            if ch == word[i]:  # 알파벳 같은게 있으면
                word_temp += ch + ' '  # 알파벳 붙이고
                flag = True  # 새로운게 있다고 알림
            else:  # 알파벳 다르면
                word_temp += word_now[i * 2] + ' '  # 이전에 그 자리에 있던 거 붙임.

    if flag is False:  # 바뀐게 없다? 단어가 틀렸거나, 입력한 알파벳이 단어 안에 없을 때
        chance -= 1  # 기회 줄어듦

    return word_temp


# 메인
while True:
    print('Server waiting for clients')
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(1)
    connectionSock, addr = serverSock.accept()
    print('client connected: ', str(addr))

    # 새 연결 후 게임 초기화
    initgame()

    # 클라가 ready 입력하면 게임 시작. exit이면 종료. 4번동안 다른 메세지 들어오면 그냥 종료
    try:
        recvData = connectionSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
    except ConnectionResetError:  # 강제 종료 발생 시
        print('client 강제 종료,  게임 초기화')  # 나중에 멀티 클라 상황일 때 추가 핸들링 구현
        break

    print('client ready or exit? ', recvData)

    if len(recvData) > 0:  # null이 아니면
        recvData = recvData.rstrip('\n')  # 개행문자 떼고

        if recvData == 'ready':  # ready면
            gamestart = True  # 바꾸고
        elif recvData == 'exit':
            connectionSock.close()  # 나간다하면 보내줌

    if gamestart is False:
        print("gamestart = False")
        connectionSock.close()
        continue

    while True:
        try:
            recvData = connectionSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
        except ConnectionResetError:  # 강제 종료 발생 시
            print('client 강제 종료,  게임 초기화')  # 나중에 멀티 클라 상황일 때 추가 핸들링 구현
            break

        if len(recvData) > 0:  # null이 아니면
            recvData = recvData.rstrip('\n')  # 개행문자 떼고

            if recvData == 'exit':
                print('client sent exit message')
                connectionSock.close()
                break

            word_now = checkword(recvData)  # 체크
            print('recvData: ', recvData, 'word_now: ', word_now, ' chance left: ', str(chance))

        elif len(recvData) == 0:
            break

        # 남은 횟수 /  현재 문자열 / 현재 상황? 슬래시로 보내면 클라가 슬래시로 tokenise.
        sendData = str(chance) + '/' + word_now + '/' + str(result)
        connectionSock.send(sendData.encode('utf-8'))
