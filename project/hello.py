import cherrypy


class HelloWorld(object):
    def index(self):
        return 'hello, world'
    index.exposed = True


cherrypy.quickstart(HelloWorld())
