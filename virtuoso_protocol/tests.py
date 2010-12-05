# -*- coding: UTF-8 -*-
""" Module for virtuoso_protocol plugin tests. """

from unittest import TestCase

import surf
from surf.query import a, select
from surf.rdf import Literal

class TestVirtuosoProtocol(TestCase):
    """ Tests for virtuoso_protocol plugin. """
    CONTEXT = "http://github.com/nwebs/surf.virtuoso_protocol#surf_test_graph_dummy2"

    def setUp(self):
        """ Return initialized SuRF store and session objects. """

        kwargs = {"reader": "virtuoso_protocol",
                  "writer" : "virtuoso_protocol",
                  "endpoint" : "http://localhost:8890/sparql",
                  "use_subqueries" : True,
                  "combine_queries" : True,
                  "default_context": self.CONTEXT}

        self.store = surf.Store(**kwargs)
        self.session = surf.Session(self.store)

        # Fresh start!
        self.store.clear(self.CONTEXT)

        Person = self.session.get_class(surf.ns.FOAF + "Person")
        for name in ["John", "Mary", "Jane"]:
            # Some test data.
            person = self.session.get_resource("http://%s" % name, Person)
            person.foaf_name = name
            person.save()

    def test_same_as_inference_works(self):
        # Let's say Jonathan is the same Person as John
        Person = self.session.get_class(surf.ns.FOAF["Person"])
        john = self.session.get_resource("http://John", Person)
        john.load()

        jonathan = self.session.get_resource("http://Jonathan", Person)
        jonathan.foaf_homepage = 'http://example.com'

        john[surf.ns.OWL['sameAs']] = jonathan
        self.session.commit()

        self.store.reader.define = 'input:same-as "yes"'

        query = select("?s").from_(self.CONTEXT)\
                            .where((jonathan.subject, surf.ns.FOAF['name'], '?s'))
        r = self.store.execute_sparql(unicode(query))

        self.assertEquals(set(entry['s'] for entry in r["results"]["bindings"]),
                          set([john.foaf_name[0]]))
