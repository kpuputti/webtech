from flyingfist import api
from flyingfist import settings
from flyingfist import storage
from flyingfist import utils
from mako import lookup
from rdflib import Namespace
from rdflib import RDF
from rdflib import graph
import cherrypy
import json
import logging
import lucene


logger = logging.getLogger('flyingfist.app')
tmpl_lookup = lookup.TemplateLookup(directories=[settings.TEMPLATE_FOLDER],
                                    input_encoding='utf-8')
FF = Namespace(settings.NS_FLYINGFIST)
lucene.initVM()


def error_404(status, message, traceback, version):
    return tmpl_lookup.get_template('404.mako').render_unicode(
        status=status,
        message=message)


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
        id_valid = False
        if param:
            param = param.strip()
            ptype = list(self.ontology.triples((FF[param], RDF.type, None)))
            if len(ptype) == 1:
                id_valid = True
            else:
                logger.warn('No type found for id: %s' % param)
        if not id_valid:
            raise cherrypy.HTTPError(status=404, message='Invalid resource id.')

        uri = FF[param]
        label = self.storage.get_label(self.ontology, uri) or ''

        info = self.storage.place_info(self.ontology, param)
        info_str = json.dumps(self.storage.place_info_simple(self.ontology, param))

        weather = None
        if 'latitude' in info and 'longitude' in info:
            weather = api.get_weather(float(info['latitude']['object']),
                                      float(info['longitude']['object']))

        related = self.storage.get_related(self.ontology, uri)

        return tmpl_lookup.get_template('feature.mako').render_unicode(
            label=label,
            uri=uri,
            info=info,
            sorted_keys=sorted(info, key=self._sort_key),
            info_str=info_str,
            weather=weather,
            related=related)


    @cherrypy.expose
    def api(self, method=None, term=None,
            north=None, south=None, east=None, west=None):
        lucene.getVMEnv().attachCurrentThread()
        if method is None:
            logger.error('Api method empty.')
            raise cherrypy.HTTPError(status=404, message='Api method empty.')

        if method == 'autocomplete' and term:
            hits, places = self.storage.search(term, partial=True, max_results=10)
            results = [dict(label=place['label_hi'], value=place['label'])
                       for place in places]
        elif method == 'wikipedia' and north and south and east and west:
            try:
                results = api.get_wikipedia(float(north), float(south),
                                            float(east), float(west))
            except ValueError:
                logger.error('Bad parameters in api request.')
                raise cherrypy.HTTPError(status=404, message='Bad parameters.')
        else:
            logger.error('Not enough parameters in api request.')
            raise cherrypy.HTTPError(status=404, message='Not enough parameters.')

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(results)
