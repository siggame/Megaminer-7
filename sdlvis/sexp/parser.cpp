#include "parser.h"

#include <cstdlib>
#include <cstring>
#include <cassert>

#include "lex.yy.h"

#define END 0
#define STRING 1
#define TOKEN 2
#define LPAREN 3
#define RPAREN 4

static YY_BUFFER_STATE* buffer = NULL;

static char* unescapeString(const char* string)
{
  char* result = NULL;
  
  int size = 0;
  for(int i = 1; string[i]; i++)
  {
    if(string[i] == '\\' && (string[i+1] == '\\' || string[i+1] == '"'))
      i++;
    
    size++;
  }
  size--;
  result = new char[size+1];
  
  int index = 0;
  for(int i = 1; string[i]; i++)
  {
    if(string[i] == '\\' && (string[i+1] == '\\' || string[i+1] == '"'))
    {
      result[index++] = string[i+1];
      i++;
    }
    else
    {
      result[index++] = string[i];
    }
  }
  result[index-1] = 0;
  
  assert(index == size+1);
  
  return result;
}

static char* copyString(const char* string)
{
  int length = strlen(string);
  char* copy = new char[length+1];
  memcpy(copy, string, length);
  copy[length] = 0;
  return copy;
}

Sexp* parseList()
{
  Sexp* ret = new Sexp;
  ret->val = NULL;
  ret->list = NULL;
  ret->next = NULL;
  Sexp* last = NULL;
  Sexp* next = NULL;
  
  int t = yylex();
  while(true)
  {
    if(t == RPAREN || t == END)
    {
      return ret;
    }
    
    if(t == TOKEN)
    {
      next = new Sexp;
      next->val = copyString(yytext);
      next->next = NULL;
      next->list = NULL;
    }
    
    if(t == STRING)
    {
      next = new Sexp;
      next->val = unescapeString(yytext);
      next->next = NULL;
      next->list = NULL;
    }
    
    if(t == LPAREN)
    {
      next = parseList();
    }
    
    if(!last)
    {
      ret->list = next;
    }
    else
    {
      last->next = next;
    }
    last = next;
    t = yylex();
  }
}

Sexp* parse()
{
  Sexp* ret;
  int t = yylex();
  if(t == TOKEN)
  {
    ret = new Sexp;
    ret->val = copyString(yytext);
    ret->next = NULL;
    ret->list = NULL;
  }
  
  else if(t == STRING)
  {
    ret = new Sexp;
    ret->val = unescapeString(yytext);
    ret->next = NULL;
    ret->list = NULL;
  }
  
  else if(t == LPAREN)
  {
    ret = parseList();
  }
  
  else
  {
    ret = NULL;
  }
  
  return ret;
}

void parseFile(FILE* in)
{
  YY_BUFFER_STATE* tmp =  new YY_BUFFER_STATE;
  *tmp = yy_create_buffer(in, YY_BUF_SIZE);
  yy_switch_to_buffer(*tmp);
  if(buffer)
    yy_delete_buffer(*buffer);
    delete buffer;
  buffer = tmp;
}