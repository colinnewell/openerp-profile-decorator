# based on answer from stack overflow
# http://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result
import cProfile
import threading
import time
import os

def profileit(log, timer=None):
    """
    A quick profiling decorator designed to work with OpenERP
    and it's logging.

    It writes the profile files to /tmp with filenames starting
    openerp-profile with the extension .profile.  It also makes
    use of the OpenERP log to log when it saves the profile to
    help you tie up which action corresponds to which profile.

    To make the most of the logging it is suggested you run with,

        --log-response --log-request and --log-level=debug

    To profile all calls to execute you can make a temporary
    modification to osv.py like this for example,

        --- a/osv/osv.py
        +++ b/osv/osv.py
        @@ -36,6 +36,7 @@ import openerp.exceptions
         
         import time
         import random
        +from openerpprofiledecorator import profileit
         
         _logger = logging.getLogger(__name__)
         
        @@ -176,6 +177,7 @@ class object_proxy(object):
         
                 return wrapper
         
        +    @profileit(_logger)
             def execute_cr(self, cr, uid, obj, method, *args, **kw):
                 object = pooler.get_pool(cr.dbname).get(obj)
                 if not object:

    """
    def valid_filename():
        fname = "/tmp/openerp-profile-%f-%s.profile" % (time.time(), threading.current_thread().name)
        i = 2
        while os.path.exists(fname):
            fname = "/tmp/openerp-profile-%f-%s-%d.profile" % (time.time(), threading.current_thread().name, i)
            i+=1
        return fname


    def inner(func):
        def wrapper(*args, **kwargs):
            prof_kws = {}
            if timer is not None:
                # Note passing None to timer results in TypeError "NoneType object is not callable" warnings
                # hence use of prof_kws dictionary
                prof_kws['timer'] = timer
            prof = cProfile.Profile(**prof_kws)
            retval = prof.runcall(func, *args, **kwargs)
            fname = valid_filename()
            prof.dump_stats(fname)
            # make sure you turn on --log-level=debug
            log.debug("Profile stats saved to %s" % fname)
            return retval
        return wrapper
    return inner
