surf.virtuoso_protocol is a plugin for the Python-based Object-RDF Mapper
`SuRF`_ implementing the `SPARQL protocol`_ as used in the `Virtuoso`_ backend.

.. _SuRF: http://packages.python.org/SuRF/index.html
.. _SPARQL protocol: http://www.w3.org/TR/rdf-sparql-query/
.. _Virtuoso: http://virtuoso.openlinksw.com/dataspace/dav/wiki/Main

Example
=======

Use OWL sameAs::

    >>> import surf
    >>> # Create store & session
    ... store = surf.Store(reader="virtuoso_protocol",
    ...                    writer="virtuoso_protocol",
    ...                    endpoint="http://localhost:8890/sparql",
    ...                    default_context="http://dummy")
    >>> session = surf.Session(store, {})
    >>> # John
    ... Person = session.get_class(surf.ns.FOAF["Person"])
    >>> john = session.get_resource("http://John", Person)
    >>> john.foaf_name = 'John'
    >>> # Jonathan
    ... jonathan = session.get_resource("http://Jonathan", Person)
    >>> jonathan.foaf_homepage = 'http://example.com'
    >>> # owl:sameAs
    ... john[surf.ns.OWL['sameAs']] = jonathan
    >>> session.commit()
    >>> # Set owl:sameAs Inferencing
    ... store.reader.define = 'input:same-as "yes"'
    >>> # Query
    ... query = surf.query.select("?s").from_("http://dummy")\
    ...                   .where((jonathan.subject, surf.ns.FOAF['name'], '?s'))
    >>> store.execute_sparql(unicode(query))
    {'results': {'bindings': [{'s': rdflib.Literal(u'John')}]}}

About
=====

Virtuoso can be accessed via `SuRF's sparql_protocol`_ handler. 
However, for making use of `Virtuoso's inferencing & reasoning`_
support a specialized SPARQL syntax is needed, which this plugin can
accommodate. Technically this plugin extends SuRF's sparql_protocol plugin with
functionality needed for Virtuoso.

.. _SuRF's sparql_protocol: 
   http://packages.python.org/SuRF/plugins/sparql_protocol.html
.. _Virtuoso's inferencing & reasoning:
   http://docs.openlinksw.com/virtuoso/rdfsparqlrule.html

Default write context
---------------------
Virtuoso's graph implementation knows multiple named graphs and one unnamed
graph. The unnamed graph built up from the union of all named graphs during
SPARQL queries. For SPARUL (write access) a named graph needs to be given as
context. The virtuoso_protocol plugin introduces a ``default_write_context``
parameter to provide a default context for write access. In contrast to SuRF's
``default_context`` the application of a write-only context allows for queries
over all named graphs at once, while still being able to issue writes to a
dedicated named graph.

Unit testing
============
Run::

    $ python setup.py nosetests

Similar packages
================
* surf.sparql_protocol - SuRF SPARQL protocol plugin (mentioned above), allows
  access to Virtuoso's standard SPARQL features.
* Python-Virtuoso - OpenLink Virtuoso Support for SQLAlchemy and RDFLib,
  http://pypi.python.org/pypi/virtuoso/, provides access through ODBC

Dependencies
============

* SuRF, http://code.google.com/p/surfrdf/
* surf.sparql_protocol, http://pypi.python.org/pypi/surf.sparql_protocol

