# aspects.py - Tools for AOP in Python
# Version 1.3
#
# Copyright (C) 2003-2008 Antti Kervinen (ask@cs.tut.fi)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
Aspects library allows wrapping and removing wraps on methods and
functions. Wraps are functions which are called before the wrapped
functions. A wrap may or may not call the wrapped function at some
point of their execution.

There are two kinds of wraps: new-style and old-style. New-style wraps
can be used in Python 2.5 and later, old-style wraps work in Python
2.1 and later. Support for old-style wraps is continued for
compatibility reasons, but they will be deprecated when stable Python
2.5 compatible Jython is released. For instance, arbitrary old-style
wraps cannot be removed.

1. Wrapping a method or function:

   new-style: wrap_ids = aspects.with_wrap(new_style_wrap, func1, ...)

              funcs can be in module-level or in class-level (that is,
              a method)

   old-style: wrap_id = aspects.wrap_around(method, old_style_wrap)

              method cannot be a module-level function

   In both cases, adding 'instances=[obj1, obj2, ...]' keyword
   argument causes the wrap to be executed only in the case that it is
   called through objects obj1, obj2, etc.

   wrap_around and with_wrap return identifiers for the added wraps
   (or a list of identifiers if many functions are wrapped at once in
   with_wrap). The identifiers can be used in enabling and disabling
   the wrap.

   There can be a number of wraps on the same function. When it is
   called, the topmost wrap is executed first and the wrap below is
   executed when the wrap above tries to call the original
   function. There can be both old-style and new-style wraps on the
   same function.

2. Removing a wrap:

   removed_wrap = aspects.without_wrap(new_style_wrap, method)

   or

   removed_wrap = aspects.without_wrap(wrap_id, method)

   Removed wraps can be rewrapped to the same or other methods.

   For compatibility, there is the peel_around method for removing the
   topmost wrap. It should not be used anymore.

   topmost_wrap = aspects.peel_around(func)

3. Enabling / disabling a wrap:

   both styles: enable_wrap(func, wrap_id) enables the wrap
                disable_wrap(func, wrap_id) disables the wrap
                wrap_is_enabled(func, wrap_id) returns the status

   Only enabled wraps are executed when the function is called.

4. New-style wraps

   New-style wraps are generators. Inside a wrap, the original
   function can be called with the original call arguments:

   orig_retval = yield aspects.proceed

   or with new arguments:

   orig_retval = yield aspects.proceed(args_here)

   If wanted, the original function can be called many times.
   Exceptions raised by the original method can be caught in the wrap
   if the yield statement is inside a try-except block.

   The wrap passes the original return value by default (if it does
   not yield anything but aspects.proceed), or by yielding

   yield aspects.return_stop

   The return value can be changed by yielding

   yield aspects.return_stop(value_here)

   Yielding return_stop with a new return value before the original
   method is executed causes skipping the execution.

   If the value is returned by either of the above ways, the execution
   of the wrap is restarted when the wrapped function is called next
   time. However, the value can also be returned with return_cont. In
   that case, the execution of the wrap is not restarted, which
   results in remarkably faster execution.

   (args, kw_args) = yield aspects.return_cont

   returns the original return value, and

   (args, kw_args) = yield aspects.return_cont(value_here)

   returns the given value. When the wrapped function is called next
   time, the call arguments are stored to args and kw_args, and the
   execution of the wrap is continued from the yield point.

   The wrap can access the wrapped method by yielding get_wrapped
   class.

   wrapped_method = yield get_wrapped
