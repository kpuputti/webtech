"""
[fist.py]
Script to control the Flying Fist application.

Usage:

1. Run application:
python fist.py run

2. Clear the RDF storage:
python fist.py clear_storage

3. Create the RDF storage (clears the storage first):
python fist.py create_storage
"""
import sys
from flyingfist import storage


def main(operation=None):
    if operation == 'run':
        print 'run application'
    elif operation == 'create_storage':
        print 'Creating the RDF storage.'
        st = storage.Storage()
        st.create()
    elif operation == 'clear_storage':
        print 'Clearing the RDF storage.'
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
