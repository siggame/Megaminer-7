#ifndef SEXP_SFCOMPAT_H
#define SEXP_SFCOMPAT_H

#include "sexp.h"

typedef Sexp sexp_t;

void destroy_sexp(Sexp*);

Sexp* extract_sexpr(const char*);

int sexp_list_length(Sexp*);

#endif