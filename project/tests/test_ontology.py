from flyingfist import settings
from rdflib import Namespace
from rdflib import RDF
from rdflib import RDFS
from rdflib import graph
import unittest


ontology = graph.ConjunctiveGraph()
ontology.parse(settings.ONTOLOGY_FILE, format='n3')
#ontology.parse(settings.INSTANCES_FILE, format='n3')

FF = Namespace(settings.NS_FLYINGFIST)

class OntologyTest(unittest.TestCase):

    def test_ontology_type(self):
        assert type(ontology) == graph.ConjunctiveGraph

    def test_feature_code_count(self):
        feature_codes = ontology.triples((None, RDFS.subClassOf, FF['Feature']))
        self.assertEquals(len(list(feature_codes)), 671)
