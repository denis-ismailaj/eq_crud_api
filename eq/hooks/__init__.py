from functools import wraps

from . notification import notify_change

def post_notify(func):
    @wraps(func)
    def wrapper(*args, **kwargs): 
        notify_change()
        
        return func(*args, **kwargs)

    return wrapper

