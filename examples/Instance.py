import thread
class MySingletonClass(object):
    '''Implement Pattern: SINGLETON'''

    __lockObj = thread.allocate_lock()  # lock object
    __instance = None  # the unique instance

    def __new__(cls, *args, **kargs):
        return cls.getInstance(cls, *args, **kargs)

    def __init__(self):
        pass

    def getInstance(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        # Critical section start
        cls.__lockObj.acquire()
        try:
            if cls.__instance is None:
                # (Some exception may be thrown...)
                # Initialize **the unique** instance
                cls.__instance = object.__new__(cls, *args, **kargs)

                '''Initialize object **here**, as you would do in __init__()...'''

        finally:
            #  Exit from critical section whatever happens
            cls.__lockObj.release()
        # Critical section end

        return cls.__instance
    getInstance = classmethod(getInstance)

v1=MySingletonClass()
v2=MySingletonClass()
print id(v1)
print id(v2)
