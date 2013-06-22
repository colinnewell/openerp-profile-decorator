openerpprofiledecorator
================================

A quick profiling decorator designed to work with OpenERP
and it's logging.

This is for use by developers to generate cProfile profiling
data.  It writes the profile files to /tmp with filenames 
starting openerp-profile with the extension .profile.  It also 
makes use of the OpenERP log to log when it saves the profile to
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

Once the decorator is in place and you are running openerp look
for the debug messages in the log,

    2013-06-22 13:00:27,906 1135 DEBUG ? openerp.netsvc.rpc.response: object.execute_kw time:0.016s [29]
    2013-06-22 13:00:27,907 1135 DEBUG ? openerp.netsvc.rpc.request: object.execute_kw('minimal',
    2013-06-22 13:00:27,907 1135 DEBUG ? openerp.netsvc.rpc.request:                   1,
    2013-06-22 13:00:27,907 1135 DEBUG ? openerp.netsvc.rpc.request:                   '*',
    2013-06-22 13:00:27,907 1135 DEBUG ? openerp.netsvc.rpc.request:                   'ir.attachment',
    2013-06-22 13:00:27,907 1135 DEBUG ? openerp.netsvc.rpc.request:                   'read',
    2013-06-22 13:00:27,907 1135 DEBUG ? openerp.netsvc.rpc.request:                   ([29],
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                    ['name', 'url', 'type'],
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                    {'department_id': False,
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                     'lang': 'en_GB',
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                     'section_id': False,
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                     'tz': False,
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                     'uid': 1}),
    2013-06-22 13:00:27,908 1135 DEBUG ? openerp.netsvc.rpc.request:                   {})
    2013-06-22 13:00:27,910 1135 DEBUG ? openerp.osv.osv: <strong>Profile stats saved to /tmp/openerp-profile-1371906027.910166-Thread-16.profile</strong>
    2013-06-22 13:00:27,911 1135 DEBUG ? openerp.netsvc.rpc.response: object.execute_kw time:0.004s [{'id': 29, 'name': u'SO007.pdf', 'type': u'binary', 'url': False}]

I personally like to examine the profiles using [kcachegrind] [2] by 
using [pyprof2calltree] [3] to convert the files to a format it understands.

    pyprof2calltree -i /tmp/openerp-profile-1371906027.910166-Thread-16.profile -k

--------------------------------

This decorator is based on an [answer] [1] on stackoverflow.

[1]: http://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result "Stackoverflow answer"
[2]: http://kcachegrind.sourceforge.net/html/Home.html "KCachegrind"
[3]: https://pypi.python.org/pypi/pyprof2calltree/ "pyprof2calltree"
