#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib,"Ws2_32.lib")

#define BUF_SIZE 1024
void error_handling(char *message);
char* drawHangman(int num);
void print_turn(char *player[], char *turn);
//void print_player(char *player[], int i);

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
	//servAddr.sin_addr.s_addr = inet_addr("118.45.154.188");

	servAddr.sin_port = htons(atoi("45454"));

	if (connect(hSocket, (struct sockaddr*)&servAddr, sizeof(servAddr)) == -1)
		error_handling("connect() error!");
	else
		puts("Connected...........\n게임에 입장합니다. \n");
	/*
	printf("다른 player들의 입장을 기다립니다........\n");              
	*/
	
	memset(token_player, '\0', sizeof(token_player));

	recv_len = recv(hSocket, token_player, BUF_SIZE, 0);
	//
	if (recv_len == -1 || recv_len == 0)
	{
		printf("서버로부터 player 리스트 받기 실패\n");
		exit(1);
	}

	printf("당신은 player %s입니다.\n", token_player);

	recv_len = 0;

	while (1)
	{
		recv_len = 0;
		memset(user_info, '\0', sizeof(message));
		recv_cnt = recv(hSocket, user_info, BUF_SIZE, 0);
		if (recv_cnt == -1)
			error_handling("read() error!");
		else if (recv_cnt == 0)
			printf("No data received\n");
		recv_len += recv_cnt;
		
		//printf("일단 확인하기 위해서%s\n", user_info);
		turn = strtok_s(user_info, "/", &chanceStr);
		chanceStr = strtok_s(chanceStr, "/", &word_now);
		word_now = strtok_s(word_now, "/", &tf);
		printf("%s\n", drawHangman(atoi(chanceStr)));
		printf("남은 기회 : %d \n", atoi(chanceStr));
		printf("%s\n", word_now);


		if (strcmp(tf, token_player) == 0)
			printf("\n정답 입니다.\n");
		else if(strcmp(tf,token_player)!=0 &&strcmp(tf,token_player)!=-1)
			printf("\n%s가 정답을 맞추었습니다.", tf);

		print_turn(token_player, turn);

		if (strcmp(turn, token_player) == 0)
		{
			printf("게임을 시작하겠습니다. \n");
			puts("단어 혹은 알파벳을 입력하세요 : ");
			fgets(message, BUF_SIZE, stdin);

			//if (strcmp(message, "\n") == 0)
				//continue;
			str_len = send(hSocket, message, strlen(message), 0);
		}


	
	}
	closesocket(hSocket);
	WSACleanup();
	return 0;
}

/*
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
*/
void print_turn(char *player, char *turn)
{

	if (strcmp(turn, "-1") == 0)
		printf("게임이 종료되었습니다.\n");
	printf("\n-----------------------------------\n");
	if (strcmp(player, turn) == 0)
		printf("나의 차례입니다.\n");
	else
		printf("player %s의 차례입니다. 대기하세요\n",turn);
	
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



