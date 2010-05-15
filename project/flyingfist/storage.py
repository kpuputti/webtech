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
        self.graph = graph.ConjunctiveGraph()
        self.classes = Namespace(settings.NS_CLASSES)
        self.admin_codes = Namespace(settings.NS_ADMIN_CODES)


    def _add_admin1_codes(self):
        logger.info('Adding admin 1 codes to the graph.')

        # Add the admin1Code Class to the graph.
        admin_code_class = self.classes['admin1Code']
        self.graph.add((admin_code_class, RDF.type, RDFS.Class))
        self.graph.add((admin_code_class, RDFS.label, Literal('admin 1 code')))

        with open(settings.FILE_ADMIN1_CODES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                try:
                    code, name = line.split('\t')
                except ValueError:
                    code, name = line, None
                code_instance = self.admin_codes[code]
                self.graph.add((code_instance, RDF.type,
                                admin_code_class))
                if name is not None:
                    self.graph.add((code_instance, RDFS.label,
                                    Literal(name)))


    def _add_admin2_codes(self):
        logger.info('Adding admin 2 codes to the graph.')

        # Add the admin2Code Class to the graph.
        admin_code_class = self.classes['admin2Code']
        self.graph.add((admin_code_class, RDF.type, RDFS.Class))
        self.graph.add((admin_code_class, RDFS.label, Literal('admin 2 code')))

        with open(settings.FILE_ADMIN2_CODES) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                code, name, asciiname, geonameid = line.split('\t')
                code_instance = self.admin_codes[code]
                self.graph.add((code_instance, RDF.type,
                                admin_code_class))
                self.graph.add((code_instance, RDFS.label,
                                Literal(name)))


    def _add_feature_codes(self):
        pass

    def _add_country_info_columns(self):
        pass

    def _add_feature_columns(self):
        pass

    def _create_ontologies(self):
        """Create the ontology structure.

        Data is read from the Geonames files and an RDF ontology is
        created of the classes and properties.
        """
        self._add_admin1_codes()
        self._add_admin2_codes()
        self._add_feature_codes()
        self._add_country_info_columns()
        self._add_feature_columns()

    def _add_data(self):
        """Add all the instance data to the RDF storage."""

    def clear(self):
        """Clears the whole RDF storage."""

    def create(self):
        """Create the RDF storage structure and add the instance data."""
        self.clear()
        self._create_ontologies()
        self._add_data()

    def save(self):
        """Serialize the graph into files."""
        pass


class Storage(object):

    def __init__(self):
        pass

    def query(self, query):
        # TODO: execute the SPARQL query
        pass
