import traceback

def debugstacktrace(log):

    def inner(func):

        def wrapper(*args, **kwargs):
            log.debug('start stack trace')
            for line in traceback.format_stack():
                log.debug(line.strip())
            log.debug('end stack trace')
            retval = func(*args, **kwargs)
            return retval

        return wrapper

    return inner

