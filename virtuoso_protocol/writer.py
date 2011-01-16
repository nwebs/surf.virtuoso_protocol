# -*- coding: utf-8 -*-
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

import sys

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import EndPointNotFound, QueryBadFormed, SPARQLWrapperException

from surf import store
from surf.rdf import URIRef
from surf.query import Filter, Group, NamedGroup, Union
from surf.query.update import insert, delete, clear
from sparql_protocol.writer import WriterPlugin as SPARQLWriterPlugin
from sparql_protocol.writer import SparqlWriterException

from reader import ReaderPlugin

class WriterPlugin(SPARQLWriterPlugin):
    def __init__(self, *args, **kwargs):
        # The write_context will be used if no context is given. Virtuoso needs
        #   a context by default on write access.
        context = kwargs.get("default_write_context")
        self.__default_write_context = (URIRef(unicode(context)) if context
                                                                 else None)
        print self.__default_write_context

        # By default set combine_queries which Virtuoso supports
        if "combine_queries" not in kwargs:
            kwargs["combine_queries"] = True

        SPARQLWriterPlugin.__init__(self, *args, **kwargs)

    def __add_default_write_context(self, context):
        """ Return write context if context is None. """

        if context == store.NO_CONTEXT:
            # Should not beed needed, as not supported by Virtuoso
            context = None
        elif not context:
            context = self.__default_write_context

        return context

    # Re-implemented methods

    def _save(self, *resources):
        for context, items in self.__group_by_context(resources).items():
            context = self.__add_default_write_context(context)
            # Deletes all triples with matching subjects.
            remove_query = self.__prepare_delete_many_query(items, context)
            insert_query = self.__prepare_add_many_query(items, context)
            self.__execute(remove_query, insert_query)

    def _update(self, *resources):
        for context, items in self.__group_by_context(resources).items():
            context = self.__add_default_write_context(context)
            # Explicitly enumerates triples for deletion.
            remove_query = self.__prepare_selective_delete_query(items, context)
            insert_query = self.__prepare_add_many_query(items, context)
            self.__execute(remove_query, insert_query)

    def _remove(self, *resources, **kwargs):
        for context, items in self.__group_by_context(resources).items():
            context = self.__add_default_write_context(context)
            # Deletes all triples with matching subjects.
            inverse = kwargs.get("inverse")
            query = self.__prepare_delete_many_query(items, context, inverse)
            self.__execute(query)

    # Overloaded methods

    def load_triples(self, source, format='xml', context=None, **kwargs):
        context = self.__add_default_write_context(context)
        super(WriterPlugin, self).load_triples(source, format, context, **kwargs)

    def _add_triple(self, s=None, p=None, o=None, context=None):
        context = self.__add_default_write_context(context)
        super(WriterPlugin, self)._add_triple(s, p, o, context)

    def _set_triple(self, s=None, p=None, o=None, context=None):
        context = self.__add_default_write_context(context)
        super(WriterPlugin, self)._set_triple(s, p, o, context)

    def _remove_triple(self, s=None, p=None, o=None, context=None):
        context = self.__add_default_write_context(context)
        super(WriterPlugin, self)._remove_triple(s, p, o, context)

    def _clear(self, context=None):
        context = self.__add_default_write_context(context)
        super(WriterPlugin, self)._clear(context)
