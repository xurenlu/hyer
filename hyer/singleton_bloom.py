import thread

import hyer.singleton

import hyer.vendor.bloom

class SingletonBloom(hyer.singleton.Singleton):
    __lockObj = thread.allocate_lock()  # lock object
    __bloom=hyer.vendor.bloom.Bloom(1024,6)
    def exists(self,k):
        return k in self.__bloom
    def add(self,k):
        self.__lockObj.acquire()
        try:
            self.__bloom.add(k)
        except:
            pass
        self.__lockObj.release()
SingletonBloomObject=SingletonBloom()
def exists(k):
    return SingletonBloom.exists(SingletonBloom(),k)
def add(k):
    return SingletonBloom.add(SingletonBloom(),k)

def test():
    assert exists("http://www.sohu.com")==False
    assert add("http://www.sohu.com")==None
    assert exists("http://www.sohu.com")==True
if __name__ == "__main__":
    test()
