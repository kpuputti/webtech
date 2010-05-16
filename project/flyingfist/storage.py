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
        self.ontology.bind('flyingfist', self.flyingfist)
        self.instances.bind('flyingfist', self.flyingfist)

    def _add_classes(self):
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

        feature_code = self.flyingfist['FeatureCode']
        self.ontology.add((feature_code, RDF.type, RDFS.Class))
        self.ontology.add((feature_code, RDFS.label, Literal('feature code')))

    def _add_properties(self):
        feature = self.flyingfist['feature']
        self.ontology.add((feature, RDF.type, RDF.Property))
        self.ontology.add((feature, RDFS.label, Literal('feature')))
        description = self.flyingfist['description']
        self.ontology.add((description, RDF.type, RDF.Property))
        self.ontology.add((description, RDFS.label, Literal('description')))


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
        feature_code = self.flyingfist['FeatureCode']
        description_prop = self.flyingfist['description']
        with open(settings.FILE_FEATURE_CODES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                try:
                    code, name, description = line.split('\t')
                except ValueError:
                    code, name = line.split('\t')
                    description = None
                if name != 'null':
                    instance = self.flyingfist[code]
                    self.ontology.add((instance, RDF.type, RDFS.Class))
                    self.ontology.add((instance, RDFS.subClassOf, feature_code))
                    self.ontology.add((instance, RDFS.label, Literal(name)))
                    if description:
                        self.ontology.add((instance, description_prop,
                                           Literal(description)))

    def _add_country_info_columns(self):
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
        self._add_country_info_columns()
        self._add_feature_columns()

    def _add_data(self):
        """Add all the instance data to the RDF storage."""

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
