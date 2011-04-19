#ifndef SEXP_SEXP_H
#define SEXP_SEXP_H

#include <iostream>

struct Sexp
{
  char* val;
  Sexp* list;
  Sexp* next;
  
  friend std::ostream& operator <<(std::ostream &,const Sexp &);
};

void destroySexp(Sexp*);

#endif