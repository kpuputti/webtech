<%inherit file="base.mako"/>

<%def name="title()">${label}</%def>

<h1>${label}</h1>

<div id="map"></div>

<script type="text/javascript">
  var PLACE = ${info};
</script>
