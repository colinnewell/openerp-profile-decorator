# based on answer from stack overflow
# http://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result
import cProfile
import threading
import time
import os

def profileit(log):
    def valid_filename():
        fname = "/tmp/openerp-profile-%f-%s.profile" % (time.time(), threading.current_thread().name)
        i = 2
        while os.path.exists(fname):
            fname = "/tmp/openerp-profile-%f-%s-%d.profile" % (time.time(), threading.current_thread().name, i)
            i+=1
        return fname


    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            fname = valid_filename()
            prof.dump_stats(fname)
            # make sure you turn on --log-level=debug
            log.debug("Profile stats saved to %s" % fname)
            return retval
        return wrapper
    return inner
