from flyingfist import settings
from flyingfist import storage
from flyingfist import utils
from mako import lookup
from rdflib import Literal
from rdflib import Namespace
from rdflib import RDFS
from rdflib import graph
import cherrypy
import itertools
import logging
import lucene


logger = logging.getLogger('flyingfist.app')
tmpl_lookup = lookup.TemplateLookup(directories=[settings.TEMPLATE_FOLDER],
                                    input_encoding='utf-8')
FF = Namespace(settings.NS_FLYINGFIST)
lucene.initVM()

class FlyingFist(object):

    def __init__(self):
        logger.info('Reading in the ontology, might take a while...')
        self.ontology = graph.ConjunctiveGraph()
        #self.ontology.parse(settings.ONTOLOGY_FILE, format='n3')
        #self.ontology.parse(settings.INSTANCES_FILE, format='n3')
        logger.info('Finished reading the ontology.')
        self.storage = storage.Storage()

    @cherrypy.expose
    def index(self):
        return tmpl_lookup.get_template('index.mako').render_unicode()

    @cherrypy.expose
    def search(self, q=None):
        lucene.getVMEnv().attachCurrentThread()
        if q is None:
            query = ''
            hits = 0
        else:
            query = utils.escape_html(q)
            hits, places = self.storage.search(q)
        return tmpl_lookup.get_template('search.mako').render_unicode(
            query=query,
            hits=hits,
            places=places)

    def get_label(self, uri):
        triples = list(self.ontology.triples((uri, RDFS.label, None)))
        if triples:
            return triples[0][2]
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

        return tmpl_lookup.get_template('feature.mako').render_unicode(
            label=label,
            uri=uri,
            subject_data=subject_data,
            object_data=object_data)
