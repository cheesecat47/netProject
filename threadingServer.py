from socket import *
import threading
import time

# 상수
FAIL = -1

# 소켓 변수
port = 45454

# 게임 관련 변수
chance = 7  # 기회 7번
goal = 999  # * 맞춰야하는 알파벳 수
word = 'apple'  # 단어는 나중에 랜덤 선택.
word_now = ''  # 게임 중에 보여줄 문자열
gamestart = False  # 게임 시작 체크
clients = list();  # 클라 배열
turn = 0  # 게임 시작 전에는 준비된 수, 시작 후에는 누구차례
result = -1

def initgame():  # 게임 초기화
    global chance  # 전역 변수 사용
    global word_now
    global gamestart
    global goal

    chance = 7
    gamestart = True
    goal = len(word)  # * 맞춰야할 단어의 길이 체크
    word_now = ''
    for _ in word:
        word_now += '_ '  # 처음엔 빈 칸으로 초기화, word 길이만큼 _ _ _ _ _
    # print(word_now)

def client_manager(connectionSock, addr):
    global gamestart
    global turn
    global word_now
    global clients

    if gamestart:
        return
    localturn = turn
    turn += 1

    #readycheck = ready_check(connectionSock)
    #if readycheck == FAIL:
    #    turn -= 1
    #    return

    clientName = name_check(connectionSock)
    if clientName == FAIL:
        turn -= 1
        return

    print('client name?  ', clientName)
    clients.append((clientName, connectionSock))

    while not gamestart:  # wait for other players
        time.sleep(1)

    while gamestart:
        if localturn == turn:
            print("localturn ", localturn, " turn ", turn)
            send_formal_data(turn, connectionSock)

            try:
                recvData = connectionSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
            except ConnectionResetError:  # 강제 종료 발생 시
                print('client 강제 종료, 턴 넘기기')  # 나중에 멀티 클라 상황일 때 추가 핸들링 구현
                break

            if len(recvData) > 0:  # null이 아니면
                recvData = recvData.rstrip('\n')  # 개행문자 떼고

                if recvData == 'exit':
                    print('client sent exit message')
                    connectionSock.close()
                    break

                word_now = checkword(recvData, localturn)  # 체크
                print('recvData: ', recvData, 'word_now: ', word_now, ' chance left: ', str(chance))
                turn = (turn + 1) % len(clients)

            elif len(recvData) == 0:
                break
        else:
            print("player ", clientName, "waiting for turn", localturn, "/", turn)
            time.sleep(1)

def checkword(ch, cast):
    global chance
    global word
    global goal
    global word_now
    global result

    word_temp = ''
    flag = False  # 새로운 알파벳 있는지 확인하기 위해

    # 알파벳인지 단어인지 구별
    # 단어일 때
    if ch == word:
        flag = True
        goal = 0  # * 한꺼번에 맞췄을경우 전부 제거
        for i in range(len(word)):
            word_temp += word[i] + ' '  # 알파벳 띄어쓰기 포함해서 붙임

    # 알파벳일 때
    elif ch != word:
        for i in range(len(word)):
            if ch == word[i]:  # 알파벳 같은게 있으면
                if ch in word_now:  # * ch가 이미 나왔을경우
                    word_temp += word_now[i * 2] + ' '  # * 알파벳 똑같을때랑 똑같이 처리
                else:
                    word_temp += ch + ' '  # 알파벳 붙이고
                    flag = True  # 새로운게 있다고 알림
                    goal -= 1  # * 그리고 정답 체크
            else:  # 알파벳 다르면
                word_temp += word_now[i * 2] + ' '  # 이전에 그 자리에 있던 거 붙임.

    if flag is False:  # 바뀐게 없다? 단어가 틀렸거나, 입력한 알파벳이 단어 안에 없을 때
        chance -= 1  # 기회 줄어듦

    if flag == True and goal <= 0:
        result = cast

    return word_temp

def collect_clients():
    print('Server waiting for clients')
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(10)

    while not gamestart:
        connectionSock, addr = serverSock.accept()
        print('client connected: ', str(addr))
        t = threading.Thread(target=client_manager,args = (connectionSock, addr))
        t.start()

    print("player collection complete")

def ready_check(connectionSock):
    global turn
    localturn = turn
    try:
        recvData = connectionSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
    except ConnectionResetError:  # 강제 종료 발생 시
        print('client 강제 종료,  클라이언트 나가기 처리')  # 나중에 멀티 클라 상황일 때 추가 핸들링 구현
        return FAIL

    if len(recvData) > 0:  # null이 아니면
        recvData = recvData.rstrip('\n')  # 개행문자 떼고

        if recvData == 'ready':  # ready면
            localturn = turn  # 바꾸고
        elif recvData == 'exit':
            localturn = FAIL
            connectionSock.close()  # 나간다하면 보내줌

        recvData = recvData.rstrip('\n')  # 개행문자 떼고
    return localturn

def name_check(connectionSock):# 클라 이름 입력 받음
    recvData = "defaultName"
    try:
        recvData = connectionSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
    except ConnectionResetError:  # 강제 종료 발생 시
        print('client 강제 종료,  클라이언트 나가기 처리')  # 나중에 멀티 클라 상황일 때 추가 핸들링 구현
        return FAIL

    if len(recvData) > 0:  # null이 아니면
        recvData = recvData.rstrip('\n')  # 개행문자 떼고
    else:
        return FAIL

    return recvData

def start_check():
    global gamestart
    while not gamestart:
        clientnum = len(clients)
        print("clientnum = ", clientnum, " ready = ", turn)
        if clientnum > 0 and clientnum == turn:
            gamestart = True
            print("game started, players : ",  clientnum)
        else:
            time.sleep(1)

def send_formal_data(n, sock):
    global chance
    global word_now
    global result

    sendData = str(n) + '/' + str(chance) + '/' + word_now + '/' + str(result)
    print(sendData)
    sock.send(sendData.encode('utf-8'))

# 메인
while True:
    gamestart = False
    t = threading.Thread(target=start_check)
    t.start()

    t = threading.Thread(target=collect_clients)
    t.start()
    # 모든 클라이언트 이름 보내기

    while not gamestart:
        time.sleep(1)
    print("game started")
    initgame()

    nameList = '/'.join(name for name, sock in clients)
    i = 0
    turn = 0
    for name, sock in clients:
        sendData = nameList + '/' + str(i)
        print(sendData)
        sock.send(sendData.encode('utf-8'))
        if i != turn:
            send_formal_data(-1, sock)
        i += 1

    beforeturn = turn
    while gamestart:
        if turn != beforeturn:
            print("turn ", turn)
            beforeturn = turn
            n, s = clients[beforeturn]
            for name, sock in clients:
                if sock != s:
                    send_formal_data(-1, sock)

    break