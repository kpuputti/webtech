# Namespace definitions.
_NS_DOMAIN = 'http://example.org/'
_NS_BASE = _NS_DOMAIN + 'flyingfist/'

NS_PROPERTIES = _NS_BASE + 'properties/'
NS_FEATURES = _NS_BASE + 'features/'

NS_ADMIN1_CODES = _NS_BASE + 'admin1Codes/'
NS_ADMIN2_CODES = _NS_BASE + 'admin2Codes/'

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
    'ISO',
    'ISO3',
    'ISO-Numeric',
    'fips',
    'Country Capital Area(in sq km)',
    'Population',
    'Continent',
    'tld',
    'CurrencyCode',
    'CurrencyName',
    'Phone',
    'Postal Code Format',
    'Postal Code Regex',
    'Languages',
    'geonameid',
    'neighbours',
    'EquivalentFipsCode',
)
