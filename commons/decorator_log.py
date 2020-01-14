from functools import wraps
from commons.make_log import get_logger
import traceback

def logs(func):
    @wraps(func)
    def log(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            fun_name = func.__name__
            error = traceback.format_exc()
            get_logger().error("%s--%s" %(fun_name,error))
    return log