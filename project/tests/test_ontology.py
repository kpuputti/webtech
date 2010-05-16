from flyingfist import settings
from rdflib import Namespace
from rdflib import RDF
from rdflib import RDFS
from rdflib import graph
import unittest


ontology = graph.ConjunctiveGraph()
ontology.parse(settings.ONTOLOGY_FILE, format='n3')
#ontology.parse(settings.INSTANCES_FILE, format='n3')

FEATURE_CODE_COUNT = 671
FF = Namespace(settings.NS_FLYINGFIST)

SPARQL_BASE = """\
PREFIX rdf:<%s>
PREFIX rdfs:<%s>
PREFIX ff:<%s>

SELECT ?res
WHERE {

""" % (str(RDF), str(RDFS), str(FF))

class OntologyTest(unittest.TestCase):

    def test_ontology_type(self):
        assert type(ontology) == graph.ConjunctiveGraph

    def test_feature_code_count(self):
        feature_codes = ontology.triples((None, RDFS.subClassOf, FF['Feature']))
        self.assertEquals(len(list(feature_codes)), FEATURE_CODE_COUNT)

    def test_feature_labels(self):
        query = SPARQL_BASE + """\
        ?res rdfs:subClassOf ff:Feature .
        ?res rdfs:label ?l
        }
        """
        result = ontology.query(query)
        self.assertEquals(len(result), FEATURE_CODE_COUNT)
