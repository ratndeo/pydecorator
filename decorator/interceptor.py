# A decorator class to intercept after or before of original obj method call
class Decorator(object):
    class Executor(object):
        def __init__(self, f,  before_f=None , after_f=None ):
            self.f = f
            self.before_f = before_f
            self.after_f = after_f

        def __call__(self, *args, **kwargs):
            if self.before_f:
                self.before_f(context_args=args, context_kwargs = kwargs)
            result = self.f(*args, **kwargs)

            if self.after_f:
                self.after_f(context_args = args, context_kwargs = kwargs)
            return result

    def __init__(self, obj, after_f=None, before_f=None, excludes=[]):
        object.__setattr__(self, "obj",obj)
        object.__setattr__(self, "before_f", before_f)
        object.__setattr__(self,"after_f", after_f)
        object.__setattr__(self,"excludes", excludes)

    def __getattr__(self, item):
        original_attr = getattr(self.obj,item)
        if callable(original_attr):
            return Decorator.Executor(original_attr, after_f=self.after_f, before_f= self.before_f)
        else:
            return original_attr

    def __setattr__(self, key, value):
        return setattr(self.obj,key, value)


# Creates interceptor Decorator
# to use
# @decorator(before_f=f1)
# class A
#   pass
def decorator(before_f=None, after_f=None, excludes=[]):
    def factorty(cls):
        def inner(*arg, **kwargs):
            return Decorator(cls(*arg, **kwargs), after_f=after_f, before_f=before_f,excludes=excludes)
        return inner
    return factorty
