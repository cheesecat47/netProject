#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib,"Ws2_32.lib")

#define BUF_SIZE 1024
void error_handling(char *message);
char* drawHangman(int num);

int main(int argc, char *argv[])
{

	char message[BUF_SIZE];
	char message2[BUF_SIZE];
	char user_name[20];
	char ch;
	int recv_len;
	int str_len;
	int recv_cnt = 0;
	char *tf,*chanceStr, *word_now;
	WSADATA wsaData;
	SOCKET hSocket;
	SOCKADDR_IN servAddr;
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
		puts("Connected...........");


	printf("player 이름을 입력해주세요 :");
	fgets(user_name, sizeof(user_name), stdin);

	printf("준비된 클라이언트는 'r'을 입력,게임에 불참을 원하시면 'e'를 입력해주세요\n");
	if (ch = getchar() == 'r')
	{
		str_len = send(hSocket, "ready", strlen("ready"), 0);
	}
	else if  (ch = getchar() == 'e')
	{
		str_len = send(hSocket, "exit", strlen("exit"), 0);
	}

	memset(message2, '\0', sizeof(message));
	recv_len = 0;
	while (1)
	{
		puts("input message(0 to q): ");
		fgets(message, BUF_SIZE, stdin);
		//message[1] = "";
		
		if (!strcmp(message, "exit\n") || (!strcmp(message, "EXIT\n")))
			break;

		str_len = send(hSocket, message, strlen(message), 0);

		recv_len = 0;
		while (recv_len < str_len)
		{
			recv_cnt = recv(hSocket, &message2[recv_len], BUF_SIZE, 0);

			if (recv_cnt == -1)
				error_handling("read() error!");
			recv_len += recv_cnt;
		}
	
		chanceStr = strtok_s(message2, "/",&word_now);
		word_now = strtok_s(word_now, "/", &tf);

		printf("%s", tf);
		printf("from server : %d",atoi(chanceStr));
	//arsing = strtok(NULL, )

			printf("%s\n", word_now);
			
			printf("%s\n", drawHangman(atoi(chanceStr)));
	}

	closesocket(hSocket);
	WSACleanup();
	return 0;
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



