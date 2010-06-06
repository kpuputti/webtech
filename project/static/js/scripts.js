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
        }
    };
}());


$(document).ready(function () {
    $('#q').focus().autocomplete({
        source: '/api?method=autocomplete'
    });
    FF.feature.init();
});
