from flyingfist import settings
from rdflib import Namespace
from rdflib import RDF
from rdflib import RDFS
from rdflib import graph
import rdflib


rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')


FF = Namespace(settings.NS_FLYINGFIST)

SPARQL_BASE = """\
PREFIX rdf:<%s>
PREFIX rdfs:<%s>
PREFIX ff:<%s>
SELECT ?res
WHERE {
""" % (str(RDF), str(RDFS), str(FF))

print 'loading ontology...'
ontology = graph.ConjunctiveGraph()
ontology.parse(settings.ONTOLOGY_FILE, format='n3')
ontology.parse(settings.INSTANCES_FILE, format='n3')
print 'ontology loaded'

def main():
    while True:
        q = raw_input('Type in query: ')
        query = SPARQL_BASE + """\
        ?res ff:geonameId ?id .
        ?res rdfs:label ?label .
        FILTER regex(?label, '^%s') .
        }
        """ % q
        print query
        results = list(ontology.query(query))
        print 'Results for "%s" (%d).' % (q, len(results))


if __name__ == '__main__':
    main()
