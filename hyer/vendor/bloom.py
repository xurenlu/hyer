#!/usr/bin/python
"""Bloom filters in Python, using SHA-1 and Python longs.

My first attempt stored the whole filter in a single arbitrary-size integer,
but for some reason that was 100x slower than storing it in a bunch of 256-bit
integers.
"""

#import sha
import hashlib

def nbits_required(n):
    """Bits required to represent any integer in [0, n)."""
    n -= 1
    rv = 0
    while n:
	n >>= 1
	rv += 1
    return rv

class Bloom:
    """Bloom filter: compact hash table for membership tests with false pos."""
    # default bits per bucket is 256 to cut down on pickle overhead
    def __init__(self, size, nhashes, bucketbits=256):
    	"""size: number of bits.  Should be a power of 2.
	nhashes: number of separate hashes to use.

	Making nhashes larger will make it slower.  There are also tradeoffs
	between size, performance, and false-positive rate, which you can look
	up elsewhere."""
	self.bucketbits = bucketbits
    	self.filter = [0L] * int((size + bucketbits - 1) / bucketbits)
	self.size = size
	self.nhashes = nhashes
	self.hashbits = nbits_required(size)
	assert self.hashbits * nhashes <= 160  # 160's all we get with SHA1
    def add(self, astr):
    	"""Add a string to the membership of the filter."""
    	for offset in self._hashes(astr):
	    bucket, bit = divmod(offset, self.bucketbits)
	    self.filter[bucket] |= (1L << bit)
    def __contains__(self, astr):
    	"""Returns true if the string is in the filter or it feels like it."""
    	for offset in self._hashes(astr):
	    bucket, bit = divmod(offset, self.bucketbits)
	    if not self.filter[bucket] & (1L << bit): return 0
	return 1
    def _hashes(self, astr):
    	"""The hashes of a particular string."""
    	digest = hashlib.sha1(astr).digest()
	# is there no better way to convert a byte string into a long?!
	hashlong = 0L
	for ch in digest: hashlong = (hashlong << 8) | ord(ch)
	rv = []
	mask = (1L << self.hashbits) - 1
	for ii in range(self.nhashes):
	    # Note that this will give substantially nonuniform results if
	    # self.size is not a power of 2, in order to avoid wasting hash
	    # bits or doing long division:
	    rv.append((hashlong & mask) % self.size)
	    hashlong >>= self.hashbits
	return rv

def test_bloom():
    """Very basic sanity test for Bloom filter implementation."""
    def ok(a, b): assert a == b, (a, b)
    ok(map(nbits_required, range(1, 10)), [0, 1, 2, 2, 3, 3, 3, 3, 4])
    ok(nbits_required(131072), 17)
    ok(nbits_required(131073), 18)

    b = Bloom(1024, 5)
    assert 'asdf' not in b
    assert 'fdsa' not in b
    b.add('asdf')
    assert 'asdf' in b
    assert 'fdsa' not in b

    # false positives (depends on hash function):
    x = Bloom(1024, 8)
    x.add('asdf') # about a 5% chance of false positives
    x.add('1') # about a 5% chance of false positives
    x.add('2') # about a 5% chance of false positives
    x.add('3') # about a 5% chance of false positives
    x.add('4') # about a 5% chance of false positives
    x.add('5') # about a 5% chance of false positives
    x.add('6') # about a 5% chance of false positives
    x.add('7') # about a 5% chance of false positives
    x.add('8') # about a 5% chance of false positives
    assert 'asdf' in x
    assert '1' in x
    assert '2' in x
    assert '3' in x
    assert '4' in x
    assert '5' in x
    assert '6' in x
    assert '7' in x
    assert '8' in x
    #ok(filter(x.__contains__, ['foo%d' % ii for ii in range(25)]), ['foo22'])
    print "done"
if __name__=="__main__":
    test_bloom()
