from flyingfist import settings
from rdflib import Namespace
from rdflib import RDF
from rdflib import RDFS


FF = Namespace(settings.NS_FLYINGFIST)


def escape_html(s):
    escapes = (
        ('&', '&amp;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
    )
    escaped = s
    for ch, seq in escapes:
        escaped = escaped.replace(ch, seq)
    return escaped


def get_sparql_query(select='?res', body=''):
    return '''\
    PREFIX rdf:<%(rdf)s>
    PREFIX rdfs:<%(rdfs)s>
    PREFIX ff:<%(ff)s>
    SELECT %(select)s
    WHERE {
    %(body)s
    }''' % ({
        'rdf': str(RDF),
        'rdfs': str(RDFS),
        'ff': str(FF),
        'select': select,
        'body': body,
    })
