# -*- coding: UTF-8 -*-
""" Module for virtuoso_protocol plugin tests. """

import os
from unittest import TestCase

import surf
from surf.query import a, select
from surf.rdf import Literal

ENV = 'SURF_SPARQL_TEST'
ENDPOINT = (os.environ[ENV] if ENV in os.environ and os.environ[ENV].strip()
                            else "http://localhost:8890/sparql")

class TestVirtuosoProtocol(TestCase):
    """ Tests for virtuoso_protocol plugin. """
    CONTEXT = "http://github.com/nwebs/surf.virtuoso_protocol#surf_test_graph_dummy2"


    def _get_store_session(self, use_default_context=True):
        """ Return initialized SuRF store and session objects. """

        kwargs = {"reader": "virtuoso_protocol",
                  "writer" : "virtuoso_protocol",
                  "endpoint" : ENDPOINT,
                  "use_subqueries" : True,
                  "combine_queries" : True,
                  "default_write_context": self.CONTEXT}

        if use_default_context:
            kwargs["default_context"] = self.CONTEXT

        store = surf.Store(**kwargs)
        session = surf.Session(store)

        # Fresh start!
        store.clear(self.CONTEXT)

        Person = session.get_class(surf.ns.FOAF + "Person")
        for name in ["John", "Mary", "Jane"]:
            # Some test data.
            person = session.get_resource("http://%s" % name, Person)
            person.foaf_name = name
            person.save()

        return store, session

    def test_missing_default_context(self):
        """ Test read & write without default_context set. """

        _, session = self._get_store_session(use_default_context=False)

        Person = session.get_class(surf.ns.FOAF + "Person")
        john = session.get_resource("http://John", Person)
        john.remove()
        self.assertTrue(not john.is_present())

        john.save()
        self.assertTrue(john.is_present())

    def test_same_as_inference_works(self):
        """ Test owl:sameAs inferencing. """

        store, session = self._get_store_session()
        # Let's say Jonathan is the same Person as John
        Person = session.get_class(surf.ns.FOAF["Person"])
        john = session.get_resource("http://John", Person)
        john.load()

        jonathan = session.get_resource("http://Jonathan", Person)
        jonathan.foaf_homepage = 'http://example.com'

        john[surf.ns.OWL['sameAs']] = jonathan
        session.commit()

        store.reader.define = 'input:same-as "yes"'

        query = select("?s").from_(self.CONTEXT)\
                            .where((jonathan.subject, surf.ns.FOAF['name'], '?s'))
        r = store.execute_sparql(unicode(query))

        self.assertEquals(set(entry['s'] for entry in r["results"]["bindings"]),
                          set([john.foaf_name[0]]))
