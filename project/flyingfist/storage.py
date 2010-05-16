"""Helper functions to create the RDF storage.
"""
from flyingfist import settings
from rdflib import Literal
from rdflib import Namespace
from rdflib import RDF
from rdflib import RDFS
from rdflib import graph
import logging


logger = logging.getLogger('flyingfist.storage')


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
        self.instances.add((instance,
                            self.flyingfist['alternateNames'],
                            Literal(alternate_names)))
        self.instances.add((instance,
                            self.flyingfist['latitude'],
                            Literal(latitude)))
        self.instances.add((instance,
                            self.flyingfist['longitude'],
                            Literal(longitude)))
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
        pass

    def query(self, query):
        # TODO: execute the SPARQL query
        pass
