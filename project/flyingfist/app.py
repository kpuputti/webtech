from flyingfist import settings
from mako import lookup
from rdflib import Literal
from rdflib import Namespace
from rdflib import RDFS
from rdflib import graph
import cherrypy
import itertools
import logging


logger = logging.getLogger('flyingfist.app')
tmpl_lookup = lookup.TemplateLookup(directories=[settings.TEMPLATE_FOLDER])
FF = Namespace(settings.NS_FLYINGFIST)


class FlyingFist(object):

    def __init__(self):
        logger.info('Reading in the ontology, might take a while...')
        self.ontology = graph.ConjunctiveGraph()
        self.ontology.parse(settings.ONTOLOGY_FILE, format='n3')
        self.ontology.parse(settings.INSTANCES_FILE, format='n3')
        logger.info('Finished reading the ontology.')

    @cherrypy.expose
    def index(self):
        return 'goto <a href="/flyingfist">/flyingfist</a>'

    def get_label(self, uri):
        triples = list(self.ontology.triples((uri, RDFS.label, None)))
        if triples:
            return str(triples[0][2])
        return uri

    def get_data(self, uri, label):
        subject_triples = self.ontology.triples((uri, None, None))
        object_triples = self.ontology.triples((None, None, uri))
        subject_data = []
        object_data = []

        for triple in itertools.chain(subject_triples, object_triples):

            subject = triple[0]
            predicate = triple[1]
            tobject = triple[2]

            item = [
                {
                    'uri': str(subject),
                    'label': self.get_label(subject),
                    'local': subject.startswith(FF),
                },
                {
                    'uri': str(predicate),
                    'label': self.get_label(predicate),
                    'local': subject.startswith(FF),
                },
                {
                    'local': tobject.startswith(FF),
                },
            ]

            if type(tobject) == Literal:
                item[2]['text'] = str(tobject)
            else:
                item[2]['uri'] = str(tobject)
                item[2]['label'] = self.get_label(tobject)

            if str(subject) == str(uri):
                subject_data.append(item)
            else:
                object_data.append(item)
        return subject_data, object_data

    @cherrypy.expose
    def flyingfist(self, param=None):
        if param is None:
            return tmpl_lookup.get_template('index.mako').render()

        uri = FF[param]
        label = self.get_label(uri) or ''
        subject_data, object_data = self.get_data(uri, label)

        if not subject_data and not object_data:
            raise cherrypy.HTTPError(status=404, message='resource not found')

        return tmpl_lookup.get_template('feature.mako').render(
            label=label,
            uri=uri,
            subject_data=subject_data,
            object_data=object_data)