"""

version_info=(1,3)

import re

import thread

import types

import inspect

import sys
_python_version=sys.version_info[:2]

_permission_to_touch_wraps=thread.allocate_lock()

class AspectsException(Exception):
    pass

if _python_version < (2,3):
    class object: pass

class proceed(object):
    """
    Yielding a proceed object from a generator advice causes
    (re)invokation of the wrapped function with the given arguments.
    """
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs

class return_stop(object):
    """
    Yielding a return_stop object from a generator advice causes passing
    the given argument as a return value to the caller of the wrapped
    function.
    """
    def __init__(self,retval):
        self.retval=retval

class return_cont(object):
    """
    Yielding a return_cont object from a generator advice causes
    passing the given argument as a return value of the original
    method to the caller. The execution of the advice will be
    continued from the yield point when the wrapped function is called
    next time.
    """
    def __init__(self,retval):
        self.retval=retval

class get_wrapped(object):
    """
    Yielding a get_wrapped_function class from a generator advice causes
    the wrapped function object to be sent to the advice.
    """
    pass

def wrap_around_re(aClass, wildcard, advice):
    """
    Same as wrap_around but works with regular expression based
    wildcards to map which methods are going to be used.
    """
    matcher = re.compile(wildcard)
    for aMember in dir(aClass):
        realMember = getattr(aClass, aMember)
        if callable(realMember) and aMember[:6]!="__wrap" and \
           aMember[:9]!="__proceed" and \
           matcher.match(aMember):
            wrap_around(realMember, advice)

def with_wrap(advice, *methods, **kwargs):
    insts = kwargs.get('instances', [])
    retval = []
    for m in methods:
        if getattr(m, 'im_self', None) != None:
            # Method m is a bound method. It will be wrapped equally
            # to the corresponding unbound method with argument
            # instances=[m.im_self].
            try:
                unbound_m = getattr(m.im_class, m.im_func.func_name)
            except:
                raise AspectsException("Could not find the unbound version of method %s" % (m,))
            retval.append(_with_wrap(advice, unbound_m, instances=[m.im_self]))
        else: 
            # Method m is a function or an unbound method.
            retval.append(_with_wrap(advice, m, instances=insts))
    if len(retval) == 1:
        return retval[0]
    else:
        return retval

_next_wrap_id = 0

def _with_wrap(advice, method, instances=[]):
    """
    with_wrap wraps the execution of method inside given
    generator. When the method is called, the generator is invoked
    with the parameters the method call contains. If the generator
    yields, the yielded values define the new parameters to the
    method. The return value of the method is sent to the generator
    with .send method. If then generator yields again, the yielded
    value is passed as a return value that the caller of the method
    sees. If it does not, the return value is passed to the caller as
    is.

    If the first yield returns None instead of a pair of new
    arguments, the arguments are given to the original method.

    Usage:

    >>> def g_adv(*args,**kwargs):
    ...     print 'g_adv received arguments',args,kwargs
    ...     retval = yield aspects.proceed
    ...     print 'method returned',retval
    ...     yield aspects.return_stop(retval + 1)
    ...
    >>> class c:
    ...     def inc(number):
    ...         return number+1
    ...
    >>> aspects.with_wrap(c.inc, g_adv)
    >>> o=c()
    >>> o.inc(41)
    g_adv received arguments ((41,), {})
    method returned 42
    43
    """

    global _next_wrap_id

    _permission_to_touch_wraps.acquire()

    wrap_id = _next_wrap_id
    _next_wrap_id += 1
        
    methods_name = method.__name__

    orig_method = method

    # Information on the original method and the advice will be
    # plugged to the new method (that is, the new middleman) later on.
    new_method = _create_middleman()

    try: 
        # Older Pythons do not accept try-except-finally, so there is
        # outer try-finally here just to make sure that
        # _permission_to_touch_wraps lock will be released
        try:
            # Already wrapped method's namespace can be found from
            # aspects-orig-method-namespace
            replace_method = getattr(method, '__aspects_rmf')
        except AttributeError:
            if hasattr(method, 'im_class'): # is this a method of a class?
                replace_method = \
                    lambda orig, new: setattr(method.im_class, orig, new)
            elif hasattr(method, 'func_globals'): # is this a normal function?
                replace_method = \
                    lambda orig, new: method.func_globals.__setitem__(orig, new)
            else:
                m = inspect.getmodule(method.__module__)
                if m == None:
                    if method.__module__ in ['nt', 'posix']:
                        # os module has funny names, but we need to
                        # modify the dict of os module, not nt's or posix's.
                        m = __import__('os', [], [], '')
                    else: 
                        # sometimes inspect fails to return a module
                        m = __import__(method.__module__, [], [], '')
                if not type(m) == types.ModuleType:
                    raise AspectsException("Module of %s not found" % (method,))
                replace_method = \
                    lambda orig, new: m.__dict__.__setitem__(orig, new)
    
        replace_method(methods_name, new_method)
        new_method.__name__ = method.__name__
        new_method.__aspects_wrapid = wrap_id
        new_method.__aspects_rmf = replace_method
        new_method.__aspects_cont = None # generator to be continued
        new_method.__aspects_instances = set([id(i) for i in instances])
        new_method.__aspects_enabled = 1
        new_method.__aspects_orig = orig_method
        new_method.__aspects_adv = advice
        return wrap_id
    finally: _permission_to_touch_wraps.release()


def _create_middleman():
    def generator_middleman(*args,**kwargs):
        # Generator_advice is not executed if the advice is not
        # enabled or if we are dealing with an incorrect instance
        method = generator_middleman.__aspects_orig
        if generator_middleman.__aspects_enabled==0 or \
           (generator_middleman.__aspects_instances and not
            id(args[0]) in generator_middleman.__aspects_instances):
            return method(*args,**kwargs)
        generator_advice = generator_middleman.__aspects_adv
        # If a generator is waiting for call, continue its execution
        # with send(). Otherwise, create a new generator advice.
        
        if generator_middleman.__aspects_cont==None:
            g=generator_advice(*args,**kwargs)
            if type(g)!=types.GeneratorType:
                raise AspectsException("Advice is not a generator")
            try: rv=g.next()
            except StopIteration: return None
        else:
            g=generator_middleman.__aspects_cont
            generator_middleman.__aspects_cont=None
            try: rv=g.send((args,kwargs))
            except StopIteration: return None
            
        # Continue execution in the generator to the first yield.
        # yielded value => affect
        
        # proceed (class) => wrapped method is called with orig
        # parameters, may raise exceptions

        # proceed (object) => wrapped method is called with given
        # parameters, may raise exceptions
        
        # return_stop (class) => the return value of the original
        # method is passed to the caller. Execution of the generator
        # advice starts from the beginning when the method is called
        # next time.

        # return_stop (object) => the given return value is passed to
        # the caller. Execution of the generator advice starts from
        # the beginning when the method is called next time.

        # return_cont (class) => the return value of the original
        # method is passed to the caller. Execution of the generator
        # advice continues from the yielding row when the method is
        # called next time.

        # return_cont (object) => the given return value is passed to
        # the caller. Execution of the generator advice continues from
        # the yielding row when the method is called next time.

        # get_wrapped (class) => sends the lower level wrap to the current wrap

        # FUTURE DEVELOPMENT
        # getorig (class) => sends the original method to the wrap

        orig_retval_available=0
        while 1:
            # Reset the arguments for the original method, if new ones are
            # given with yield
            if rv==proceed:
                pass # args and kwargs are as they are
            elif type(rv)==proceed:
                args,kwargs=rv.args,rv.kwargs
            elif rv==return_stop:
                if orig_retval_available==0:
                    raise AspectsException("Original return value not available.")
                return method_rv
            elif type(rv)==return_stop:
                return rv.retval
            elif rv==return_cont:
                if orig_retval_available==0:
                    raise AspectsException("Original return value not available.")
                generator_middleman.__aspects_cont=g
                return method_rv
            elif type(rv)==return_cont:
                generator_middleman.__aspects_cont=g
                return rv.retval
            elif rv==get_wrapped:
                try: rv=g.send(method)
                except StopIteration: return None
                continue
            else:
                raise AspectsException("Advice yielded an illegal value: '%s'" % str(rv))
            # Call the original method. Its return value will be sent to
            # the generator. If the method raises an exception, the same
            # exception is raised in the generator.
            method_rv=None
            try:
                method_rv=method(*args,**kwargs)
                orig_retval_available=1
                raised_exception=None
            except Exception,e:
                raised_exception=e
                # last orig method call did not return a value:
                orig_retval_available=0
            # Continue execution in the generator advice by sending it the
            # return value or raising the catched exception. 
            try:
                if not raised_exception: rv=g.send(method_rv)
                else: rv=g.throw(e)
            except StopIteration:
                return method_rv
    # end of generator_middleman
    return generator_middleman
    
            
def wrap_around(method, advice, instances=[]):
    """
    This function will be deprecated.

    wrap_around wraps an unbound method (the first argument)
    inside an advice (function given as the second argument). When the
    method is called, the code of the advice is executed to the point
    of 'self.__proceed(*args,**keyw)'. Then the original method is
    executed after which the control returns to the advice.

    Keyword parameter instances is a container. When it is not empty,
    it specifies a set of id:s of instances with which the advice is
    executed. If the wrapped method is bound to an instance not in the
    set, the advice is omitted.

    Returns the number of the added wrap. The number can be used later
    on for enabling and disabling the wrap.
    """
    _permission_to_touch_wraps.acquire()
    try:
        methods_name, methods_class, _ = _names_mce(method)

        if methods_name[:2]=="__" and not hasattr(methods_class,methods_name):
            methods_name="_"+methods_class.__name__+methods_name

        # Check if __proceed method is implemented in the class
        try:
            getattr(methods_class,'__proceed')
        except:
            setattr(methods_class, '__proceed_stack', _proceed_stack_method)
            setattr(methods_class,'__proceed', _proceed_method)

        # Check how many times this method has been wrapped
        methodwrapcount = wrap_count(method)

        # Rename the original method: it will be __wrapped/n/origmethodname
        # where /n/ is the number of wraps around it
        wrapped_method_name = "__wrapped" + str(methodwrapcount) + methods_name
        orig_method = getattr( methods_class, methods_name)
        setattr(methods_class, wrapped_method_name, orig_method)

        # Add the wrap (that is, the advice) as a new method
        wrapper_method_name = "__wrap" + str(methodwrapcount) + methods_name
        setattr(methods_class, wrapper_method_name, advice)

        # Add __wrap_enabled/n/methodname attribute that is used for
        # enabling and disabling the wrap on the fly. By default the wrap
        # is enabled.
        enabled_attr_name = "__wrap_enabled" + str(methodwrapcount) + methods_name
        setattr(methods_class, enabled_attr_name, 1)

        # Generate condition: should this wrap be executed when the method is called
        cond_execute_wrap="self." + enabled_attr_name
        if len(instances)>0:
            instanceids_attr_name="__wrap_instanceids"+str(methodwrapcount)+methods_name
            if _python_version >= (2,4):
                setattr(methods_class,instanceids_attr_name,set([id(i) for i in instances]))
            else: # slower implementation for older pythons
                setattr(methods_class,instanceids_attr_name,[id(i) for i in instances])
            cond_execute_wrap="("+cond_execute_wrap+")" + \
                               "and (id(self) in self."+instanceids_attr_name+")"

        # Replace the original method by a method that
        # 1) sets which method should be executed in the next proceed call
        # 2) calls the wrap (advice)

        new_code = "def " + methods_name + "(self,*args,**keyw):\n" +\
                   "\tif not (" + cond_execute_wrap + "):\n" +\
                   "\t\treturn self." + wrapped_method_name + "(*args,**keyw)\n" +\
                   "\tstack=self.__proceed_stack()\n" +\
                   "\tstack.append( _Proceed_stack_entry(self." + wrapped_method_name + ",'" + methods_class.__name__ + "." + methods_name + "'))\n" +\
                   "\ttry: retval = self." + wrapper_method_name + "(*args,**keyw)\n" +\
                   "\tfinally:\n" +\
                   "\t\tstack.pop()\n" +\
                   "\t\tif len(stack)==0: _remove_proceed_stack(self)\n" +\
                   "\treturn retval\n"
        new_method = _create_function(new_code, methods_name)
        new_method.__aspects_wrapid=methodwrapcount
        new_method.__aspects_orig=orig_method
        # setattr(new_method,'__aspects_enabled',1)
        # new_method.__name__=methods_name
        setattr(methods_class, methods_name, new_method)
        return methodwrapcount
    finally: _permission_to_touch_wraps.release()

def without_wrap(advice_or_wrapid, method):
    _permission_to_touch_wraps.acquire()
    # 1. Search the wrap to be removed in the wrap stack
    #    and store it to the middleman variable
    if isinstance(advice_or_wrapid, int): # wrap is referenced by id
        # cannot use _find_wrap, because prev_middleman is needed, too
        wrapid = advice_or_wrapid
        prev_middleman = None
        middleman = method
        try:
            while middleman.__aspects_wrapid != wrapid:
                prev_middleman = middleman
                middleman = middleman.__aspects_orig
        except AttributeError:
            _permission_to_touch_wraps.release()
            raise AspectsException("Method '%s' has no wrap '%s'"
                                   % (method, wrapid))
    else: # removed wrap is referenced the advice function
        advice = advice_or_wrapid
        prev_middleman = None
        middleman = method
        try:
            while middleman.__aspects_adv != advice:
                prev_middleman = middleman
                middleman = middleman.__aspects_orig
        except AttributeError:
            _permission_to_touch_wraps.release()
            raise AspectsException("Method '%s' has no wrap '%s'"
                                   % (method, advice))
    retval = middleman.__aspects_adv

    # 2. Remove the current middleman
    if prev_middleman == None:
        # Must replace the method. This may be a poor solution,
        # because it may not change callbacks. A better solution might
        # be to switch the advice code between middlemen, keep the
        # topmost middleman the same, and remove the next middleman
        # from the chain.
        middleman.__aspects_rmf(middleman.__aspects_orig.__name__,
                                middleman.__aspects_orig)
    else:
        # Drop the middleman from the list.
        prev_middleman.__aspects_orig = middleman.__aspects_orig
    _permission_to_touch_wraps.release()
    return retval

def peel_around(method):
    """
    This function will be deprecated.

    Removes one wrap around the method (given as a parameter) and
    returns the wrap. If the method is not wrapped, returns None.
    """
    _permission_to_touch_wraps.acquire() # released in finally part
    try:
        if hasattr(method,'__aspects_enabled'): # new-style aspect, easy!
            method.__aspects_rmf(method.__name__,method.__aspects_orig)
            return method.__aspects_adv
        
        methods_name = method.__name__
        methods_class = method.im_class

        wc = wrap_count(method)-1

        if wc==-1: return None

        wrapped = getattr(methods_class, '__wrapped' + str(wc) + methods_name)
        setattr(methods_class, methods_name, wrapped)

        removed_adv = getattr(methods_class, '__wrap'+str(wc)+methods_name)
        del methods_class.__dict__['__wrapped'+str(wc)+methods_name]
        del methods_class.__dict__['__wrap'+str(wc)+methods_name]

        return removed_adv
    finally: _permission_to_touch_wraps.release()

def _find_wrap(method, wrap_number):
    wrapid = getattr(method, '__aspects_wrapid', None)
    while wrapid != wrap_number:
        if wrapid == None: 
            raise AspectsException("Wrap %s on method %s not found."
                                   % (wrap_number, method.__name__))
        method = method.__aspects_orig
        wrapid = getattr(method, '__aspects_wrapid', None)
    return method

def enable_wrap(method, wrap_number):
    wrap=_find_wrap(method, wrap_number)
    if hasattr(wrap,'__aspects_enabled'):
        setattr(wrap,'__aspects_enabled',1)
    else:
        _, methods_class, enabled_attr_name = _names_mce(method, wrap_number)
        setattr(methods_class, enabled_attr_name, 1)

def disable_wrap(method, wrap_number):
    wrap=_find_wrap(method, wrap_number)
    if hasattr(wrap,'__aspects_enabled'):
        setattr(wrap,'__aspects_enabled',0)
    else:
        _, methods_class, enabled_attr_name = _names_mce(method, wrap_number)
        setattr(methods_class, enabled_attr_name, 0)

def wrap_is_enabled(method, wrap_number):
    wrap=_find_wrap(method, wrap_number)
    if hasattr(wrap,'__aspects_enabled'):
        return getattr(wrap,'__aspects_enabled')
    else:
        _, methods_class, enabled_attr_name = _names_mce(method, wrap_number)
        return getattr(methods_class, enabled_attr_name)
    
def wrap_count(method):
    """
    Returns number of wraps around given method.
    """
    number = 0
    while hasattr(method, '__aspects_orig'):
        number += 1
        method = method.__aspects_orig
    return number

def _names_mce(method, wrap_number=None):
    """
    Returns triplet of names: Method, it's Class and wrap's Enabled
    attr name.  If enabled attr name does not exist (that is, there is
    no wrap wrap_number on the method), AspectsException is raised.
    """
    methods_name = method.__name__
    methods_class = method.im_class
    if wrap_number!=None:
        enabled_attr_name = "__wrap_enabled" + str(wrap_number) + methods_name
        if not hasattr(methods_class, enabled_attr_name):
            raise AspectsException("Method %s does not have wrap with number %s"
                                   % (methods_name, wrap_number))
    else: enabled_attr_name=None
    return methods_name, methods_class, enabled_attr_name


def _proceed_method(self, *args, **keyw):
    method=self.__proceed_stack()[-1].method
    return method(*args, **keyw)

def _remove_proceed_stack(self):
    stackname='__proceed_stack' + str(thread.get_ident())
    delattr(self,stackname)

def _proceed_stack_method(self):
    stackname='__proceed_stack' + str(thread.get_ident())
    try:
        return getattr(self,stackname)
    except:
        setattr(self,stackname,[])
        return getattr(self,stackname)

def _create_function(function_code, function_name, thread_lib=1):
    # import thread if it is required
    # if thread_lib and not 'thread' in globals(): import thread
    codeobj = compile(function_code, "", "exec")
    gl = {'_Proceed_stack_entry':_Proceed_stack_entry,
          '_remove_proceed_stack': _remove_proceed_stack}
    lo = {}
    exec(codeobj,gl,lo)
    return eval(function_name,gl,lo)

class _Proceed_stack_entry:
    def __init__(self, method, name):
        self.method = method
        self.name = name
