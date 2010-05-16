"""
[fist.py]
Script to control the Flying Fist application.

Usage:

1. Run application:
python fist.py run

2. Create the RDF storage (clears the storage first):
python fist.py create_storage

3. Run the test suite:
python fist test
"""
from flyingfist import settings
from flyingfist import storage
import logging
import sys
import nose


# Set logging configuration.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    filename=settings.LOG_FILE)
logger = logging.getLogger('flyingfist')


def main(operation=None):
    if operation == 'run':
        logger.info('Running the application.')
    elif operation == 'create_storage':
        logger.info('Creating the RDF storage.')
        st = storage.StorageCreator()
        st.create()
        st.save(settings.ONTOLOGY_FILE, settings.INSTANCES_FILE)
    elif operation == 'test':
        logger.info('Running tests.')
        nose.main(argv=['-w', 'tests'])
    else:
        sys.stderr.write('Unknown argument: %s\r\n' % operation)
        print __doc__
        return 2
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(main(sys.argv[1]))
    else:
        sys.stderr.write('Invalid arguments.\r\n')
        print __doc__
        sys.exit(2)
