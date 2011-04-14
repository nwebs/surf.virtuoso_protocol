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

import urllib
from surf.rdf import URIRef
from sparql_protocol.reader import ReaderPlugin as SPARQLReaderPlugin


class ReaderPlugin(SPARQLReaderPlugin):
    def __init__(self, *args, **kwargs):
        self.define = kwargs.pop('define', None)

        self._inference = False

        if "default_context" in kwargs:
            self._default_context = URIRef(kwargs["default_context"])

        SPARQLReaderPlugin.__init__(self, *args, **kwargs)

    # Inferencing

    def _inference_rule(self):
        """ Returns a unique name for the inference rule."""
        if not hasattr(self, '_default_context'):
            raise ValueError('Inferencing enabled but no default context set')

        return ('http://github.com/nwebs/surf.virtuoso_protocol#rule_'
                + urllib.quote(self._default_context))

    def _add_inference_rule(self):
        """ Adds a inference rule for the default context.

        Needs EXECUTE rights on rdfs_rule_set::

            (GRANT EXECUTE ON DB.DBA.rdfs_rule_set TO "SPARQL")
        """
        # Needs a 'GRANT EXECUTE ON DB.DBA.rdfs_rule_set TO "SPARQL"'
        self.execute_sparql(
                "SELECT sql:rdfs_rule_set('%(rule)s', '%(context)s') WHERE {}"
                % {'rule': self._inference_rule(),
                   'context': self._default_context})

    def get_inference(self):
        return self._inference

    def set_inference(self, inference):
        if inference and not self._inference:
            self._add_inference_rule()

        self._inference = inference

    inference = property(get_inference, set_inference)

    def _define_clause(self):
        if self.define is None:
            define = ()
        elif isinstance(self.define, basestring):
            define = (self.define,)
        else:
            define = self.define

        if self.inference:
            define_inference = 'input:inference "%s"' % self._inference_rule()
            define += (define_inference,)

        return ' '.join([('DEFINE ' + entry) for entry in define])

    def execute_sparql(self, q_string, *args, **kwargs):
        define_clause = self._define_clause()
        if define_clause:
            q_string = define_clause + '\n' + q_string + '\n'

        return SPARQLReaderPlugin.execute_sparql(self, q_string,
                                                 *args, **kwargs)
