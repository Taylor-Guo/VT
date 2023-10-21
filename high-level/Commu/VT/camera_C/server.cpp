#include <iostream>
#include <unistd.h>
#include <cstring>
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <thread>
#include <opencv2/opencv.hpp>
using namespace cv; 
using namespace std; 
#define USEPORT 1234
#define T 20
Mat FRAME; 
Point PCENTER; 

//灰度重心法函数
Point gray_center(Mat& img)
{
	Mat img_gray; 
	cvtColor(img, img_gray, COLOR_BGR2GRAY); // Change from COLOR_BGR2GRAY, 0 to just COLOR_BGR2GRAY
	Point Center; 
	double sumval = 0; 

	for (int i = 0; i < img_gray.cols; i++)
	{
		for (int j = 0; j < img_gray.rows; j++)
		{
			double s = img_gray.at<uchar>(j, i); 
			if (s < T)
				s = 0; 
			sumval += s; 
		}
	}

	Center.x = Center.y = 0;
	double x = 0, y = 0;

	for (int i = 0; i < img_gray.cols; i++){
		for (int j = 0; j < img_gray.rows; j++)
		{
			double s = img_gray.at<uchar>(j, i); 
			if (s < T)
				s = 0; 
			x += i * s / sumval;
			y += j * s / sumval;
		}}
	return Center;
}

//摄像头图像处理
void cam_stand_by(){
	VideoCapture capture; 
	if (!capture.isOpened())
	{
		cout << "fail to open camera!" << endl; 
		exit(-1); 
	}

	while (1)
	{
		capture >> FRAME; 
		PCENTER = gray_center(FRAME); 
		if (waitKey(30) >= 0)
			break; 
	}
}

int main(){
	//开启一个线程，并将其分离,使不阻塞主程序
	thread cam_th(cam_stand_by); 
	cam_th.detach(); 

	//启动服务端
	int serverSock = socket(AF_INET, SOCK_STREAM, 0); 
	if (serverSock < 0)
	{
		cout << "socket creation failed" << endl; 
		exit(-1); 
	}
	cout << "socket creation successfully" << endl; 

	struct sockaddr_in serverAddr; 
	memset(&serverAddr, 0, sizeof(serverAddr)); 
	serverAddr.sin_family = AF_INET; 
	serverAddr.sin_port = htons(USEPORT); 
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY); 

	if (bind(serverSock, 
		(struct sockaddr*)&serverAddr, 
		sizeof(struct sockaddr)) == -1)
	{
		cout << "Bind error, Port["<< USEPORT << "]" << endl; 
		exit(-1); 
	}

	cout << "Bind successfully" << endl; 

	if (listen(serverSock, 10) == -1)
	{
		cout << "Listen error!" << endl; 
	}

	cout << "Listening on port[" << USEPORT << "]" << endl; 
		while (1)
	{
		struct sockaddr clientAddr; 
		socklen_t size = sizeof(struct sockaddr); // Added "socklen_t"
		int clientSock = accept(serverSock, (struct sockaddr*)&clientAddr, &size); // Removed (socklen_t*)
		cout << "\n****NEW client touched****" << endl; 

		while (1)
		{
			if (send(clientSock, FRAME.data, FRAME.total()*FRAME.elemSize(), 0) < 0)
				break;  

			send(clientSock, &PCENTER, sizeof(Point), 0); 
		}

		cout << "\n==== CLIENT BREAK ====" << endl; 
		close(clientSock); 
	}

	close(serverSock); 
	return 0; 
}
