############################################################
#                                                          #
# The implementation of PHPRPC Protocol 3.0                #
#                                                          #
# phpformat.py                                             #
#                                                          #
# Release 3.0.2                                            #
# Copyright by Team-PHPRPC                                 #
#                                                          #
# WebSite:  http://www.phprpc.org/                         #
#           http://www.phprpc.net/                         #
#           http://www.phprpc.com/                         #
#           http://sourceforge.net/projects/php-rpc/       #
#                                                          #
# Authors:  Ma Bingyao <andot@ujn.edu.cn>                  #
#                                                          #
# This file may be distributed and/or modified under the   #
# terms of the GNU Lesser General Public License (LGPL)    #
# version 3.0 as published by the Free Software Foundation #
# and appearing in the included file LICENSE.              #
#                                                          #
############################################################
#
# PHP serialize/unserialize library.
#
# Copyright: Ma Bingyao <andot@ujn.edu.cn>
# Version: 1.2
# LastModified: Feb 27, 2009
# This library is free.  You can redistribute it and/or modify it.

import sys, os, inspect, datetime, types, fpconst, cStringIO

(__py_major__, __py_minor__) = sys.version_info[:2]
if (__py_major__ < 2) or ((__py_major__ == 2) and (__py_minor__ < 5)) :
    SEEK_CUR = 1
else :
    SEEK_CUR = os.SEEK_CUR

_classCache = {}

class SerializeError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def _serialize_int(i):
    return 'i:%s;' % i

def _serialize_long(i):
    #return 'i:%s;' % i if -2147483648 <= i <= 2147483647 else _serialize_string(str(i))
    if -2147483648 <= i <= 2147483647 :
        return 'i:%s;' % i 
    else :
        return _serialize_string(str(i))

def _serialize_float(d):
    if fpconst.isNaN(d):
        return 'd:NAN;'
    elif fpconst.isPosInf(d):
        return 'd:INF;'
    elif fpconst.isNegInf(d):
        return 'd:-INF;'
    else:
        return 'd:%s;' % d

def _serialize_string(s):
    return 's:%i:"%s";' % (len(s), s)

def _serialize_unicode_string(s):
    n = len(s)
    #return 'U:%i:"%s";'% (n, ''.join(
    #    (chr(ord(s[i]))
    #     if ord(s[i]) < 128
    #     else '\\%04x' % ord(s[i])
    #     for i in xrange(n))
    #))
    chars = []
    for i in xrange(n) :
        if ord(s[i]) < 128 :
            chars.append( chr(ord(s[i])) )
        else :
            chars.append( '\\%04x' % ord(s[i]) )

    return 'U:%i:"%s";'% (n, ''.join(chars))

