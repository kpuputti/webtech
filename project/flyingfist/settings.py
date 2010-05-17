import logging
import os.path


# The root folder of the project.
PROJECT_ROOT = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

LOG_FILE = os.path.join(PROJECT_ROOT, 'log', 'flyingfist.log')
LOG_LEVEL = logging.DEBUG

TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'templates')

# Namespace definitions.
_NS_DOMAIN = 'http://localhost:8080/'
NS_FLYINGFIST = _NS_DOMAIN + 'flyingfist/'

# countryInfo.txt column names:
#
# 00 ISO
# 01 ISO3
# 02 ISO-Numeric
# 03 fips
# 04 Country Capital Area(in sq km)
# 05 Population
# 06 Continent
# 07 tld
# 08 CurrencyCode
# 09 CurrencyName
# 10 Phone
# 11 Postal Code Format
# 12 Postal Code Regex
# 13 Languages
# 14 geonameid
# 15 neighbours
# 16 EquivalentFipsCode

COLUMNS_COUNTRY_INFO = (
    ('iso', 'ISO code', True),
    ('iso3', 'ISO3 code', True),
    ('isoNumeric', 'ISO numeric code', True),
    ('fips', 'fips', True),
    ('countryCapitalArea', 'country capital area (in sq km)', True),
    ('population', 'population', True),
    ('continent', 'continent', True),
    ('tld', 'top level domain', True),
    ('currencyCode', 'currency code', True),
    ('currencyName', 'currency name', True),
    ('phone', 'phone', True),
    ('postalCodeFormat', 'postal code format', True),
    ('postalCodeRegex', 'postal code regex', False),
    ('languages', 'languages', True),
    ('feature', 'feature', True),
    ('neighbours', 'neighbours', True),
    ('equivalentFipsCode', 'equivalent fips code', True),
)

# NL.txt column names:
#
#  geonameid         : integer id of record in geonames database
#  name              : name of geographical point (utf8) varchar(200)
#  asciiname         : name of geographical point in plain ascii characters, varchar(200)
#  alternatenames    : alternatenames, comma separated varchar(5000)
#  latitude          : latitude in decimal degrees (wgs84)
#  longitude         : longitude in decimal degrees (wgs84)
#  feature class     : see http://www.geonames.org/export/codes.html, char(1)
#  feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
#  country code      : ISO-3166 2-letter country code, 2 characters
#  cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
#  admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
#  admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
#  admin3 code       : code for third level administrative division, varchar(20)
#  admin4 code       : code for fourth level administrative division, varchar(20)
#  population        : bigint (8 byte int)
#  elevation         : in meters, integer
#  gtopo30           : average elevation of 30'x30' (ca 900mx900m) area in meters, integer
#  timezone          : the timezone id (see file timeZone.txt)
#  modification date : date of last modification in yyyy-MM-dd format

COLUMNS_FEATURE = (
    'geonameid',
    'name',
    'asciiname',
    'alternatenames',
    'latitude',
    'longitude',
    'feature class',
    'feature code',
    'country code',
    'cc2',
    'admin1 code',
    'admin2 code',
    'population',
    'elevation',
    'gtopo30',
    'timezone',
    'modification date',
)

# Continent codes :
# AF : Africa           geonameId=6255146
# AS : Asia         geonameId=6255147
# EU : Europe           geonameId=6255148
# NA : North America        geonameId=6255149
# OC : Oceania          geonameId=6255151
# SA : South America        geonameId=6255150
# AN : Antarctica           geonameId=6255152

CONTINENTS = {
    'AF': 6255146,
    'AS': 6255147,
    'EU': 6255148,
    'NA': 6255149,
    'OC': 6255151,
    'SA': 6255150,
    'AN': 6255152,
}

PROPERTIES = {
    'feature': 'feature',
    'description': 'description',
    'geonameId': 'geoname id',
    'alternateNames': 'alternate names',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'countryCode': 'country code',
    'cc2': 'cc2',
    'admin1Code': 'admin1 code',
    'admin2Code': 'admin 2 code',
    'admin3Code': 'admin 3 code',
    'admin4Code': 'admin 4 code',
    'population': 'population',
    'elevation': 'elevation',
    'timezone': 'timezone',
}

_DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data')

FILE_ADMIN1_CODES = os.path.join(_DATA_FOLDER, 'admin1Codes.txt')
FILE_ADMIN2_CODES = os.path.join(_DATA_FOLDER, 'admin2Codes.txt')
FILE_FEATURE_CODES = os.path.join(_DATA_FOLDER, 'featureCodes_en.txt')
FILE_COUNTRY_INFO = os.path.join(_DATA_FOLDER, 'countryInfo.txt')
FILE_NL_FEATURES = os.path.join(_DATA_FOLDER, 'NL.txt')

_OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, 'output')
ONTOLOGY_FILE = os.path.join(_OUTPUT_FOLDER, 'ontology.n3')
INSTANCES_FILE = os.path.join(_OUTPUT_FOLDER, 'instances.n3')
