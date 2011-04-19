#include "sexp.h"

std::ostream& operator <<(std::ostream &os,const Sexp &obj)
{
  if(obj.val)
    os << obj.val;
  else if(obj.list)
  {
    Sexp* child = obj.list;
    os << "( ";
    while(child)
    {
      os << *child << " ";
      child = child->next;
    }
    os << " )";
  }
  return os;
}

void destroySexp(Sexp* s)
{
  Sexp* next;
  while(s)
  {
    if(s->val)
    {
      delete[] s->val;
    }
    if(s->list) destroySexp(s->list);
    next = s->next;
    delete s;
    s = next;
  }
}