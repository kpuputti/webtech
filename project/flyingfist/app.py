from flyingfist import settings
from mako import lookup
from rdflib import Literal
from rdflib import Namespace
from rdflib import RDFS
from rdflib import graph
import cherrypy
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

    def get_link(self, uri):
        label = self.get_label(uri)
        return '<a href="%s">%s</a>' % (uri, label)

    @cherrypy.expose
    def flyingfist(self, param=None):
        if param is None:
            return tmpl_lookup.get_template('index.mako').render()

        uri = FF[param]
        triples = self.ontology.triples((uri, None, None))
        label = self.get_label(uri) or ''
        data = []

        for triple in triples:

            predicate = triple[1]
            tobject = triple[2]
            item = [
                dict(uri=str(predicate), label=self.get_label(predicate),
                     local=predicate.startswith(FF)),
                dict(uri=str(tobject)),
            ]

            if type(tobject) == Literal:
                item[1]['text'] = str(tobject)
            else:
                item[1]['local'] = tobject.startswith(FF)
                item[1]['uri'] = str(tobject)
                item[1]['label'] = self.get_label(tobject)

            data.append(item)

        if not data:
            raise cherrypy.HTTPError(status=404, message='resource not found')

        return tmpl_lookup.get_template('feature.mako').render(label=label,
                                                               uri=uri,
                                                               data=data)
