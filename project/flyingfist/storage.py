"""Helper functions to create the RDF storage.
"""
from flyingfist import settings
from rdflib import Literal
from rdflib import Namespace
from rdflib import RDF
from rdflib import RDFS
from rdflib import graph
import logging
import lucene


logger = logging.getLogger('flyingfist.storage')
FF = Namespace(settings.NS_FLYINGFIST)


class IndexCreator(object):

    def __init__(self):
        logger.info('Initializing Lucene index creation.')
        lucene.initVM()
        self.directory = lucene.SimpleFSDirectory(
            lucene.File(settings.INDEX_FOLDER))
        self.analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)

    def _places(self):
        with open(settings.FILE_NL_FEATURES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                columns = line.split('\t')
                geoname_id = columns[0]
                label = columns[1]
                yield (geoname_id, label)

    def create_index(self):
        logger.info('Writing the Lucene index.')
        writer = lucene.IndexWriter(self.directory, self.analyzer, True,
                                    lucene.IndexWriter.MaxFieldLength.UNLIMITED)
        count = 0
        for geoname_id, label in self._places():
            count += 1
            doc = lucene.Document()
            doc.add(lucene.Field('geonameid', geoname_id, lucene.Field.Store.YES,
                                 lucene.Field.Index.NOT_ANALYZED))
            doc.add(lucene.Field('label', label, lucene.Field.Store.YES,
                                 lucene.Field.Index.ANALYZED))
            writer.addDocument(doc)

        logger.info('Added %d places to the index.' % count)
        writer.optimize()
        writer.close()
        logger.info('Lucene index successfully created.')


class StorageCreator(object):

    def __init__(self):
        self.ontology = graph.ConjunctiveGraph()
        self.instances = graph.ConjunctiveGraph()
        self.flyingfist = Namespace(settings.NS_FLYINGFIST)
        self.ontology.bind('ff', self.flyingfist)
        self.instances.bind('ff', self.flyingfist)

    def _add_classes(self):
        logger.info('Adding classes to the graph.')
        admin_code = self.flyingfist['AdminCode']
        self.ontology.add((admin_code, RDF.type, RDFS.Class))
        self.ontology.add((admin_code, RDFS.label, Literal('admin code')))

        admin1_code = self.flyingfist['Admin1Code']
        self.ontology.add((admin1_code, RDF.type, RDFS.Class))
        self.ontology.add((admin1_code, RDFS.label,
                           Literal('admin 1 code')))
        self.ontology.add((admin1_code, RDFS.subClassOf, admin_code))

        admin2_code = self.flyingfist['Admin2Code']
        self.ontology.add((admin2_code, RDF.type, RDFS.Class))
        self.ontology.add((admin2_code, RDFS.label,
                           Literal('admin 2 code')))
        self.ontology.add((admin2_code, RDFS.subClassOf, admin_code))

        feature_code = self.flyingfist['Feature']
        self.ontology.add((feature_code, RDF.type, RDFS.Class))
        self.ontology.add((feature_code, RDFS.label, Literal('feature')))

    def _add_properties(self):
        logger.info('Adding properties to the graph.')

        self.ontology.add((RDFS.label, RDFS.label, Literal('label')))
        self.ontology.add((RDF.Property, RDFS.label, Literal('property')))
        self.ontology.add((RDFS.Class, RDFS.label, Literal('class')))
        self.ontology.add((RDF.type, RDFS.label, Literal('type')))
        self.ontology.add((RDFS.subClassOf, RDFS.label, Literal('sub class of')))

        for name, desc in settings.PROPERTIES.iteritems():
            prop = self.flyingfist[name]
            self.ontology.add((prop, RDF.type, RDF.Property))
            self.ontology.add((prop, RDFS.label, Literal(desc)))

    def _add_admin1_codes(self):
        logger.info('Adding admin 1 codes to the graph.')
        admin_code_class = self.flyingfist['Admin1Code']
        with open(settings.FILE_ADMIN1_CODES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                try:
                    code, name = line.split('\t')
                except ValueError:
                    code, name = line, None
                code_instance = self.flyingfist[code]
                self.instances.add((code_instance, RDF.type,
                                    admin_code_class))
                if name is not None:
                    self.instances.add((code_instance, RDFS.label,
                                        Literal(name)))

    def _add_admin2_codes(self):
        logger.info('Adding admin 2 codes to the graph.')
        admin_code_class = self.flyingfist['Admin2Code']
        feature = self.flyingfist['feature']
        with open(settings.FILE_ADMIN2_CODES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                code, name, asciiname, geonameid = line.split('\t')
                code_instance = self.flyingfist[code]
                self.instances.add((code_instance, RDF.type,
                                    admin_code_class))
                self.instances.add((code_instance, RDFS.label,
                                    Literal(name)))
                self.instances.add((code_instance, feature,
                                    self.flyingfist[geonameid]))

    def _add_feature_codes(self):
        logger.info('Adding feature codes to the graph.')
        feature_code = self.flyingfist['Feature']
        description_prop = self.flyingfist['description']
        with open(settings.FILE_FEATURE_CODES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                try:
                    code, name, description = line.split('\t')
                except ValueError:
                    code, name = line.split('\t')
                    description = None
                if code != 'null':
                    instance = self.flyingfist[code]
                    self.ontology.add((instance, RDF.type, RDFS.Class))
                    self.ontology.add((instance, RDFS.subClassOf, feature_code))
                    self.ontology.add((instance, RDFS.label, Literal(name)))
                    if description:
                        self.ontology.add((instance, description_prop,
                                           Literal(description)))

    def _add_country_info(self):
        pass

    def _add_feature_columns(self):
        pass

    def _create_ontologies(self):
        """Create the ontology structure.

        Data is read from the Geonames files and an RDF ontology is
        created of the classes and properties.
        """
        self._add_classes()
        self._add_properties()
        self._add_admin1_codes()
        self._add_admin2_codes()
        self._add_feature_codes()
        self._add_country_info()
        self._add_feature_columns()

    def _get_admin_class(self, code1, code2, level):
        if level == 1:
            # First try the NL prefix.
            feature_class = self.flyingfist['NL.' + code1]
            class_triples = self.instances.triples((feature_class,
                                                    RDF.type,
                                                    None))
            if len(list(class_triples)) == 1:
                return feature_class
            else:
                # If the NL prefix was not found, try the BE one.
                feature_class = self.flyingfist['BE.' + code1]
                class_triples = self.instances.triples((feature_class,
                                                        RDF.type,
                                                        None))
                if len(list(class_triples)) == 1:
                    return feature_class
                else:
                    logger.warn('Admin 1 code not found: %s' % code1)
                    return None
        elif level == 2:
            # First try the NL prefix.
            code = 'NL.' + code1 + '.' + code2
            feature_class = self.flyingfist[code]
            class_triples = self.instances.triples((feature_class,
                                                    RDF.type,
                                                    None))
            if len(list(class_triples)) == 1:
                return feature_class
            else:
                # If the NL prefix was not found, try the BE one.
                code = 'BE.' + code1 + '.' + code2
                feature_class = self.flyingfist[code]
                class_triples = self.instances.triples((feature_class,
                                                        RDF.type,
                                                        None))
                if len(list(class_triples)) == 1:
                    return feature_class
                else:
                    logger.warn("Admin 2 code '%s' not found: %s" % (code2, code))
                    return None
        else:
            logger.warn('Bad admin level: %d' % level)


    def _add_feature(self, columns):
        geoname_id = columns[0] or None
        name = columns[1] or None
        asciiname = columns[2] or None
        alternate_names = columns[3] or None
        latitude = columns[4] or None
        longitude = columns[5] or None
        feature_class = columns[6] or None
        feature_code = columns[7] or None
        country_code = columns[8] or None
        cc2 = columns[9] or None
        admin1_code = columns[10] or None
        admin2_code = columns[11] or None
        admin3_code = columns[12] or None
        admin4_code = columns[13] or None
        population = columns[14] or None
        elevation = columns[15] or None
        gtopo30 = columns[16] or None
        timezone = columns[17] or None
        modification_date = columns[18] or None

        instance = self.flyingfist[geoname_id]
        self.instances.add((instance, RDF.type,
                            self.flyingfist['%s.%s' % (feature_class,
                                                       feature_code)]))
        self.instances.add((instance, RDFS.label, Literal(name)))
        self.instances.add((instance,
                            self.flyingfist['geonameId'],
                            Literal(geoname_id)))

        if alternate_names:
            self.instances.add((instance,
                                self.flyingfist['alternateNames'],
                                Literal(alternate_names)))
        if latitude:
            self.instances.add((instance,
                                self.flyingfist['latitude'],
                                Literal(latitude)))
        if longitude:
            self.instances.add((instance,
                                self.flyingfist['longitude'],
                                Literal(longitude)))
        if country_code:
            self.instances.add((instance,
                                self.flyingfist['countryCode'],
                                Literal(country_code)))

        if admin1_code:
            admin1_class = self._get_admin_class(admin1_code, None, 1)
            if admin1_class is not None:
                self.instances.add((instance,
                                    self.flyingfist['admin1Code'],
                                    admin1_class))

                if admin2_code:
                    admin2_class = self._get_admin_class(admin1_code,
                                                         admin2_code, 2)
                    if admin2_class is not None:
                        self.instances.add((instance,
                                            self.flyingfist['admin2Code'],
                                            admin2_class))

        if population and population != '0':
            self.instances.add((instance,
                                self.flyingfist['population'],
                                Literal(population)))
        if elevation:
            self.instances.add((instance,
                                self.flyingfist['elevation'],
                                Literal(elevation)))
        if timezone:
            self.instances.add((instance,
                                self.flyingfist['timezone'],
                                Literal(timezone)))

    def _add_data(self):
        """Add all the instance data to the RDF storage."""
        with open(settings.FILE_NL_FEATURES) as f:
            for line in f:
                columns = line.decode('utf-8').strip().split('\t')
                assert len(columns) == 19
                self._add_feature(columns)

    def create(self):
        """Create the RDF storage structure and add the instance data."""
        self._create_ontologies()
        self._add_data()

    def save(self, ontology_name, instances_name):
        """Serialize the graph into files."""
        logger.info('Saving serialized ontology into file: %s' % ontology_name)
        with open(ontology_name, 'w') as f:
            f.write(self.ontology.serialize(format='n3'))
        logger.info('Ontology saved successfully.')
        logger.info('Saving serialized instances into file: '
                    '%s' % instances_name)
        with open(instances_name, 'w') as f:
            f.write(self.instances.serialize(format='n3'))
        logger.info('Instances saved successfully.')


class Storage(object):

    def __init__(self):
        logger.info('Initializing Lucene storage.')

        self.directory = lucene.SimpleFSDirectory(
            lucene.File(settings.INDEX_FOLDER))
        self.analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)
        self.formatter = lucene.SimpleHTMLFormatter('<b>', '</b>')
        self.searcher = lucene.IndexSearcher(self.directory, True)

    def get_label(self, ontology, uri):
        triples = list(ontology.triples((uri, RDFS.label, None)))
        if triples:
            return triples[0][2]
        return uri

    def place_info(self, ontology, geoname_id):
        if ontology is None:
            return {}
        info = {}
        place = FF[str(geoname_id)]

        for subject, predicate, tobject in ontology.triples((place, None, None)):
            if '#' in predicate:
                key = predicate[predicate.rindex('#') + 1:]
            else:
                key = predicate[predicate.rindex('/') + 1:]
            is_literal = type(tobject) == Literal
            if is_literal:
                object_label = None
            else:
                object_label = self.get_label(ontology, tobject)
            is_local = False
            if not is_literal and tobject.startswith(FF):
                is_local = True
            info[key] = {
                'isLiteral': is_literal,
                'isLocal': is_local,
                'predicateLabel': self.get_label(ontology, predicate),
                'object': tobject,
                'objectLabel': object_label,
            }
        return info

    def place_info_simple(self, ontology, geoname_id):
        info = self.place_info(ontology, geoname_id)
        simple_info = {}

        if 'type' in info:
            simple_info['type'] = info['type']['objectLabel']

        if 'label' in info:
            simple_info['label'] = info['label']['objectLabel']

        for acode in ('admin1Code', 'admin2Code'):
            if acode in info:
                simple_info[acode] = info[acode]['object']
                simple_info[acode + 'Label'] = info[acode]['objectLabel']

        for prop in ('countryCode', 'population', 'latitude', 'longitude'):
            if prop in info:
                simple_info[prop] = info[prop]['object']

        return simple_info

    def search(self, query, ontology=None, partial=False, max_results=200):
        if not query or len(query.strip().replace('*', '')) < 1:
            return 0, []
        words = query.strip().split()
        if partial:
            # Add wildcard to each search word.
            words = [word + '*' for word in words if not word.endswith('*')]
        query_str = ' '.join(words)
        lquery = lucene.QueryParser(lucene.Version.LUCENE_CURRENT,
                                    'label', self.analyzer).parse(query_str)
        scorer = lucene.QueryScorer(lquery)
        highlighter = lucene.Highlighter(self.formatter, scorer)

        results = self.searcher.search(lquery, None, max_results)
        hits = results.totalHits

        places = []
        for score_doc in results.scoreDocs:
            doc = self.searcher.doc(score_doc.doc)
            geoname_id = int(doc['geonameid'])
            label = doc['label']
            label_hi = highlighter.getBestFragment(self.analyzer,
                                                   'label', label)
            score = score_doc.score
            places.append({
                'geoname_id': geoname_id,
                'label': label,
                'label_hi': label_hi,
                'score': score,
                'info': self.place_info_simple(ontology, geoname_id),
                })
        return hits, places
