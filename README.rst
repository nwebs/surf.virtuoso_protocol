surf.virtuoso_protocol is a plugin for the Python-based Object-RDF Mapper
`SuRF`_ implementing the `SPARQL protocol`_ as used in the `Virtuoso`_ backend.

.. _SuRF: http://packages.python.org/SuRF/index.html
.. _SPARQL protocol: http://www.w3.org/TR/rdf-sparql-query/
.. _Virtuoso: http://virtuoso.openlinksw.com/dataspace/dav/wiki/Main

About
=====
Virtuoso kann be accessed via `SuRF's sparql_protocol`_
handler. However, for making use of `Virtuoso's inferencing & reasoning`_
support a specialized SPARQL syntax is needed, which this plugin can
accommodate.

.. _SuRF's sparql_protocol: 
   http://packages.python.org/SuRF/plugins/sparql_protocol.html
.. _Virtuoso's inferencing & reasoning:
   http://docs.openlinksw.com/virtuoso/rdfsparqlrule.html

Dependencies
============

* SuRF, http://code.google.com/p/surfrdf/
* surf.sparql_protocol, http://pypi.python.org/pypi/surf.sparql_protocol
