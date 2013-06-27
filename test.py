from stackdecorator import debugstacktrace
from openerpprofiledecorator import profileit

class Log(object):

    def debug(self, msg):
        print msg

logger = Log()

class Test(object):

    @debugstacktrace(logger)
    @profileit(logger)
    def mymethod(self, name):
        print "Hello %s" % name

if __name__ == '__main__':
    o = Test()
    o.mymethod('programmer')

