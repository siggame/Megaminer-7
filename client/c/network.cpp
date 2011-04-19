//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <assert.h>

#ifdef _WIN32
#include <winsock2.h>
#pragma comment(lib, "Ws2_32.lib")
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#define SOCKET_ERROR -1
#endif

#include "network.h"

#define GLOBAL_BUFFER_SIZE 512

using namespace std;

static int sock_server;

/*                                networking functions                          */
DLLEXPORT int open_server_connection(const char* host, const char* port)
{
    struct sockaddr_in addr;

#ifdef WIN32
    WSADATA wsaData;
    WSAStartup( MAKEWORD( 2, 2 ), &wsaData );
#endif
    sock_server = socket(AF_INET, SOCK_STREAM, 0);

    if(sock_server == SOCKET_ERROR )
    {
        cerr << "Error creating socket" << endl;
        return -1;
    }

    char* address = strdup(host);

    if(strchr(address, ':'))
    {
      port = strchr(address, ':') + 1;
      *strchr(address, ':') = 0;
    }

    // cover our DNS lookup stuff:
    struct hostent *h;
    if((h = gethostbyname( address )) == NULL)
    {
        cerr << "Unable to lookup host: " << host << endl;
        free(address);
        return -1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(port));
    addr.sin_addr = *((struct in_addr *)h->h_addr);
    memset(addr.sin_zero, '\0', sizeof(addr.sin_zero) );

    free(address);

    if( connect(sock_server, (struct sockaddr *)&addr, sizeof(addr) ) == SOCKET_ERROR)
    {
        cerr <<  "Unable to open socket!" << endl;
        cerr << "Couldn't connect to " << host << endl;
#ifdef WIN32
        cerr << "Windows Error " << WSAGetLastError() << endl;
#endif
        return -1;
    }
    return sock_server;
}


DLLEXPORT int send_string(int socket, const char* payload) {

#ifdef SHOW_NETWORK
    cout << "C: " << payload << endl;
#endif

    // this function only supports the fake 'no compression' scheme

    char buffer[GLOBAL_BUFFER_SIZE];
    int numbytes = strlen(payload)+1;
    char * cstr = new char[numbytes]; //payload + \0
    
    memset(cstr, 0, numbytes);
    strcat(cstr, payload);
    
    int offset = 0;

    // add our packet header
    int msg_len = numbytes-1;

    int n_msg_len = htonl(msg_len);

    // first, send the payload size (4 bytes)
   int val = send(socket, (char*)&n_msg_len, 4, 0);
    if( val != 4)
    {
        cerr << "Connection broken." << endl;
        cerr << "Sent: " << val << endl;
        delete[] cstr;
        return -1;
    }

    // now, keep sending chunks of the payload
    // until we send the whole thing
    

    while(offset < msg_len)
    {
        // we can't copy GLOBAL_BUFFER_SIZE bytes each time,
        // because that might push us past the end of cstr.
        // figure out which is smaller, GLOBAL_BUFFER_SIZE
        // or (payload.length() - offset)
        int bytes_to_copy = min(GLOBAL_BUFFER_SIZE, msg_len - offset );
        memcpy((void*)&buffer, (void*)(cstr+offset), bytes_to_copy);

        if((numbytes = send(socket, buffer, bytes_to_copy, 0)) == -1)
        {
            cerr << "Error sending data to  server!" << endl;
            delete[] cstr;
            return -1;
        }

        // update the offset to copy from
        offset += numbytes;
    }
    
    delete[] cstr;
    return 0;

}


// Takes the socket connected to the server, reads
// the network packet format, and extracts the payload
// as a string.
DLLEXPORT char* rec_string(int socket)
{
    char* ret = NULL;
    
    char buffer[GLOBAL_BUFFER_SIZE];
    int numbytes = 0;
    string result = "";
    int msg_len = -1;
    int bytes_to_read = 0;
    int bytes_left_to_read = 0;

    // first, receive the payload size (4 bytes)
    numbytes = recv(socket, (char*)&msg_len, 4, 0);
    if( numbytes == 0)
    {
        cerr << "Disconnected from server!" << endl;
        // we've been disconnected, there's no point in going on
        exit(0);
    }
    // get this out of network byte order
    //memcpy((void*)&msg_len, (void*)&buffer, 4);
    msg_len = ntohl(msg_len);

    bytes_left_to_read = msg_len;


    while(bytes_left_to_read > 0)
    {
        numbytes = 0;
        bytes_to_read = min(GLOBAL_BUFFER_SIZE-1, bytes_left_to_read);

        if((numbytes = recv(socket, buffer, bytes_to_read, 0)) == -1) {
            cerr << "Error reading data from server!" << endl;
            return 0;
        }

        if(numbytes == 0)
        {
            cerr << "Disconnected from server!" << endl;
            // we've been disconnected, there's no point in going on
            exit(0);
        }

        bytes_left_to_read -= numbytes;

        buffer[numbytes] = '\0';
        result += buffer;
    }

#ifdef SHOW_NETWORK
    cout << "S: " << result.c_str() << endl;
#endif
    ret = new char[result.size()+1];
    strncpy(ret, result.c_str(), result.size());
    ret[result.size()] = 0;
    return ret;
}

/*                                      sexpr functions                                       */

DLLEXPORT char* escape_string(const char* string)
{
  char* result = NULL;
  
  int size = 0;
  for(int i = 0; string[i]; i++)
  {
    size++;
    if(string[i] == '\\' || string[i] == '"')
      size++;
  }
  result = new char[size+1];
  
  int index = 0;
  for(int i = 0; string[i]; i++)
  {
    if(string[i] == '\\' || string[i] == '"')
    {
    result[index++] = '\\';
    }
    result[index++] = string[i];
  }
  result[index] = 0;
  
  assert(index == size);
  
  return result;
}

