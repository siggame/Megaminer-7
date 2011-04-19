//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef NETWORK_H
#define NETWORK_H

#include "sexp/sfcompat.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifdef __cplusplus
extern "C"
{
#endif
  DLLEXPORT int open_server_connection(const char* host, const char* port);
  DLLEXPORT int send_string(int socket, const char* payload);
  DLLEXPORT char* rec_string(int socket);
  
  DLLEXPORT char* escape_string(const char* string);
#ifdef __cplusplus
}
#endif
#endif

