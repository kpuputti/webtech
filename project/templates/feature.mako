<%inherit file="base.mako"/>

<%def name="title()">${label}</%def>

<div id="header">

  <h1>${label}</h1>

  <form id="search" action="/search" method="get" autocomplete="off">
    <input type="text" id="q" name="q" />
    <input type="submit" value="Search" />
  </form>

</div>

<div id="map"></div>

<script type="text/javascript">
  var PLACE = ${info};
</script>
