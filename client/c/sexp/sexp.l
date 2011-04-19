%option noyywrap

%{
#ifndef YYSTYPE
#define YYSTYPE int
#endif
#define END 0
#define STRING 1
#define TOKEN 2
#define LPAREN 3
#define RPAREN 4

#include <iostream>
using namespace std;

%}  

%%

L?\"(\\.|[^\\"])*\"  {return STRING;}
[^ \t\n\r()"\\]+        {return TOKEN;}
[ \t\n\r]            {}
\(                   {return LPAREN;}
\)                   {return RPAREN;}
<<EOF>>              {return END;}

%%
