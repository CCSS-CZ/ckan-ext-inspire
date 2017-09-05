import rdflib
from rdflib.graph import Graph as _Graph
from rdflib.namespace import Namespace, RDF, RDFS, XSD
from rdflib.term import URIRef, Literal, BNode, Node

import logging
logger = logging.getLogger(__name__)

rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')

CNT = Namespace("http://www.w3.org/2011/content#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCES = Namespace("http://purl.org/dc/elements/1.1/")
DCL = Namespace("http://dclite4g.xmlns.com/schema.rdf#")
DCT = Namespace("http://purl.org/dc/terms/")
EARL = Namespace("http://www.w3.org/ns/earl#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
GCO = Namespace("http://www.isotc211.org/2005/gco")
GMD = Namespace("http://www.isotc211.org/2005/gmd")
GML = Namespace("http://www.opengis.net/gml")
LICENSES = Namespace("http://purl.org/okfn/licenses/")
LOCAL = Namespace("http://opendatasearch.org/schema#")
LOCN = Namespace("http://w3.org/ns/locn#")
OPMV = Namespace("http://purl.org/net/opmv/ns#")
OS = Namespace("http://a9.com/-/spec/opensearch/1.1/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
REV = Namespace("http://purl.org/stuff/rev#")
SCOVO = Namespace("http://purl.org/NET/scovo#")
SCHEMA = Namespace("http://schema.org/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
SRV = Namespace("http://www.isotc211.org/2005/srv")
TIME = Namespace("http://www.w3.org/2006/time#")
UUID = Namespace("urn:uuid:")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
VOID = Namespace("http://rdfs.org/ns/void#")
WDRS = Namespace("http://www.w3.org/2007/05/powder-s#")
XLINK = Namespace("http://www.w3.org/1999/xlink")

namespaces = {
	"cnt": CNT,
	"dcl": DCL,
    "dc": DC,
    "dcat": DCAT,
    "dct": DCT,
    "earl": EARL,
    "foaf": FOAF,
    "gco": GCO,
    "gmd": GMD,
    "gml": GML,
    "licenses": LICENSES,
    "local": LOCAL,
    "locn": LOCN,
    "opmv": OPMV,
    "os": OS,
    "owl": OWL,
    "prov": PROV,
    "rdf": RDF,
    "rdfs": RDFS,
    "rev": REV,
    "scovo": SCOVO,
    "schema": SCHEMA,
    "skos": SKOS,
    "srv": SRV,
    "time": TIME,
    "vcard": VCARD,
    "void": VOID,
    "wdrs": WDRS,
    "xlink": XLINK,
}

def bind_ns(g):
    """
    Given an :class:`~rdflib.graph.Graph`, bind the namespaces present in
    the dictionary in this module to it for more readable serialisations.

    :param g: an instance of :class:`rdflib.graph.Graph`.
    """
    try:
        for x in namespaces.items():
            g.bind(*x)
            logger.debug(x)
        ##[g.bind(*x) for x in namespaces.items()]
    except Exception as e:
        logger.exception('pass namespaces')
        pass

from rdflib import plugin, exceptions, query
def __query(self, query_object, processor='sparql', result='sparql',
        initBindings={}):
    if not isinstance(processor, query.Processor):
        processor = plugin.get(processor, query.Processor)(self)
    if not isinstance(result, query.Result):
        result = plugin.get(result, query.Result)
    return result(processor.query(query_object, initBindings, namespaces))


def Graph(*a, **kw):
    _Graph.bound_query = __query
    graph = _Graph(*a, **kw)
    bind_ns(graph)
    ##graph.bind('ex', URIRef('http://www.my-example.intra/ontologies/ci.owl#'))
    return graph
