#include "sfcompat.h"
#include "parser.h"

#include "lex.yy.h"

void destroy_sexp(Sexp* s)
{
  destroySexp(s);
}

Sexp* extract_sexpr(const char* in)
{
  Sexp* ret;
  yy_scan_string(in);
  ret = parse();
  yypop_buffer_state();
  return ret;
}

int sexp_list_length(Sexp* s)
{
  int length = 0;
  Sexp* child = s->list;
  while(child)
  {
    length++;
    child = child->next;
  }
  return length;
}