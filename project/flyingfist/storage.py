"""Helper functions to create the RDF storage.
"""
from flyingfist import settings
import logging


logger = logging.getLogger('flyingfist.storage')


class StorageCreator(object):

    def __init__(self):
        pass

    def _add_admin1_codes(self):
        with open(settings.FILE_ADMIN1_CODES) as f:
            for line in f:
                try:
                    code, name = line.strip().split('\t')
                except ValueError:
                    code, name = line.strip(), None


    def _add_admin2_codes(self):
        pass

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

_store = None

class Storage(object):

    def __init__(self):
        if _store is None:
            # TODO: create a new store
            pass

    def query(self, query):
        # TODO: execute the SPARQL query
        pass
