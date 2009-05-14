#coding:utf-8
import hashlib
import os
def hash_path(key,path_prefix):
    '''
    return the real hash path
    '''
    md5_hash=hashlib.md5(key).hexdigest()
    dir_hash=path_prefix+md5_hash[0:2]+"/"+md5_hash[2:4]
    return dir_hash+"/"+md5_hash+".doc"
def hash_write(key,txt,path_prefix):
    ''' save the document to hard disk
    hash files ,not in single directory
        '''
    md5_hash=hashlib.md5(key).hexdigest()
    dir_hash=path_prefix+md5_hash[0:2]+"/"+md5_hash[2:4]
    file_name=dir_hash+"/"+md5_hash+".doc"
    if not os.path.isdir(dir_hash):
        os.system("mkdir -p "+dir_hash)
    try:
        f=open(file_name,"w")
        f.write(txt)
        f.close()
    except:
        pass
def hash_read(key,path_prefix):
    ''' read file from disk,realpath has been hashed.'''
    md5_hash=hashlib.md5(key).hexdigest()
    dir_hash=path_prefix+md5_hash[0:2]+"/"+md5_hash[2:4]
    file_name=dir_hash+"/"+md5_hash+".doc"
    if not os.path.exists(file_name):
        return None
    try:
        f=open(file_name,"r")
        txt=f.read()
        f.close()
        return txt
    except:
        return None
        pass
