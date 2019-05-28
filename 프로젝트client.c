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
	int recv_len;
	int str_len;
	int recv_cnt = 0;
	char *chanceStr, *word_now;
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
		hangman = "忙式式式忖\n弛\n弛\n弛\n弛\n戌式式式式式式\n";
		break;
	case 6:
		hangman = "忙式式式忖\n弛﹛∞\n弛\n弛\n弛\n戌式式式式式式\n";
		break;
	case 5:
		hangman = "忙式式式忖\n弛﹛∞\n弛﹛ |\n弛\n弛\n戌式式式式式式\n";
		break;
	case 4:
		hangman = "忙式式式忖\n弛﹛∞\n弛﹛/|\n弛\n弛\n戌式式式式式式\n";
		break;
	case 3:
		hangman = "忙式式式忖\n弛﹛∞\n弛﹛/|′\n弛﹛\n弛\n戌式式式式式式\n";
		break;
	case 2:
		hangman = "忙式式式忖\n弛﹛∞\n弛﹛/|′\n弛﹛/\n弛\n戌式式式式式式\n";
		break;
	case 1:
		hangman = "忙式式式忖\n弛﹛∞\n弛﹛/|′\n弛﹛/′\n弛\n戌式式式式式式\n";
		break;
	case 0:
		hangman = "忙式式式忖\n弛﹛∞\n弛﹛ X\n弛﹛/|′\n弛﹛/′\n戌式式式式式式\n";
		break;
	default:
		hangman = "drawing error\n";
		break;
	}
	return hangman;
}



