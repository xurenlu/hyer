#!/usr/bin/env python
#
# Setup script for the elementtidy library
# $Id: setup.py 2275 2005-02-03 18:20:56Z fredrik $
#
# Usage: python setup.py install
#

from distutils.core import setup, Extension

NAME = "elementtidy"
VERSION = "1.0-20050212"

TIDYFILES = [
    "tidylib/src/access.c",
    "tidylib/src/alloc.c",
    "tidylib/src/attrask.c",
    "tidylib/src/attrdict.c",
    "tidylib/src/attrget.c",
    "tidylib/src/attrs.c",
    "tidylib/src/buffio.c",
    "tidylib/src/clean.c",
    "tidylib/src/config.c",
    "tidylib/src/entities.c",
    "tidylib/src/fileio.c",
    "tidylib/src/istack.c",
    "tidylib/src/lexer.c",
    "tidylib/src/localize.c",
    "tidylib/src/parser.c",
    "tidylib/src/pprint.c",
    "tidylib/src/streamio.c",
    "tidylib/src/tagask.c",
    "tidylib/src/tags.c",
    "tidylib/src/tidylib.c",
    "tidylib/src/tmbstr.c",
    "tidylib/src/utf8.c",
]

setup(
    name=NAME,
    version=VERSION,
    author="Fredrik Lundh",
    author_email="fredrik@pythonware.com",
    description="ElementTidy - a tidylib interface for ElementTree",
    url="http://effbot.org/zone/element-tidylib.htm",
    #packages=["elementtidy"],
    ext_modules = [
        Extension(
            "_elementtidy",
            ["_elementtidy.c"] + TIDYFILES,
            define_macros=[("NDEBUG", None)],
            include_dirs=["tidylib/include"],
            )
        ]
    )
