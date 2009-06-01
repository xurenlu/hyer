############################################################
#                                                          #
# The implementation of PHPRPC Protocol 3.0                #
#                                                          #
# fpconst.py                                               #
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
# Utilities for handling IEEE 754 floating point special values
#
# This python module implements constants and functions for working with
# IEEE754 double-precision special values.  It provides constants for
# Not-a-Number (NaN), Positive Infinity (PosInf), and Negative Infinity
# (NegInf), as well as functions to test for these values.
#
# Copyright: Ma Bingyao <andot@ujn.edu.cn>
# Version: 1.0
# LastModified: Oct 4, 2008
# This library is free.  You can redistribute it and/or modify it.

import types

PosInf = 1e300000
NegInf = -1e300000
NaN = PosInf/PosInf

def isPosInf(value):
    return (PosInf == value)

def isNegInf(value):
    return (NegInf == value)

def isInf(value):
    return (PosInf == value) or (NegInf == value)

def isFinite(value):
    return (PosInf > value > NegInf)

def isNaN(value):
    return (types.FloatType == type(value)) and (value != value)

if __name__ == "__main__":
    def test_isNaN():
        assert( not isNaN(PosInf) )
        assert( not isNaN(NegInf) )
        assert(     isNaN(NaN   ) )
        assert( not isNaN(   1.0) )
        assert( not isNaN(  -1.0) )

    def test_isInf():
        assert(     isInf(PosInf) )
        assert(     isInf(NegInf) )
        assert( not isInf(NaN   ) )
        assert( not isInf(   1.0) )
        assert( not isInf(  -1.0) )

    def test_isFinite():
        assert( not isFinite(PosInf) )
        assert( not isFinite(NegInf) )
        assert( not isFinite(NaN   ) )
        assert(     isFinite(   1.0) )
        assert(     isFinite(  -1.0) )

    def test_isPosInf():
        assert(     isPosInf(PosInf) )
        assert( not isPosInf(NegInf) )
        assert( not isPosInf(NaN   ) )
        assert( not isPosInf(   1.0) )
        assert( not isPosInf(  -1.0) )

    def test_isNegInf():
        assert( not isNegInf(PosInf) )
        assert(     isNegInf(NegInf) )
        assert( not isNegInf(NaN   ) )
        assert( not isNegInf(   1.0) )
        assert( not isNegInf(  -1.0) )

    # overall test
    def test():
        test_isNaN()
        test_isInf()
        test_isFinite()
        test_isPosInf()
        test_isNegInf()

    test()