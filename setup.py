# Copyright 2010, nwebs GbR
# author: Christoph Burgmer

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer
#      in the documentation and/or other materials provided with
#      the distribution.
#    * Neither the name of nwebs nor the
#      names of its contributors may be used to endorse or promote
#      products derived from this software without specific prior
#      written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL NWEBS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='surf.virtuoso_protocol',
    version='0.1',
    description="SuRF plugin for Virtuoso's SPARQL HTTP protocol",
    long_description=open('README.rst').read(),
    url = "http://github.com/nwebs/surf.virtuoso_protocol",
    author="Christoph Burgmer",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    keywords = 'python Virtuoso SPARQL RDF resource mapper',
    test_suite = "nose.collector",
    packages=['virtuoso_protocol'],
    # TODO Broken, see http://code.google.com/p/surfrdf/issues/detail?id=56
    #install_requires=['surf.sparql_protocol>=1.0.0',],
    setup_requires=['nose>=0.11'],
    entry_points={
		'surf.plugins.reader': 'virtuoso_protocol = virtuoso_protocol.reader:ReaderPlugin',
		'surf.plugins.writer': 'virtuoso_protocol = virtuoso_protocol.writer:WriterPlugin',
    }
)
