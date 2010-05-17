/*jslint white: true, browser: true, onevar: true, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true */
/*global jquery: false, $: false, google: false, console: false*/

var LOG = function (s) {
    try {
        console.log(s);
    } catch (e) {}
};

// Root namespace for all code.
var FF = {};

$(document).ready(function () {
    LOG('init page');
});
