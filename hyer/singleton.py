#coding:utf-8
import thread
class Singleton(object):
    '''Implement Pattern: SINGLETON
        Example code:
        class S2(MySingletonClass):
            d=""
            def hello(self):
                print id(self);
            def __init__(self,helo):
                self.d=helo
                print "S2.__init__ called,arg helo:",helo

        v1=S2("godo1")
        print v1.d
        v2=S2("godo2")
        print v2.d
        print id(v1)
        print id(v2)
        print v1.d
    '''

    __lockObj = thread.allocate_lock()  # lock object
    __instance = None  # the unique instance

    def __new__(cls, *args, **kargs):
        return cls.getInstance(cls, *args, **kargs)

    def __init__(self):
        pass
    def singletonInit(self):
        print "method ",self.__class__,".singletonInit() called"
    def getInstance(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        # Critical section start
        cls.__lockObj.acquire()
        try:
            if cls.__instance is None:
                # (Some exception may be thrown...)
                # Initialize **the unique** instance
                cls.__instance = object.__new__(cls)

                '''Initialize object **here**, as you would do in __init__()...'''
        finally:
            #  Exit from critical section whatever happens
            cls.__lockObj.release()
        # Critical section end

        return cls.__instance
    getInstance = classmethod(getInstance)

