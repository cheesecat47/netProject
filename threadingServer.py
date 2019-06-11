from socket import *
import threading
import time
import random

# 상수
NOBODY = -1
GAME_WRONG = 0
GAME_CORRECT = 1
GAME_WIN = 2
GAME_LOST = 3
CLIENTS_MIN = 4

# 소켓 변수
port = 45454

# 시스템 처리 변수
clients = list()  # 클라 배열
CLIENTS_LIST_LOCKED = False

# 게임 관련 변수
tries_left = 7
word = 'test'  # 단어는 나중에 랜덤 선택.
word_now = ''  # 게임 중에 보여줄 문자열
goal = 4  # * 맞춰야하는 알파벳 수
turn = NOBODY
result = NOBODY
game_updated = True


def game_reset():
    global tries_left
    global word
    global goal
    global word_now
    global result
    global game_updated

    tries_left = 7
    word = get_random_word()
    goal = len(word)  # * 맞춰야할 단어의 길이 체크
    word_now = ''
    for _ in word:
        word_now += '_ '  # 처음엔 빈 칸으로 초기화, word 길이만큼 _ _ _ _ _
    result = NOBODY
    game_updated = True


def get_random_word():
    # 미구현
    return 'apple'


def game_set_random_turn():
    global turn
    global clients
    # 미구현
    clients_number = len(clients)
    if clients_number > 0:
        turn = random.randrange(clients_number)


def game_word_check(input):
    global tries_left
    global word
    global goal
    global word_now

    check_result = GAME_WRONG

    word_temp = ''
    flag_found = False  # 새로운 알파벳 있는지 확인하기 위해

    # 알파벳인지 단어인지 구별
    # 단어일 때
    if input == word:
        flag_found = True
        goal = 0  # * 한꺼번에 맞췄을경우 전부 제거
        for i in range(len(word)):
            word_temp += word[i] + ' '  # 알파벳 띄어쓰기 포함해서 붙임

    # 알파벳일 때
    elif input != word:
        for i in range(len(word)):
            if input == word[i]:  # 알파벳 같은게 있으면
                if input in word_now:  # * ch가 이미 나왔을경우
                    word_temp += word_now[i * 2] + ' '  # * 알파벳 똑같을때랑 똑같이 처리
                else:
                    word_temp += input + ' '  # 알파벳 붙이고
                    flag_found = True  # 새로운게 있다고 알림
                    goal -= 1  # * 그리고 정답 체크
            else:  # 알파벳 다르면
                word_temp += word_now[i * 2] + ' '  # 이전에 그 자리에 있던 거 붙임.

    if flag_found:
        check_result = GAME_CORRECT
        if goal <= 0:
            check_result = GAME_WIN
    else:
        # 바뀐게 없다? 단어가 틀렸거나, 입력한 알파벳이 단어 안에 없을 때
        tries_left -= 1  # 기회 줄어듦
        if tries_left <= 0:
            check_result = GAME_LOST

    return word_temp, check_result


def clients_accept():
    global CLIENTS_LIST_LOCKED
    print('Server waiting for clients')
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(10)
    while True:
        connectionSock, addr = serverSock.accept()
        print('client connected: ', str(addr))
        if CLIENTS_LIST_LOCKED:
            connectionSock.close()
            print('access denied')
            continue
        CLIENTS_LIST_LOCKED = True
        clients_number = len(clients)
        clients.append((clients_number, connectionSock))
        print("client entry ", clients_number, " socket info : ", connectionSock)
        CLIENTS_LIST_LOCKED = False


def clients_notify():
    global tries_left
    global word_now
    global result
    global clients
    global game_updated
    global turn

    if not game_updated:
        return False
    need_to_reset = False
    remove_list = list()

    if turn == NOBODY:
        client_index = NOBODY
    else:
        client_index, client_socket = clients[turn]

    sendData = str(client_index) + '/' + str(tries_left) + '/' + word_now + '/' + str(result)
    for index, sock in clients:
        print(sendData, " index = ", index)
        try:
            sock.send(sendData.encode('utf-8'))
        except ConnectionResetError:
            remove_list.append((index, sock))
            continue

    for i in range(len(remove_list)):
        clients.remove(remove_list[i])
        need_to_reset = True

    return need_to_reset


def clients_take_turn(client_index, connectionSock):
    global word_now
    global game_updated
    global result

    print("[", client_index, "] 의 차례.")
    try:
        recvData = connectionSock.recv(40).decode('utf-8')  # 문자열로 입력 받음
    except ConnectionResetError:  # 강제 종료 발생 시
        print('client 강제 종료, 게임 종료하기')  # 나중에 멀티 클라 상황일 때 추가 핸들링 구현
        return True

    if len(recvData) > 0:  # null이 아니면
        recvData = recvData.rstrip('\n')  # 개행문자 떼고

        if recvData == 'exit':
            print('client sent exit message')
            connectionSock.close()
            return True

        word_now, check_result = game_word_check(recvData)  # 체크

        game_updated = True
        if check_result == GAME_WIN:
            result = client_index
            return True
        elif check_result == GAME_LOST:
            return True

        print('recvData: ', recvData, 'word_now: ', word_now, ' chance left: ', str(tries_left))

    elif len(recvData) == 0:
        return True
    return False


# 메인
t = threading.Thread(target=clients_accept)
t.start()

new_game = True

game_reset()
game_set_random_turn()
while True:
    if CLIENTS_LIST_LOCKED:
        continue
    CLIENTS_LIST_LOCKED = True
    clients_number = len(clients)
    if clients_number < CLIENTS_MIN:
        print("error : 클라이언트가 부족합니다. clients_number = ", clients_number)
        CLIENTS_LIST_LOCKED = False
        time.sleep(0.5);
        new_game = True
        continue

    if new_game:
        new_game = False
        for name, sock in clients:
            sendData = str(name)
            print(sendData)
            sock.send(sendData.encode('utf-8'))
        game_set_random_turn()

    if clients_notify():
        print("error : 클라이언트 연결이 끊겼습니다.")
        CLIENTS_LIST_LOCKED = False
        continue
    if turn >= 0 and turn < clients_number:
        client_index, client_socket = clients[turn]
        game_end = clients_take_turn(client_index, client_socket)
        if game_end:
            turn = NOBODY
            clients_notify()
            game_reset()
            game_set_random_turn()
        else:
            turn = (turn + 1) % clients_number
    else:
        print("error : 누구도 턴을 받을 수 없습니다. turn = ", turn)
    CLIENTS_LIST_LOCKED = False
