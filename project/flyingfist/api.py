from datetime import datetime
import json
import logging
import urllib2


logger = logging.getLogger('flyingfist.api')
URL_WEATHER = 'http://ws.geonames.org/findNearByWeatherJSON?'
URL_WIKIPEDIA = 'http://ws.geonames.org/wikipediaBoundingBoxJSON?'


def _filter_weather(weather):
    order = {
        'datetime': '001',
        'temperature': '002',
        'clouds': '003',
        'windSpeed': '004',
        'humidity': '005',
    }
    if 'temperature' in weather:
        weather['temperature'] = weather['temperature'] + ' &deg;C'
    if 'windSpeed' in weather:
        weather['windSpeed'] = weather['windSpeed'] + ' m/s'
    if 'datetime' in weather:
        d = datetime.strptime(weather['datetime'], '%Y-%m-%d %H:%M:%S')
        weather['datetime'] = d.strftime('%a %b %d %Y at %H:%M')
    filtered = [(k, v) for k, v in weather.iteritems() if k in order]
    return sorted(filtered, key=lambda (k, v): order.get(k, k))


def get_weather(lat, lng):
    logger.debug('Fetching weather information.')
    url = '%s&lat=%f&lng=%f' % (URL_WEATHER, lat, lng)
    try:
        data = json.loads(urllib2.urlopen(url).read())
    except urllib2.URLError:
        logger.error('Could not open or read url: %s' % url)
        return None
    logger.debug('Finished fetching weather information.')
    return _filter_weather(data.get('weatherObservation', None))


def _get_wikipedia_html(wiki):
    img = ''
    if 'thumbnailImg' in wiki:
        img = '<img src="%s" />' % wiki['thumbnailImg']
    return '''\
    <div class="wikipedia-popup">
        <h4>%(title)s</h4>
        <p>%(img)s%(summary)s</p>
        <p><a href="%(url)s" target="_blank">go to the Wikipedia page</a></p>
    </div>
    ''' % ({
        'title': wiki.get('title', ''),
        'summary': wiki.get('summary', ''),
        'img': img,
        'url': 'http://' + wiki['wikipediaUrl']
    })


def _filter_wikipedia(wikipedia):
    if not wikipedia or 'geonames' not in wikipedia:
        return []
    data = []
    for wiki in wikipedia['geonames']:
        data.append({
            'lat': wiki['lat'],
            'lng': wiki['lng'],
            'popupHtml': _get_wikipedia_html(wiki),
            'url': 'http://' + wiki['wikipediaUrl'],
            'title': wiki.get('title', None),
            'summary': wiki.get('summary', None),
            'img': wiki.get('thumbnailImg', None),
        })
    return data


def get_wikipedia(north, south, east, west):
    logger.debug('Fetching Wikipedia information.')
    url = '%s&north=%s&south=%s&east=%s&west=%s' % (URL_WIKIPEDIA, north,
                                                    south, east, west)
    logger.debug(url)
    try:
        data = json.loads(urllib2.urlopen(url).read())
    except urllib2.URLError:
        logger.error('Could not open or read url: %s' % url)
        return None
    logger.debug('Finished fetching Wikipedia information.')
    return _filter_wikipedia(data)

