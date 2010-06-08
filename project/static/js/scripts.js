/*jslint white: true, browser: true, onevar: true, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true */
/*global jquery: false, $: false, google: false, console: false, PLACE: false*/

var LOG = function (s) {
    try {
        console.log(s);
    } catch (e) {}
};

// Root namespace for all code.
var FF = {};

FF.feature = (function () {

    var map,
        point,
        marker,

        wikiUrl = '/api',
        fetched = false,
        wikiMarkers = [],
        wikiBusy = false,
        wikiIcon,

        addMarker = function (obj) {

            var marker,
                markerPoint,
                infoWindow;

            markerPoint = new google.maps.LatLng(obj.lat, obj.lng);

            marker = new google.maps.Marker({
                position: markerPoint,
                map: map,
                title: obj.title,
                icon: wikiIcon
            });

            infoWindow = new google.maps.InfoWindow({
                content: obj.popupHtml,
                size: new google.maps.Size(300, 200)
            });

            LOG(obj.popupHtml);

            google.maps.event.addListener(marker, 'click', function () {
                infoWindow.open(map, marker);
            });

            return marker;

        },

        initWikipedia = function () {

            var wikiToggle = $('#toggle-wikipedia input');
            wikiIcon = new google.maps.MarkerImage('/static/img/wikipedia.png');

            wikiToggle.click(function (e) {
                var checked = wikiToggle.is(':checked'),
                    i, bounds, ne, sw, params;

                if (wikiBusy) {
                    LOG('Wikipedia fetching busy.');
                    return;
                }

                if (checked && !fetched) {

                    LOG('checked for first time');

                    bounds = map.getBounds();
                    ne = bounds.getNorthEast();
                    sw = bounds.getSouthWest();

                    params = {
                        method: 'wikipedia',
                        north: ne.lat(),
                        south: sw.lat(),
                        east: ne.lng(),
                        west: sw.lng()
                    };

                    wikiBusy = true;
                    $.getJSON(wikiUrl, params, function (data, textStatus) {
                        var i;
                        fetched = true;
                        for (i = 0; i < data.length; i += 1) {
                            wikiMarkers.push(addMarker(data[i]));
                        }
                        wikiBusy = false;
                        wikiToggle.attr('checked', 'checked');
                    });

                } else if (checked && fetched) {
                    LOG('checked, data already fetched');
                    for (i = 0; i < wikiMarkers.length; i += 1) {
                        wikiMarkers[i].setVisible(true);
                    }
                    wikiToggle.attr('checked', 'checked');
                } else {
                    LOG('uncheck');
                    for (i = 0; i < wikiMarkers.length; i += 1) {
                        wikiMarkers[i].setVisible(false);
                    }
                    wikiToggle.attr('checked', '');
                }
            });

        },

        initMap = function (mapContainer) {
            try {
                point = new google.maps.LatLng(
                    parseFloat(PLACE.latitude, 10),
                    parseFloat(PLACE.longitude, 10)
                );
            } catch (e) {
                LOG('Place coordinates invalid.');
                return;
            }
            LOG('Initializing map.');
            LOG(point);
            map = new google.maps.Map(mapContainer, {
                center: point,
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });
            marker = new google.maps.Marker({
                position: point,
                title: PLACE.label,
                map: map
            });
        };

    return {
        init: function () {
            var mapElem = $('#map');
            if (mapElem.length !== 1 || !PLACE) {
                LOG('Map elem not found, not initializing map.');
                return;
            }
            initMap(mapElem.get(0));
            initWikipedia();
        }
    };
}());


$(document).ready(function () {
    $('#q').focus().autocomplete({
        source: '/api?method=autocomplete'
    });
    FF.feature.init();
});