def _serialize_datetime(dt, obj_container):
    obj_container.extend([None, None, None, None, None, None, None])
    out = []
    out.append(_serialize_string('year'))
    out.append(_serialize_int(dt.year))
    out.append(_serialize_string('month'))
    out.append(_serialize_int(dt.month))
    out.append(_serialize_string('day'))
    out.append(_serialize_int(dt.day))
    out.append(_serialize_string('hour'))
    out.append(_serialize_int(dt.hour))
    out.append(_serialize_string('minute'))
    out.append(_serialize_int(dt.minute))
    out.append(_serialize_string('second'))
    out.append(_serialize_int(dt.second))
    out.append(_serialize_string('millisecond'))
    out.append(_serialize_int(dt.microsecond // 1000))
    return 'O:11:"PHPRPC_Date":7:{%s}' % ''.join(out)

def _serialize_key(key):
    t = type(key)
    if ((t is types.IntType) or (t is types.BooleanType) or
        (t is types.LongType) and (-2147483648 <= key <= 2147483647)):
        return 'i:%i;' % key
    elif t is types.StringType:
        return 's:%i:"%s";' % (len(key), key)
    elif t is types.NoneType:
    	return 's:0:"";'
    else:
        key = str(key)
        return 's:%i:"%s";' % (len(key), key)

def _serialize_array(a, obj_container):
    return 'a:%i:{%s}' % (len(a),
        ''.join(('i:%i;%s' % (i, _serialize(a[i], obj_container))
        for i in xrange(len(a)))))

def _serialize_dict(d, obj_container):
    return 'a:%i:{%s}' % (len(d),
        ''.join(['%s%s' % (_serialize_key(key), _serialize(d[key], obj_container))
        for key in d.iterkeys()]))

def _serialize_object(obj, obj_container):
    name = []
    if obj.__class__.__module__ != '__main__':
        name.extend(obj.__class__.__module__.split('.'))
    name.append(obj.__class__.__name__)
    name = '_'.join(name)
    _classCache[name] = obj.__class__
    if hasattr(obj, 'serialize') and inspect.ismethod(obj.serialize):
        s = obj.serialize()
        return 'C:%i:"%s":%i:{%s}' % (len(name), name, len(s), s)
    __sleep = '_' + obj.__class__.__name__ + '__sleep'
    if hasattr(obj, __sleep):
        __sleep = getattr(obj, __sleep)
        if inspect.ismethod(__sleep):
            keys = __sleep()
            return 'O:%i:"%s":%i:{%s}' % (len(name), name, len(keys),
                ''.join(['%s%s' % (_serialize_key(key),
                _serialize(getattr(obj, key, None), obj_container))
                for key in keys]))
    data = vars(obj)
    return 'O:%i:"%s":%i:{%s}' % (len(name), name, len(data),
        ''.join(('%s%s' % (_serialize_key(key), _serialize(data[key], obj_container))
        for key in data)))

def _serialize(obj, obj_container):
    obj_id = len(obj_container)
    obj_container.append(None)
    t = type(obj)
    if t is types.NoneType:
        return 'N;'
    elif t is types.BooleanType:
        return 'b:%i;' % obj
    elif t is types.IntType:
        return _serialize_int(obj)
    elif t is types.LongType:
        return _serialize_long(obj)
    elif t is types.FloatType:
        return _serialize_float(obj)
    elif t is types.StringType:
        if obj in obj_container:
            return 'r:%i;' % obj_container.index(obj)
        else:
            obj_container[obj_id] = obj
            return _serialize_string(obj)
    elif t is types.UnicodeType:
        if obj in obj_container:
            return 'r:%i;' % obj_container.index(obj)
        else:
            obj_container[obj_id] = obj
            return _serialize_unicode_string(obj)
    elif t is datetime.datetime:
        if obj in obj_container:
            return 'r:%i;' % obj_container.index(obj)
        else:
            obj_container[obj_id] = obj
            return _serialize_datetime(obj, obj_container)
    elif (t is types.ListType) or (t is types.TupleType):
        if obj in obj_container:
            obj_container.pop
            return 'R:%i;' % obj_container.index(obj)
        else:
            obj_container[obj_id] = obj
            return _serialize_array(obj, obj_container)
    elif t is types.DictType:
        if obj in obj_container:
            obj_container.pop
            return 'R:%i;' % obj_container.index(obj)
        else:
            obj_container[obj_id] = obj
            return _serialize_dict(obj, obj_container)

    else:
        if obj in obj_container:
            return 'r:%i;' % obj_container.index(obj)
        else:
            obj_container[obj_id] = obj
            return _serialize_object(obj, obj_container)

def _get_class(name):
    name = name.split('.')
    if len(name) == 1:
        return getattr(sys.modules['__main__'], name[0], None)
    clsname = name.pop()
    modname = '.'.join(name)
    if sys.modules.has_key(modname):
        return getattr(sys.modules[modname], clsname, None)
    return None

def _get_class2(name, ps, i, c):
    if i < len(ps):
        p = ps[i]
        name = name[:p] + c + name[p + 1:]
        cls = _get_class2(name, ps, i + 1, '.')
        if (i + 1 < len(ps)) and (cls == None):
            cls = _get_class2(name, ps, i + 1, '_')
        return cls
    return _get_class(name)

def _get_class_by_alias(name):
    if _classCache.has_key(name):
        return _classCache[name]
    else:
        cls = getattr(sys.modules['__main__'], name, None)
        if not inspect.isclass(cls):
            ps = []
            p = name.find('_')
            while p > -1:
                ps.append(p)
                p = name.find('_', p + 1)
            cls = _get_class2(name, ps, 0, '.')
        if cls == None:
            cls = type(name, (), {})
        _classCache[name] = cls
        return cls

def _read_number(sio):
    num = []
    while True:
        c = sio.read(1)
        if (c == ':') or (c == ';'): break
        num.append(c)
    return ''.join(num)

def _unserialize_boolean(sio):
    sio.read(1)
    result = (sio.read(1) == '1')
    sio.read(1);
    return result;

def _unserialize_int(sio):
    sio.read(1)
    return int(_read_number(sio))

def _unserialize_double(sio):
    sio.read(1)
    d = _read_number(sio)
    if d == 'NAN':
        return fpconst.NaN
    elif d == 'INF':
        return fpconst.PosInf
    elif d == '-INF':
        return fpconst.NegInf
    elif ('.' in d) or ('e' in d) or ('E' in d):
        return float(d)
    else:
        return long(d)

def _unserialize_string(sio):
    len = _unserialize_int(sio)
    return sio.read(len + 3)[1:-2]

def _unserialize_escaped_string(sio):
    length = _unserialize_int(sio)
    s = []
    sio.read(1)
    for i in xrange(length):
        c = sio.read(1)
        if c == "\\":
            c = chr(int(sio.read(2), 16))
        s.append(c)
    sio.read(2)
    return ''.join(s)

def _unserialize_unicode_string(sio):
    length = _unserialize_int(sio)
    s = []
    sio.read(1)
    for i in xrange(length):
        c = sio.read(1)
        if c == "\\":
            c = unichr(int(sio.read(4), 16))
        s.append(c)
    sio.read(2)
    return u''.join(s)

def _unserialize_array(sio, obj_container):
    count = _unserialize_int(sio)
    obj = {}
    obj_container.append(obj)
    sio.read(1)
    for i in xrange(count):
        tag = sio.read(1)
        if tag == '':
            raise SerializeError('End of Stream encountered before parsing was completed.')
        elif tag == 'i':
            key = _unserialize_int(sio)
        elif tag == 's':
            key = _unserialize_string(sio)
        elif tag == 'S':
            key = _unserialize_escaped_string(sio)
        elif tag == 'U':
            key = _unserialize_unicode_string(sio)
        else:
            raise SerializeError('Unexpected Tag: "%c".' % tag)
        obj[key] = _unserialize(sio, obj_container)
    sio.read(1)
    return obj

def _unserialize_key(sio):
    tag = sio.read(1)
    if tag == '':
        raise SerializeError('End of Stream encountered before parsing was completed.')
    elif tag == 's':
        return _unserialize_string(sio)
    elif tag == 'S':
        return _unserialize_escaped_string(sio)
    elif tag == 'U':
        return _unserialize_unicode_string(sio)
    else:
        raise SerializeError('Unexpected Tag: "%c".' % tag)

def _unserialize_date(sio, obj_container):
    obj_id = len(obj_container)
    obj_container.append(None)
    h = {}
    count = _unserialize_int(sio)
    sio.read(1)
    for i in xrange(count):
        key = _unserialize_key(sio)
        h[key] = _unserialize(sio, obj_container)
    sio.read(1)
    dt = datetime.datetime(h['year'],
                           h['month'],
                           h['day'],
                           h['hour'],
                           h['minute'],
                           h['second'],
                           h['millisecond'] * 1000)
    obj_container[obj_id] = dt
    return dt

def _unserialize_object(sio, obj_container):
    classname = _unserialize_string(sio)
    sio.seek(-1, SEEK_CUR)
    if classname == 'PHPRPC_Date':
        return _unserialize_date(sio, obj_container)
    obj = _get_class_by_alias(classname)()
    obj_container.append(obj)
    count = _unserialize_int(sio)
    sio.read(1)
    for i in xrange(count):
        key = _unserialize_key(sio)
        if key[0] == '\0':
            key = key[key.find('\0', 1) + 1:]
        value = _unserialize(sio, obj_container)
        setattr(obj, key, value)
    sio.read(1)
    __wakeup = '_' + obj.__class__.__name__ + '__wakeup'
    if hasattr(obj, __wakeup):
        __wakeup = getattr(obj, __wakeup)
        if inspect.ismethod(__wakeup):
            __wakeup()
    return obj

def _unserialize_custom_object(sio, obj_container):
    classname = _unserialize_string(sio)
    sio.seek(-1, SEEK_CUR)
    obj = _get_class_by_alias(classname)()
    obj_container.append(obj)
    length = _unserialize_int(sio)
    s = sio.read(length + 2)[1:-1]
    if hasattr(obj, 'unserialize') and inspect.ismethod(obj.unserialize):
        obj.unserialize(s)
    else:
        obj.data = s
    return obj

def _unserialize(sio, obj_container):
    tag = sio.read(1)
    if tag == '':
        raise SerializeError('End of Stream encountered before parsing was completed.')
    elif tag == 'N':
        sio.read(1)
        obj = None
        obj_container.append(obj)
    elif tag == 'b':
        obj = _unserialize_boolean(sio)
        obj_container.append(obj)
    elif tag == 'i':
        obj = _unserialize_int(sio)
        obj_container.append(obj)
    elif tag == 'd':
        obj = _unserialize_double(sio)
        obj_container.append(obj)
    elif tag == 's':
        obj = _unserialize_string(sio)
        obj_container.append(obj)
    elif tag == 'S':
        obj = _unserialize_escaped_string(sio)
        obj_container.append(obj)
    elif tag == 'U':
        obj = _unserialize_unicode_string(sio)
        obj_container.append(obj)
    elif tag == 'r':
        obj = obj_container[_unserialize_int(sio) - 1]
        obj_container.append(obj)
    elif tag == 'R':
        obj = obj_container[_unserialize_int(sio) - 1]
    elif tag == 'a':
        obj = _unserialize_array(sio, obj_container)
    elif tag == 'O':
        obj = _unserialize_object(sio, obj_container)
    elif tag == 'C':
        obj = _unserialize_custom_object(sio, obj_container)
    else:
        raise SerializeError('Unexpected Tag: "%c".' % tag)
    return obj

def serialize(obj):
    '''Return the PHP-serialized representation of the object as a string.'''
    return _serialize(obj, [None])

def unserialize(s):
    '''Read a PHP-serialized object hierarchy from a string.'''
    sio = cStringIO.StringIO(s)
    result = _unserialize(sio, [])
    sio.close()
    return result

def dict_to_list(d):
    '''Converts an ordered dict into a list.'''
    try:
        return [d[x] for x in xrange(len(d))]
    except KeyError:
        raise ValueError('dict is not a sequence')


def dict_to_tuple(d):
    '''Converts an ordered dict into a tuple.'''
    return tuple(dict_to_list(d))

if __name__ == '__main__':
    class Test1(object):
        def __init__(self):
            self.xxx = 1
            self.xxxx = 3
    class Test2:
        def __init__(self):
            self.xxx = 'xxx'
            self.xxxx = 'xxxx'
        def serialize(self):
            print 'serialize'
            return ','.join([str(self.xxx), str(self.xxxx)])
        def unserialize(self, s):
            print 'unserialize'
            self.xxx, self.xxxx = s.split(',')
    class Test3:
        def __init__(self):
            self.xxx = 1.2
            self.xxxx = 2.3
        def __sleep(self):
            print '__sleep';
            return ('xxx', 'xxxx', 'xxxxx')
        def __wakeup(self):
            assert(self.xxx == 1.2)
            assert(self.xxxx == 2.3)
            assert(self.xxxxx == None)
            print '__wakeup'

    def test():
        assert(serialize(None) == 'N;')
        assert(serialize(True) == 'b:1;')
        assert(serialize(False) == 'b:0;')
        assert(serialize(1) == 'i:1;')
        assert(serialize(1L) == 'i:1;')
        assert(serialize(2147483647) == 'i:2147483647;')
        assert(serialize(-2147483648) == 'i:-2147483648;')
        assert(serialize(2147483647L) == 'i:2147483647;')
        assert(serialize(-2147483648L) == 'i:-2147483648;')
        assert(serialize(2147483648) == 's:10:"2147483648";')
        assert(serialize(-2147483649) == 's:11:"-2147483649";')
        assert(serialize(1.0) == 'd:1.0;')
        assert(serialize(0.0) == 'd:0.0;')
        assert(serialize(1e32) == 'd:1e+032;')
        assert(serialize(1e-32) == 'd:1e-032;')
        assert(serialize(fpconst.NaN) == 'd:NAN;')
        assert(serialize(fpconst.PosInf) == 'd:INF;')
        assert(serialize(fpconst.NegInf) == 'd:-INF;')
        assert(serialize('Hello!') == 's:6:"Hello!";')
        assert(unserialize(serialize(True)) == True)
        assert(unserialize(serialize(False)) == False)
        assert(unserialize(serialize(u'abc\u1234\u0092abc')) == u'abc\u1234\u0092abc')
        dt = datetime.datetime(2007, 12, 1, 12, 23, 23, 138343)
        assert(str(unserialize(serialize(dt))) == '2007-12-01 12:23:23.138000')
        assert(dict_to_tuple(unserialize(serialize((1,2,3,4,5)))) == (1,2,3,4,5))
        assert(dict_to_list(unserialize(serialize([1,2,3,4,5]))) == [1,2,3,4,5])
        assert(unserialize(serialize({'Hello': 'Hi', 'O': 'Hi'})) == {'Hello': 'Hi', 'O': 'Hi'})
        t1 = Test1()
        tt1 = unserialize(serialize(t1))
        assert(tt1.xxx == t1.xxx)
        assert(tt1.xxxx == t1.xxxx)
        assert(tt1.__class__ == t1.__class__)
        t2 = Test2()
        tt2 = unserialize(serialize(t2))
        assert(tt2.xxx == t2.xxx)
        assert(tt2.xxxx == t2.xxxx)
        assert(tt2.__class__ == t2.__class__)
        t3 = Test3()
        tt3 = unserialize(serialize(t3))
        assert(tt3.xxx == t3.xxx)
        assert(tt3.xxxx == t3.xxxx)
        assert(tt3.__class__ == t3.__class__)
    test()
