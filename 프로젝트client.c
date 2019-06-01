#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib,"Ws2_32.lib")

#define BUF_SIZE 1024
void error_handling(char *message);
char* drawHangman(int num);
void print_turn(char *player[], char *turn, int i);
void print_player(char *player[], int i);

int main(int argc, char *argv[])
{
	WSADATA wsaData;
	SOCKET hSocket;
	SOCKADDR_IN servAddr;
	char message[BUF_SIZE], user_info[BUF_SIZE];
	char user_name[20],ch;	//player name
	char *temp,*k; //username에서 \n때기 위해서
	char *tf, *chanceStr, *word_now;
	char *turn;
	char token_player[BUF_SIZE], *players[3];
	int recv_len;
	int str_len;
	int recv_cnt = 0;

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		error_handling("WSAStartup() error!");

	hSocket = socket(PF_INET, SOCK_STREAM, 0);
	if (hSocket == -1)
		error_handling("socket() error");

	memset(&servAddr, 0, sizeof(servAddr));
	servAddr.sin_family = AF_INET;
	servAddr.sin_addr.s_addr = inet_addr("155.230.28.129");
	servAddr.sin_port = htons(atoi("45454"));

	if (connect(hSocket, (struct sockaddr*)&servAddr, sizeof(servAddr)) == -1)
		error_handling("connect() error!");
	else
		puts("Connected...........\n");


	printf("player 이름을 입력해주세요 :");
	fgets(user_name, sizeof(user_name), stdin);
	temp = strtok_s(user_name, "\n", &k);

	printf("게임이 준비된 클라이언트는 'r'을 입력, 불참을 원하시면 'e'를 입력해주세요\n\n");
	ch = getchar();

	while (1)
	{
		getchar();
		if (ch == 'r')
		{
			//str_len = send(hSocket, "ready", strlen("ready"), 0);
			str_len = send(hSocket, user_name, strlen(user_name), 0);
			//getchar();
			break;
		}
		else if (ch == 'e')
		{
			str_len = send(hSocket, "exit", strlen("exit"), 0);
			printf("종료하겠습니다.\n");
			closesocket(hSocket);
			WSACleanup();
			return 0;
		}
		else
		{
			printf("'r'또는 'e'만 입력해주세요\n");
			ch = getchar();

		}
	}

	memset(token_player, '\0', sizeof(token_player));
	printf("다른 player들의 입장을 기다립니다........\n");
	              
	recv_len = recv(hSocket, token_player, BUF_SIZE, 0);
	//printf("%s", token_player);
	if (recv_len == -1 || recv_len == 0)
	{
		printf("서버로부터 player 리스트 받기 실패\n");
		//exit(1);
	}


	/*
	클라이언트 플레이어 수 반복으로 돌리자

	*/

	players[0] = strtok_s(token_player, "/", &players[1]);
	players[1] = strtok_s(players[1], "/", &players[2]);
	print_player(players, 3);
	/*
	참가 user 출력
	recv
	//'/'로 parsing
	//player[]에 저장
//	print
	*/
	//	ch = getchar();
	memset(user_info, '\0', sizeof(message));
	recv_len = 0;

	while (1)
	{
		recv_len = 0;
		//str_len = 0;
		while (recv_len < str_len)
		{
			recv_cnt = recv(hSocket, &user_info[recv_len], BUF_SIZE, 0);

			if (recv_cnt == -1)
				error_handling("read() error!");
			recv_len += recv_cnt;
		}
		
		turn = strtok_s(user_info, "/", &chanceStr);

		chanceStr = strtok_s(chanceStr, "/", &word_now);
		

		word_now = strtok_s(word_now, "/", &tf);
		if (strcmp(tf, user_name) == 0)
			printf("당신의 승리입니다.\n");
		else if (strcmp(tf, "0") != 0)
			printf("%s의 승리입니다.", tf);
	

		printf("남은 기회 : %d \n", atoi(chanceStr));
		printf("%s\n", word_now);

		//printf("%s", tf);


		printf("%s\n", drawHangman(atoi(chanceStr)));
		print_turn(players, turn, 3);

		if (strcmp(turn, temp) == 0)	//본인이름과 server가 보낸 turn 비교해서 같으면 진행
		{
			printf("게임을 시작하겠습니다. 종료하시고 싶으시면 'exit'를 입력해주세요\n");
			puts("단어 혹은 알파벳을 입력하세요 : ");
			fgets(message, BUF_SIZE, stdin);
	
			if (strcmp(message, "\n") == 0)
				continue;

			if (!strcmp(message, "exit\n") || (!strcmp(message, "EXIT\n")))
			{
				//str_len = send(hSocket, message, strlen(message), 0);
				break;
			}

			str_len = send(hSocket, message, strlen(message), 0);
		}
		else
		    printf("당신의 turn이 아닙니다. turn이 돌아올때까지 대기해주세요\n");

		
	}

	closesocket(hSocket);
	WSACleanup();
	return 0;
}

void print_player(char *player[], int i)
{

	//int i;
	printf("\n---------list of players---------\n");
	for (i = 0; i < 3; i++)
	{

		printf("%s\n", player[i]);
	}
	printf("-----------------------------------\n");
}

void print_turn(char *player[], char *turn, int i)
{
	//int i;
	printf("\n------------현재 turn------------\n");

	for (i = 0; i < 3; i++)
	{
		//strcat(player[i], "\n");
		if (strcmp(turn, player[i]) == 0)
			printf("%s<-\n", player[i]);
		else
			printf("%s\n", player[i]);
	}
	printf("-----------------------------------\n");

}


void error_handling(char *message)
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}


char* drawHangman(int num) {
	char* hangman = { 0 };
	switch (num)
	{
	case 7:
		hangman = "┌───┐\n│\n│\n│\n│\n└──────\n";
		break;
	case 6:
		hangman = "┌───┐\n│　○\n│\n│\n│\n└──────\n";
		break;
	case 5:
		hangman = "┌───┐\n│　○\n│　 |\n│\n│\n└──────\n";
		break;
	case 4:
		hangman = "┌───┐\n│　○\n│　/|\n│\n│\n└──────\n";
		break;
	case 3:
		hangman = "┌───┐\n│　○\n│　/|＼\n│　\n│\n└──────\n";
		break;
	case 2:
		hangman = "┌───┐\n│　○\n│　/|＼\n│　/\n│\n└──────\n";
		break;
	case 1:
		hangman = "┌───┐\n│　○\n│　/|＼\n│　/＼\n│\n└──────\n";
		break;
	case 0:
		hangman = "┌───┐\n│　○\n│　 X\n│　/|＼\n│　/＼\n└──────\n";
		break;
	default:
		hangman = "drawing error\n";
		break;
	}
	return hangman;
}



