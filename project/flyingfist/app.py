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
import json
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
        self.ontology.parse(settings.ONTOLOGY_FILE, format='n3')
        self.ontology.parse(settings.INSTANCES_FILE, format='n3')
        logger.info('Finished reading the ontology.')
        self.storage = storage.Storage()

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('/search', 302)

    @cherrypy.expose
    def search(self, q=None):
        lucene.getVMEnv().attachCurrentThread()
        if q is None or not q.strip():
            search = False
            query = ''
            query_raw = ''
            hits = 0
            places = []
        else:
            search = True
            query_raw = q.replace('"', '')
            query = utils.escape_html(q)
            hits, places = self.storage.search(q, ontology=self.ontology)
        return tmpl_lookup.get_template('search.mako').render_unicode(
            search=search,
            query=query,
            query_raw=query_raw,
            hits=hits,
            places=places)

    def _sort_key(self, key):
        values = {
            'label': '00',
            'type': '01',
            'admin1Code': '02',
            'admin2Code': '03',
            'latitude': '04',
            'longitude': '05',
        }
        return values.get(key, key)

    @cherrypy.expose
    def flyingfist(self, param=None):
        if param is None:
            return tmpl_lookup.get_template('index.mako').render()

        uri = FF[param]
        label = self.storage.get_label(self.ontology, uri) or ''

        info = self.storage.place_info(self.ontology, param)
        info_str = json.dumps(self.storage.place_info_simple(self.ontology, param))

        return tmpl_lookup.get_template('feature.mako').render_unicode(
            label=label,
            uri=uri,
            info=info,
            sorted_keys=sorted(info, key=self._sort_key),
            info_str=info_str)


    @cherrypy.expose
    def api(self, method=None, term=None):
        lucene.getVMEnv().attachCurrentThread()
        if method is None:
            logger.debug('Api method empty.')
            raise cherrypy.HTTPError(status=404, message='Api method empty.')

        if method == 'autocomplete' and term:
            hits, places = self.storage.search(term, partial=True, max_results=10)
        else:
            return ''

        cherrypy.response.headers['Content-Type'] = 'application/json'

        results = [dict(label=place['label_hi'], value=place['label'])
                   for place in places]
        return json.dumps(results)
