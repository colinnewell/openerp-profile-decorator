import traceback

def debugstacktrace(log):

    def inner(func):

        def wrapper(*args, **kwargs):
            for line in traceback.format_stack():
                log.debug(line.strip())
            retval = func(*args, **kwargs)
            return retval

        return wrapper

    return inner

