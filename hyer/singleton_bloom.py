import thread

import hyer.singleton

import hyer.vendor.bloom

class SingletonBloom(hyer.singleton.Singleton):

    __lockObj = thread.allocate_lock()  # lock object

    def __init__(self,index="default"):
        if not self.__dict__.has_key("__bloom"):
            self.__dict__["__bloom"]={}
        if not self.__dict__["__bloom"].has_key(index):
            self.__dict__["__bloom"][index]=hyer.vendor.bloom.Bloom(1024,6)
    def exists(self,k,index="default"):
        return k in self.__dict__["__bloom"][index]

    def add(self,k,index="default"):
        self.__lockObj.acquire()
        try:
            self.__dict__["__bloom"][index].add(k)
        except Exception,e:
            print "some thing error",e
            pass
        self.__lockObj.release()

def exists(k,index="default"):
    return SingletonBloom(index).exists(k,index)
def add(k,index="default"):
    return SingletonBloom(index).add(k,index)

def test():
    assert exists("http://www.sohu.com")==False
    assert add("http://www.sohu.com")==None
    assert exists("http://www.sohu.com")==True
#if __name__ == "__main__":
#    test()
