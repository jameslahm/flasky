from functools import wraps
from ..models import Permission
from .errors import forbidden
from flask import g

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args,**kwargs)
        return decorated_function
    return decorator