"""
[fist.py]
Script to control the Flying Fist application.

Usage:

1. Run application:
python fist.py run

2. Create the RDF storage (clears the storage first):
python fist.py create_storage

3. Clear the RDF storage:
python fist.py clear_storage
"""
from flyingfist import settings
from flyingfist import storage
import logging
import sys


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
        st = storage.Storage()
        st.create()
    elif operation == 'clear_storage':
        logger.info('Clearing the RDF storage.')
        st = storage.Storage()
        st.clear()
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
